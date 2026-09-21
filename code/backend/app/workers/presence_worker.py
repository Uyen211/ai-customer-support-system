import asyncio
import logging
import time
from datetime import datetime, timezone

from app.core.redis import redis_client
from app.db.session import SessionLocal
from app.models.user import User
from app.services.user_service import UserService

logger = logging.getLogger(__name__)

OFFLINE_AFTER_SECONDS = 30
SCAN_INTERVAL_SECONDS = 10

# user_id (str) -> last hoạt động (time.time) khi còn kết nối WS
_alive: dict = {}
# user_id (str) -> thời điểm kết nối đóng (time.time); chờ quá OFFLINE_AFTER_SECONDS thì tự OFFLINE
_gone: dict = {}


def register_staff(user_id: str) -> None:
    """Đăng ký nhân viên khi có kết nối WebSocket (heartbeat bắt đầu).

    Kết nối mới = nhân viên đang trực tuyến -> tự phục hồi ONLINE nếu vừa bị
    auto-OFFLINE do rớt kết nối (Use Case 3.2 E-1, chiều quay lại).
    """
    if not user_id:
        return
    uid = str(user_id)
    _alive[uid] = time.time()
    _gone.pop(uid, None)
    _set_online_sync(uid)


def touch_staff(user_id: str) -> None:
    """Cập nhật last_seen khi kết nối còn sống (gọi mỗi vòng lặp WS)."""
    if not user_id:
        return
    uid = str(user_id)
    _alive[uid] = time.time()
    _gone.pop(uid, None)


def drop_staff(user_id: str) -> None:
    """Đánh dấu kết nối vừa đóng; nếu không reconnect trong OFFLINE_AFTER_SECONDS sẽ tự OFFLINE."""
    if not user_id:
        return
    uid = str(user_id)
    _alive.pop(uid, None)
    _gone.setdefault(uid, time.time())


def _set_offline_sync(user_id: str) -> None:
    """Cập nhật status = OFFLINE trong DB + Redis + bắn sự kiện (chạy trong thread)."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.status == "OFFLINE":
            return
        user.status = "OFFLINE"
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        UserService._sync_agent_status(user.id, "OFFLINE")
        logger.info(f"Heartbeat: nhân viên {user.full_name} ({user_id}) mất kết nối -> tự chuyển OFFLINE.")
    except Exception as e:
        db.rollback()
        logger.error(f"Heartbeat: lỗi khi set OFFLINE cho {user_id}: {e}")
    finally:
        db.close()


def _set_online_sync(user_id: str) -> None:
    """Phục hồi status = ONLINE trong DB + Redis + bắn sự kiện khi WS kết nối lại."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.status == "ONLINE":
            return
        user.status = "ONLINE"
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        UserService._sync_agent_status(user.id, "ONLINE")
        logger.info(f"Heartbeat: nhân viên {user.full_name} ({user_id}) kết nối lại WS -> chuyển ONLINE.")
    except Exception as e:
        db.rollback()
        logger.error(f"Heartbeat: lỗi khi phục hồi ONLINE cho {user_id}: {e}")
    finally:
        db.close()


async def start_presence_monitor() -> None:
    """Quét định kỳ: nhân viên nào mất kết nối > 30s => tự chuyển OFFLINE (Use Case 3.2 E-1)."""
    logger.info("Khởi động Presence Monitor (heartbeat 30s -> OFFLINE)...")
    while True:
        await asyncio.sleep(SCAN_INTERVAL_SECONDS)
        now = time.time()

        to_offline: list = []
        for uid, since in list(_gone.items()):
            if now - since > OFFLINE_AFTER_SECONDS:
                _gone.pop(uid, None)
                to_offline.append(uid)
        for uid, seen in list(_alive.items()):
            if now - seen > OFFLINE_AFTER_SECONDS:
                _alive.pop(uid, None)
                to_offline.append(uid)

        for uid in to_offline:
            await asyncio.to_thread(_set_offline_sync, uid)

        try:
            redis_client.set("presence:monitor:last_scan", str(now))
        except Exception:
            pass