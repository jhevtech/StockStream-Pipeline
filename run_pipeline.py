from src.ingestion.fetch_stock import fetch_stock_data
from datetime import datetime

def run_pipeline():
    print(f"Market Pulse Pipeline Started at {datetime.now()}")
    fetch_stock_data()
    print(f"Pipeline Successfully ran at {datetime.now()}")


if __name__ == "__main__":
    run_pipeline()