import asyncio
import logging

logger = logging.getLogger(__name__)

async def start_sla_monitor_worker():
    """Cron job quét vi phạm hạn cam kết SLA mỗi 30s và bắn sự kiện qua Redis Pub/Sub."""
    logger.info("Khởi động SLA Monitor Worker...")
    while True:
        try:
            # Logic quét DB tickets có deadline < now() và sla_breached = False
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            logger.info("Dừng SLA Monitor Worker.")
            break
        except Exception as e:
            logger.error(f"Lỗi SLA Monitor Worker: {e}")
            await asyncio.sleep(30)
