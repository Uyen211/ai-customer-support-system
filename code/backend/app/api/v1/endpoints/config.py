from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.models.ai_rule import AIRule
from app.core.redis import redis_client

router = APIRouter()

class AlertConfigUpdate(BaseModel):
    instruction_prompt: str = Field(default="")
    p1_threshold: float = Field(default=-0.60, le=0)
    p2_threshold: float = Field(default=-0.30, le=0)

class AlertConfigResponse(BaseModel):
    id: str
    instruction_prompt: str
    p1_threshold: float
    p2_threshold: float

@router.get("/alerts", response_model=AlertConfigResponse)
def get_alert_config(db: Session = Depends(get_db)):
    config = db.query(AIRule).first()
    
    # Auto-seeding if empty (Singleton)
    if not config:
        config = AIRule(
            instruction_prompt="",
            p1_threshold=-0.60,
            p2_threshold=-0.30
        )
        db.add(config)
        db.commit()
        db.refresh(config)
        
    return {
        "id": str(config.id),
        "instruction_prompt": config.instruction_prompt,
        "p1_threshold": float(config.p1_threshold),
        "p2_threshold": float(config.p2_threshold)
    }

@router.put("/alerts", response_model=AlertConfigResponse)
def update_alert_config(payload: AlertConfigUpdate, db: Session = Depends(get_db)):
    # Validation E-1
    if payload.p1_threshold >= payload.p2_threshold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="P1 threshold must be strictly less than P2 threshold"
        )
        
    config = db.query(AIRule).first()
    if not config:
        config = AIRule()
        db.add(config)
        
    config.instruction_prompt = payload.instruction_prompt
    config.p1_threshold = payload.p1_threshold
    config.p2_threshold = payload.p2_threshold
    
    db.commit()
    db.refresh(config)
    
    # Cache Invalidation
    try:
        redis_client.delete("cache:alert_rules")
    except Exception as e:
        pass # Log error if needed, but don't fail the request
        
    return {
        "id": str(config.id),
        "instruction_prompt": config.instruction_prompt,
        "p1_threshold": float(config.p1_threshold),
        "p2_threshold": float(config.p2_threshold)
    }
