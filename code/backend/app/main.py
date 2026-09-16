from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.modules.rag_assistant.router import router as rag_router

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

# Register Sub-module Routers
app.include_router(rag_router)

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

