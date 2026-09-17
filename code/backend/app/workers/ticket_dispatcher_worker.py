import asyncio
import logging

logger = logging.getLogger(__name__)

async def start_ticket_dispatcher_worker():
    """Lắng nghe hàng đợi Redis Queue (queue:tickets:pending) để điều phối ticket tự động."""
    logger.info("Khởi động Ticket Dispatcher Worker...")
    while True:
        try:
            # Logic lấy ticket từ Redis queue và phân công Agent
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            logger.info("Dừng Ticket Dispatcher Worker.")
            break
        except Exception as e:
            logger.error(f"Lỗi Ticket Dispatcher Worker: {e}")
            await asyncio.sleep(5)
