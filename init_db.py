from sqlalchemy import create_engine
from database import Base

def init_database():
    """Initialize the database and create all tables"""
    try:
        engine = create_engine('sqlite:///chat.db', echo=True)
        Base.metadata.create_all(engine)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_database() 