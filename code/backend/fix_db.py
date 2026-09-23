import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from sqlalchemy import text

def fix_database():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE tickets ADD COLUMN resolution_note TEXT;"))
            conn.commit()
            print("Successfully added resolution_note column.")
        except Exception as e:
            print(f"Column might already exist or error occurred: {e}")

if __name__ == "__main__":
    fix_database()
