import time
from app.core.redis import redis_client

def start_ticket_dispatcher():
    print("[Worker] Ticket Dispatcher Worker started listening on Redis Queue...")
    while True:
        try:
            # Pop ticket from queue
            ticket_event = redis_client.rpop("queue:tickets:pending")
            if ticket_event:
                print(f"[Worker] Processing ticket event: {ticket_event}")
                # Implementation of Least-Loaded dispatcher algorithm
            else:
                time.sleep(2)
        except Exception as e:
            print(f"[Worker Error] Dispatcher error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_ticket_dispatcher()
