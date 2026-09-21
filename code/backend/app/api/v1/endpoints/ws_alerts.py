import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.core.security import decode_access_token
from app.core.redis import redis_client

router = APIRouter(prefix="/ws", tags=["WebSockets"])
logger = logging.getLogger(__name__)

# Lưu trữ các kết nối alerts (in-memory)
active_alert_connections = []

@router.websocket("/alerts")
async def websocket_alerts(websocket: WebSocket, token: str = Query(...)):
    # Xác thực token cơ bản
    payload = decode_access_token(token)
    if not payload or payload.get("role") == "CUSTOMER":
        await websocket.close(code=1008)
        return

    await websocket.accept()
    active_alert_connections.append(websocket)
    logger.info(f"Staff connected to /ws/alerts. Total: {len(active_alert_connections)}")

    try:
        # Giữ connection mở bằng vòng lặp nhận tin nhắn (nếu client gửi)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_alert_connections.remove(websocket)
        logger.info("Staff disconnected from /ws/alerts")

# Background task để lắng nghe Redis pub/sub và forward tới các WebSocket đang mở
async def listen_to_redis_alerts():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("channel:ws_alerts")
    logger.info("Started Redis pubsub listener for channel:ws_alerts")
    
    while True:
        # Sử dụng asyncio.to_thread để tránh block event loop do redis_client là thư viện đồng bộ
        message = await asyncio.to_thread(pubsub.get_message, ignore_subscribe_messages=True, timeout=1.0)
        if message and message["type"] == "message":
            data = message["data"]
            # Forward data tới tất cả active connections
            disconnected = []
            for ws in active_alert_connections:
                try:
                    await ws.send_text(data)
                except Exception as e:
                    logger.error(f"Lỗi khi gửi alert tới WS: {e}")
                    disconnected.append(ws)
            
            for ws in disconnected:
                if ws in active_alert_connections:
                    active_alert_connections.remove(ws)
        
        await asyncio.sleep(0.1)
