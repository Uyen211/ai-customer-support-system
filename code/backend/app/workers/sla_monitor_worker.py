import asyncio
import logging
import json
from sqlalchemy import select, func, update

from app.db.session import SessionLocal
from app.models.ticket import Ticket
from app.models.user import User
from app.core.redis import redis_client

logger = logging.getLogger(__name__)

async def start_sla_monitor_worker():
    """Cron job quét vi phạm hạn cam kết SLA mỗi 30s và bắn sự kiện qua Redis Pub/Sub."""
    logger.info("Khởi động SLA Monitor Worker...")
    while True:
        try:
            # Lấy các Session riêng cho background job
            with SessionLocal() as db:
                # 1. Tìm các ticket IN_PROGRESS đã quá hạn nhưng chưa đánh dấu breached
                # Sử dụng with_for_update(skip_locked=True) để tránh block các worker khác nếu chạy nhiều bản sao
                overdue_tickets = db.execute(
                    select(Ticket)
                    .where(
                        Ticket.status == "IN_PROGRESS",
                        Ticket.sla_breached == False,
                        Ticket.sla_deadline <= func.now()
                    )
                    .with_for_update(skip_locked=True)
                ).scalars().all()

                for ticket in overdue_tickets:
                    # 2. Đánh dấu vi phạm
                    ticket.sla_breached = True
                    
                    # 3. Lấy thông tin nhân viên để báo động
                    agent = db.execute(select(User).where(User.id == ticket.assigned_to)).scalar_one_or_none()
                    agent_name = agent.full_name if agent else "Unknown Agent"
                    
                    # 4. Gửi sự kiện báo động lên Manager
                    alert_msg = f"Phiếu hỗ trợ {ticket.id} do nhân viên {agent_name} phụ trách đã quá hạn xử lý!"
                    payload = {
                        "event": "SLA_BREACH_ALERT",
                        "payload": {
                            "ticket_id": str(ticket.id),
                            "assigned_to": str(ticket.assigned_to),
                            "agent_name": agent_name,
                            "message": alert_msg
                        }
                    }
                    redis_client.publish("channel:ws_alerts", json.dumps(payload))
                    
                    logger.warning(f"[SLA BREACH] Ticket {ticket.id} assigned to {agent_name}")

                if overdue_tickets:
                    db.commit()

            await asyncio.sleep(30)
        except asyncio.CancelledError:
            logger.info("Dừng SLA Monitor Worker.")
            break
        except Exception as e:
            logger.error(f"Lỗi SLA Monitor Worker: {e}")
            await asyncio.sleep(30)
