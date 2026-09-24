from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime, date
from uuid import UUID
from typing import Optional

from app.api.deps import get_db, require_roles
from app.models.user import User
from app.models.ticket import Ticket
from app.models.conversation import Conversation
from app.schemas.report import PerformanceReportResponse, AgentPerformanceSchema

router = APIRouter(prefix="/admin/reports", tags=["Reports"])

@router.get("/performance", response_model=PerformanceReportResponse, summary="Báo cáo thống kê hiệu suất (UC 4.4)")
def get_performance_report(
    start_date: str = Query(..., description="Từ ngày (DD/MM/YYYY)"),
    end_date: str = Query(..., description="Đến ngày (DD/MM/YYYY)"),
    agent_id: Optional[UUID] = Query(None, description="Lọc theo nhân viên"),
    priority: Optional[str] = Query(None, description="Lọc theo mức độ ưu tiên"),
    category: Optional[str] = Query(None, description="Lọc theo danh mục sự cố"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("MANAGER", "ADMIN"))
):
    # Validate date
    try:
        start_dt = datetime.strptime(start_date, "%d/%m/%Y").date()
        end_dt = datetime.strptime(end_date, "%d/%m/%Y").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ngày nhập không đúng định dạng DD/MM/YYYY")

    today = date.today()
    if start_dt > end_dt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc")
    if end_dt > today:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ngày kết thúc không được vượt quá ngày hiện tại")
    
    delta = (end_dt - start_dt).days
    if delta > 365:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khoảng thời gian tra cứu tối đa không vượt quá 365 ngày")

    # Start date string for db query (00:00:00) and end date (23:59:59)
    query_start = datetime.strptime(start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
    query_end = datetime.strptime(end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")

    # Base query
    stmt = select(Ticket, Conversation).join(Conversation, Ticket.conversation_id == Conversation.id).where(
        Ticket.created_at >= query_start,
        Ticket.created_at <= query_end
    )

    if agent_id:
        stmt = stmt.where(Ticket.assigned_to == agent_id)
    if priority:
        stmt = stmt.where(Ticket.priority == priority)
    if category:
        stmt = stmt.where(Ticket.category == category)

    results = db.execute(stmt).all()

    # Aggregate
    n_total = len(results)
    if n_total == 0:
        return PerformanceReportResponse(
            n_total=0,
            n_resolved=0,
            n_in_progress=0,
            n_breached=0,
            sla_breach_rate=0.0,
            sentiment_distribution={"Tích cực": 0, "Bình thường": 0, "Tiêu cực nhẹ": 0, "Bức xúc cao": 0},
            agent_performance=[]
        )

    n_resolved = 0
    n_in_progress = 0
    n_breached = 0
    sentiment_dist = {"Tích cực": 0, "Bình thường": 0, "Tiêu cực nhẹ": 0, "Bức xúc cao": 0}
    agent_map = {}

    for t, c in results:
        # Status counts
        if t.status in ["RESOLVED", "CLOSED"]:
            n_resolved += 1
        if t.status in ["PENDING", "IN_PROGRESS"]:
            n_in_progress += 1
            
        # SLA breached
        if t.sla_breached:
            n_breached += 1
            
        # Sentiment mapping
        s = c.last_sentiment
        if s == "POSITIVE":
            sentiment_dist["Tích cực"] += 1
        elif s == "NEUTRAL":
            sentiment_dist["Bình thường"] += 1
        elif s == "NEGATIVE":
            sentiment_dist["Tiêu cực nhẹ"] += 1
        elif s == "CRITICAL":
            sentiment_dist["Bức xúc cao"] += 1

        # Agent performance
        if t.assigned_to:
            aid = str(t.assigned_to)
            if aid not in agent_map:
                agent_map[aid] = {"total": 0, "resolved": 0}
            agent_map[aid]["total"] += 1
            if t.status in ["RESOLVED", "CLOSED"]:
                agent_map[aid]["resolved"] += 1

    sla_breach_rate = round((n_breached / n_total) * 100, 1)

    # Fetch agent names
    agent_ids = [UUID(aid) for aid in agent_map.keys()]
    agent_performance = []
    if agent_ids:
        agents = db.execute(select(User).where(User.id.in_(agent_ids))).scalars().all()
        agent_names = {str(a.id): a.full_name for a in agents}
        
        for aid, stats in agent_map.items():
            agent_performance.append(AgentPerformanceSchema(
                agent_id=aid,
                agent_name=agent_names.get(aid, "Unknown"),
                n_resolved=stats["resolved"],
                n_total=stats["total"]
            ))

    return PerformanceReportResponse(
        n_total=n_total,
        n_resolved=n_resolved,
        n_in_progress=n_in_progress,
        n_breached=n_breached,
        sla_breach_rate=sla_breach_rate,
        sentiment_distribution=sentiment_dist,
        agent_performance=agent_performance
    )
