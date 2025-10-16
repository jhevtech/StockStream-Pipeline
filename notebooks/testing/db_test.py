from sqlalchemy import create_engine, text
engine = create_engine("postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/market_pulse")
with engine.connect() as conn:
    v = conn.execute(text("SELECT version();")).scalar()
    print("Connected to:", v)
