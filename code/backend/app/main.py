import asyncio
from app.api.v1.endpoints.ws_alerts import listen_to_redis_alerts
from app.workers.ticket_dispatcher_worker import start_ticket_dispatcher_worker
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.v1.api import api_router

# Create tables in Database if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Omnichannel Customer Support System API",
    description="FastAPI Backend for Omnichannel Support, RAG Chatbot, AI Auto-Triage, Live Console & SLA Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký API Routers cho tất cả các tiền tố (/api/v1, /api và gốc /)
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router, prefix="/api")
app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Omnichannel CSKH Backend",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(listen_to_redis_alerts())
    asyncio.create_task(start_ticket_dispatcher_worker())
