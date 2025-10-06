import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

def get_db_url():
    """PostgreSQL connection"""
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5433')
    database = os.getenv('DB_NAME', 'market_pulse')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', 'postgres')

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def get_engine():
    """SQLAlchemy engine"""
    database_url = get_db_url()
    engine = create_engine(database_url, echo=False)
    return engine

def get_session():
    """Database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
