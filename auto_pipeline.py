from src.ingestion.fetch_stock import fetch_stock_data
import time
from datetime import datetime

def auto_pipeline():
    print(f"Starting automation...")
    print("Press Ctrl+c to stop")

    try:
        while True:
            print(f"\n {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            try: 
                fetch_stock_data()
                print("Success! Next run in 15 minutes...")
            except Exception as e:
                print(f"Pipeline error: {e}")
                print("Retrying in 15 minutes...")

            #timer to wait 15 minutes
            time.sleep(900)

    except KeyboardInterrupt:
        print("\n Pipeline stopped by user")


if __name__ == "__main__":
    auto_pipeline()