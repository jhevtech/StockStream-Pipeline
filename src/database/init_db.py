import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Base
from database.connection import get_engine

from sqlalchemy import text

def init_db():
    """creating tables"""
    try: 
        engine = get_engine()
        print(f"Connecting to database: {engine}")
        Base.metadata.create_all(engine)
        print("Database tables created successfully!")

        #test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), current_user"))
            db_name, user = result.fetchone()
            print(f"Connected to database '{db_name}' as user '{user}'")

    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    init_db()
