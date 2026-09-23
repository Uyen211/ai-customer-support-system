import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.message import Message
from app.models.ticket import Ticket
from app.models.conversation import Conversation

def reset_chat_data():
    db = SessionLocal()
    try:
        # Delete all messages
        num_messages = db.query(Message).delete()
        
        # Delete all tickets
        num_tickets = db.query(Ticket).delete()
        
        # Delete all conversations
        num_conversations = db.query(Conversation).delete()
        
        db.commit()
        print(f"Data refreshed successfully!")
        print(f"Deleted {num_messages} messages.")
        print(f"Deleted {num_tickets} tickets.")
        print(f"Deleted {num_conversations} conversations.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_chat_data()
