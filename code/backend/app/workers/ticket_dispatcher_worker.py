import asyncio
import logging
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.core.redis import get_redis
from app.models.ticket import Ticket
from app.models.user import User

logger = logging.getLogger(__name__)

def process_ticket_sync(ticket_id: str):
    """Xử lý đồng bộ (Sync) gán ticket cho Agent, chạy trong thread."""
    db: Session = SessionLocal()
    redis_client = get_redis()
    try:
        # Lấy thông tin ticket có lock chống Race Condition
        # Hỗ trợ row-level locking
        ticket = db.query(Ticket).with_for_update().filter(Ticket.id == ticket_id).first()
        if not ticket:
            logger.error(f"Không tìm thấy ticket {ticket_id} trong DB.")
            redis_client.lrem("queue:tickets:processing", 0, ticket_id)
            return
            
        if ticket.status not in ["PENDING"]:
            # Đã có người nhận hoặc đã xử lý, xoá khỏi queue processing
            redis_client.lrem("queue:tickets:processing", 0, ticket_id)
            return

        category = ticket.category
        
        # 3. Lọc danh sách nhân viên đủ điều kiện (Least-Loaded Algorithm)
        # PostgreSQL JSONB operator @>
        agent_workload = db.query(
            User.id, 
            User.full_name,
            func.count(Ticket.id).label('current_tickets')
        ).outerjoin(
            Ticket, 
            (Ticket.assigned_to == User.id) & (Ticket.status.in_(["PENDING", "IN_PROGRESS"]))
        ).filter(
            User.role == 'AGENT',
            User.status == 'ONLINE',
            User.is_active == True
        ).group_by(User.id).order_by('current_tickets').all()

        if not agent_workload:
            # 4. Xử lý ngoại lệ Không có Agent nào hợp lệ
            logger.warning(f"Không có Agent nào ONLINE/phù hợp cho ticket {ticket_id} (Category: {category}).")
            ticket.status = 'PENDING'
            ticket.assigned_to = None
            db.commit()
            
            # Bắn WebSocket UNASSIGNED_TICKET_ALERT cho Admin
            redis_client.publish("channel:ws_alerts", json.dumps({
                "event": "UNASSIGNED_TICKET_ALERT",
                "payload": {
                    "ticket_id": str(ticket.id),
                    "category": ticket.category,
                    "priority": ticket.priority
                }
            }))
            
            redis_client.lrem("queue:tickets:processing", 0, ticket_id)
            return

        # 5. Gán Ticket cho Agent ít việc nhất
        selected_agent = agent_workload[0]
        logger.info(f"Phân công ticket {ticket_id} cho Agent {selected_agent.id} (Tải hiện tại: {selected_agent.current_tickets})")
        
        ticket.assigned_to = selected_agent.id
        ticket.status = 'IN_PROGRESS'
        db.commit()
        
        # Bắn sự kiện TICKET_ASSIGNED qua WebSocket
        redis_client.publish("channel:ws_alerts", json.dumps({
            "event": "TICKET_ASSIGNED",
            "payload": {
                "ticket_id": str(ticket.id),
                "agent_id": str(selected_agent.id),
                "conversation_id": str(ticket.conversation_id)
            }
        }))
        
        # 6. Dọn dẹp hàng đợi processing
        redis_client.lrem("queue:tickets:processing", 0, ticket_id)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Lỗi khi truy vấn DB cho ticket {ticket_id}: {e}")
        # Đưa lại vào pending nếu lỗi DB
        redis_client.lrem("queue:tickets:processing", 0, ticket_id)
        redis_client.lpush("queue:tickets:pending", ticket_id)
    finally:
        db.close()

def pop_ticket_sync():
    """Lấy ticket từ Redis queue (non-blocking)."""
    redis_client = get_redis()
    return redis_client.rpoplpush("queue:tickets:pending", "queue:tickets:processing")

async def start_ticket_dispatcher_worker():
    """Lắng nghe hàng đợi Redis Queue (queue:tickets:pending) để điều phối ticket tự động."""
    logger.info("Khởi động Ticket Dispatcher Worker...")
    
    while True:
        try:
            # Chạy rpoplpush trong thread để tránh block event loop
            ticket_id = await asyncio.to_thread(pop_ticket_sync)
            
            if not ticket_id:
                # Không có ticket nào, chờ 5s rồi poll tiếp
                await asyncio.sleep(5)
                continue
                
            logger.info(f"Đang xử lý phân công cho ticket: {ticket_id}")
            
            # Xử lý logic gán ticket trong thread
            await asyncio.to_thread(process_ticket_sync, ticket_id)
                
        except asyncio.CancelledError:
            logger.info("Dừng Ticket Dispatcher Worker.")
            break
        except Exception as e:
            logger.error(f"Lỗi Ticket Dispatcher Worker loop: {e}")
            await asyncio.sleep(5)
