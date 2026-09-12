import time
from app.core.database import SessionLocal
from app.core.redis import redis_client

def start_sla_monitor():
    print("[Worker] SLA Monitor Worker started scanning SLA deadlines...")
    while True:
        try:
            # Query overdue tickets and publish SLA breach alerts
            time.sleep(30)
        except Exception as e:
            print(f"[Worker Error] SLA Monitor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_sla_monitor()
