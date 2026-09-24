from pydantic import BaseModel
from typing import List, Dict

class AgentPerformanceSchema(BaseModel):
    agent_id: str
    agent_name: str
    n_resolved: int
    n_total: int

class PerformanceReportResponse(BaseModel):
    n_total: int
    n_resolved: int
    n_in_progress: int
    n_breached: int
    sla_breach_rate: float
    sentiment_distribution: Dict[str, int]
    agent_performance: List[AgentPerformanceSchema]
