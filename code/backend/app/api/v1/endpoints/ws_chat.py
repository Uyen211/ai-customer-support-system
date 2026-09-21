import asyncio
import json
import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.core.redis import redis_client
from app.db.session import SessionLocal
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.models.customer import Customer
from app.schemas.conversation import MessageItemSchema
from app.workers.presence_worker import register_staff, touch_staff, drop_staff

router = APIRouter(prefix="/ws", tags=["WebSockets"])
logger = logging.getLogger(__name__)


def _agent_can_access_room(conv: Conversation, user: User, db: Session) -> bool:
    if user.role in ("MANAGER", "ADMIN"):
        return True
    if conv.assigned_agent_id == user.id:
        return True
    # Cho phép nhân viên mở xem và chat trong phiên họ đã tiếp quản; phiên trong hàng đợi cho xem trước
    if conv is not None:
        if conv.assigned_agent_id is None and (conv.is_flagged or conv.mode == "WAITING_HUMAN"):
            return True
    return False


async def _broadcast_room(channel: str, payload: dict) -> None:
    try:
        await asyncio.to_thread(redis_client.publish, channel, json.dumps(payload, ensure_ascii=False))
    except Exception as e:
        logger.error(f"Lỗi publish room {channel}: {e}")


@router.websocket("/chat/{conversation_id}")
async def websocket_chat(websocket: WebSocket, conversation_id: str, token: str = Query(...)):
    # Xác thực & xác định vai trò (khách hàng hoặc nhân viên)
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    role = (payload.get("role") or "CUSTOMER").upper()
    sub_id = payload.get("sub") or payload.get("user_id") or payload.get("customer_id")
    if not sub_id:
        await websocket.close(code=1008)
        return

    try:
        conv_uuid = UUID(conversation_id)
    except (ValueError, TypeError):
        await websocket.close(code=1008)
        return

    db: Session = SessionLocal()
    try:
        conv = db.query(Conversation).filter(Conversation.id == conv_uuid).first()
        if not conv:
            await websocket.close(code=1004)
            return

        if role == "CUSTOMER":
            customer = db.query(Customer).filter(Customer.id == UUID(sub_id)).first()
            if not customer or not customer.is_active or conv.customer_id != customer.id:
                await websocket.close(code=1008)
                return
        else:
            user = db.query(User).filter(User.id == UUID(sub_id), User.is_active == True).first()
            if not user:
                await websocket.close(code=1008)
                return
            if not _agent_can_access_room(conv, user, db):
                await websocket.close(code=1008)
                return
    finally:
        db.close()

    await websocket.accept()

    room_channel = f"channel:chat:{conv_uuid}"
    pubsub = redis_client.pubsub()
    pubsub.subscribe(room_channel)

    staff_id = sub_id if role != "CUSTOMER" else None
    if staff_id:
        register_staff(staff_id)

    logger.info(f"Kết nối WS chat room {conv_uuid} với vai trò {role}")

    try:
        while True:
            # Heartbeat: nhân viên còn kết nối room chat => còn hoạt động
            if staff_id:
                touch_staff(staff_id)
            # Đọc sự kiện phòng từ Redis pub/sub (chuyển hướng: takeover, tin nhắn...)
            try:
                pub_msg = await asyncio.to_thread(
                    pubsub.get_message, ignore_subscribe_messages=True, timeout=0.2
                )
                if pub_msg and pub_msg["type"] == "message":
                    await websocket.send_text(pub_msg["data"])
            except Exception as e:
                logger.error(f"Lỗi đọc pubsub room {conv_uuid}: {e}")

            # Nhận tin nhắn từ client (khách hàng / nhân viên)
            try:
                raw = await asyncio.wait_for(websocket.receive_text(), timeout=0.3)
            except asyncio.TimeoutError:
                continue
            except WebSocketDisconnect:
                break

            try:
                msg = json.loads(raw)
            except Exception:
                continue

            event = msg.get("type") or msg.get("event")
            if event != "send_message":
                continue

            content = (msg.get("content") or "").strip()
            if not content:
                await websocket.send_text(json.dumps(
                    {"type": "error", "event": "ERROR", "payload": {"error": "Vui lòng nhập nội dung tin nhắn."}},
                    ensure_ascii=False
                ))
                continue

            db2: Session = SessionLocal()
            try:
                conv2 = db2.query(Conversation).filter(Conversation.id == conv_uuid).first()
                if not conv2 or conv2.mode == "CLOSED":
                    await websocket.send_text(json.dumps(
                        {"type": "error", "event": "ERROR",
                         "payload": {"error": "Phiên trò chuyện này đã đóng hoặc không tồn tại."}},
                        ensure_ascii=False
                    ))
                    continue

                if role == "CUSTOMER":
                    sender_type = "CUSTOMER"
                    sender_id = None
                else:
                    sender_type = "AGENT"
                    sender_id = UUID(sub_id)

                message = Message(
                    conversation_id=conv2.id,
                    sender_type=sender_type,
                    sender_id=sender_id,
                    content=content
                )
                db2.add(message)
                conv2.updated_at = datetime.now(timezone.utc)
                db2.commit()
                db2.refresh(message)

                # Broadcast tin nhắn mới tới cả phòng (khách + nhân viên)
                await _broadcast_room(room_channel, {
                    "type": "message",
                    "event": "CHAT_MESSAGE",
                    "payload": MessageItemSchema.model_validate(message).model_dump(mode="json"),
                })
                logger.info(f"Đã lưu tin nhắn {sender_type} trong room {conv_uuid}")
            finally:
                db2.close()
    except WebSocketDisconnect:
        logger.info(f"WS chat room {conv_uuid} đóng kết nối ({role})")
    except Exception as e:
        logger.error(f"WS chat room {conv_uuid} lỗi: {e}")
    finally:
        if staff_id:
            drop_staff(staff_id)
        try:
            pubsub.unsubscribe(room_channel)
            pubsub.close()
        except Exception:
            pass