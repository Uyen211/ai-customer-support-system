import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db, require_roles
from app.models.user import User
from app.models.ticket import Ticket
from app.schemas.ticket import TicketAssignRequest, TicketResponse
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
    redis_client.publish("ws_alerts", json.dumps(payload))

    return ticket
