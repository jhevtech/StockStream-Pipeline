import pandas as pd
from .connection import get_session
from .models import StockPrice

def load_latest_data(limit=500):
    session = get_session()

    # Query the most recent rows
    query = (
        session.query(StockPrice)
        .order_by(StockPrice.timestamp.desc())
        .limit(limit)
    )

    rows = query.all()
    session.close()

    # Convert ORM objects → DataFrame
    df = pd.DataFrame([
        {
            "ticker": r.ticker,
            "timestamp": r.timestamp,
            "open": r.open,
            "high": r.high,
            "low": r.low,
            "close": r.close,
            "volume": r.volume
        }
        for r in rows
    ])

    # Ensure chronological order
    return df.sort_values("timestamp")
