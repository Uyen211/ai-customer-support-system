import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.api.deps import get_db, require_roles
from app.models.user import User
from app.models.ticket import Ticket
from app.schemas.ticket import TicketAssignRequest, TicketResponse, TicketResolveRequest
from app.core.redis import redis_client

router = APIRouter(prefix="/admin/tickets", tags=["Tickets Management"])

@router.post(
    "/{ticket_id}/assign",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Gán Ticket thủ công cho Agent (UC 4.1 Luồng con A-1)"
)
def assign_ticket(
    ticket_id: uuid.UUID,
    req: TicketAssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("ADMIN", "MANAGER"))
):
    # 1. Lấy Ticket (có lock)
    ticket = db.execute(
        select(Ticket).where(Ticket.id == ticket_id).with_for_update()
    ).scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket không tồn tại."
        )

    # 2. Lấy Agent
    agent = db.execute(
        select(User).where(User.id == req.agent_id, User.role == "AGENT", User.is_active == True)
    ).scalar_one_or_none()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent không tồn tại hoặc không hợp lệ."
        )

    # 3. Cập nhật Ticket
    ticket.assigned_to = agent.id
    ticket.status = "IN_PROGRESS"
    
    db.commit()
    db.refresh(ticket)

    # 4. Gửi sự kiện WebSocket cho Agent
    payload = {
        "event": "TICKET_ASSIGNED",
        "payload": {
            "ticket_id": str(ticket.id),
            "conversation_id": str(ticket.conversation_id),
            "agent_id": str(agent.id),
            "assigned_by": str(current_user.id)
        }
    }
    # Tương thích với WebSocket Connection Manager (nếu nó đang lắng nghe trên channel chung hoặc channel theo user)
    # Giả định Connection Manager lắng nghe trên channel 'ws_alerts'
    redis_client.publish("channel:ws_alerts", json.dumps(payload))

    return ticket

@router.get(
    "/active",
    response_model=list[TicketResponse],
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách Ticket đang xử lý của Agent"
)
def get_active_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN"))
):
    query = select(Ticket).where(Ticket.status == "IN_PROGRESS")
    if current_user.role == "AGENT":
        query = query.where(Ticket.assigned_to == current_user.id)
    
    tickets = db.execute(query.order_by(Ticket.sla_deadline.asc())).scalars().all()
    return tickets

@router.put(
    "/{ticket_id}/resolve",
    response_model=TicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Hoàn tất xử lý Ticket (UC 4.2)"
)
def resolve_ticket(
    ticket_id: uuid.UUID,
    req: TicketResolveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("AGENT", "MANAGER", "ADMIN"))
):
    # 1. Lấy Ticket (có lock)
    ticket = db.execute(
        select(Ticket).where(Ticket.id == ticket_id).with_for_update()
    ).scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket không tồn tại."
        )

    # 2. Phân quyền: Nếu là AGENT thì chỉ được resolve ticket của chính mình
    if current_user.role == "AGENT" and ticket.assigned_to != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền cập nhật phiếu hỗ trợ do nhân viên khác phụ trách!"
        )

    # 3. Kiểm tra luân chuyển trạng thái
    if ticket.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tiến độ phiếu chỉ được phép chuyển tiến lên theo quy trình (từ Đang xử lý -> Đã giải quyết)."
        )

    # 4. Cập nhật dữ liệu
    ticket.status = "RESOLVED"
    ticket.resolution_note = req.resolution_note.strip()
    ticket.resolved_at = func.now()

    db.commit()
    db.refresh(ticket)
    
    # 5. Broadcast sự kiện UI cập nhật (nếu cần)
    payload = {
        "event": "TICKET_RESOLVED",
        "payload": {
            "ticket_id": str(ticket.id),
            "status": ticket.status
        }
    }
    redis_client.publish("channel:ws_alerts", json.dumps(payload))

    return ticket
