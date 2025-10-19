import yfinance as yf
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_session
from database.models import StockPrice
from ingestion.ticker_loader import get_sp500_tickers

# to calculate metrics
import logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/pipeline.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_stock_data():
    #get and store stock data
    session = get_session()
    stocks = get_sp500_tickers()
    #print(f"Fetching data for {len(stocks)} stocks...")

    inserted = 0
    total_errors = 0

    for ticker in stocks:

        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='5d', interval='1h') #get 5 day with hourly

            inserted += inserted
            logging.info(f"Success: {ticker} - {inserted} records")

            if data.empty:
                print(f"No data returned for {ticker}")
                continue

            print(f"Got {len(data)} records for {ticker}")

            for timestamp, row in data.iterrows():
                #check if already existed
                existing = session.query(StockPrice).filter_by(
                    ticker=ticker,
                    timestamp=timestamp.to_pydatetime()
                ).first()
                #add if not there
                if not existing:
                    #create new stock record
                    stock_price = StockPrice(
                        ticker=ticker,
                        timestamp=timestamp.to_pydatetime(),#converting pandas timestamp
                        open=round(float(row['Open']),3),#convert numpy float to python 
                        high=round(float(row['High']),3),
                        low=round(float(row['Low']),3),
                        close=round(float(row['Close']),3),
                        volume=int(row['Volume'])
                    )

                    session.add(stock_price)
                    inserted += 1

                    session.commit()
                    print("Data saved to database!")
            print("Successfully inserted into database")

        except Exception as e:
            print(f"Error: {e}")
            total_errors += 1
            logging.error(f"Failed: {ticker} - {e}")
            session.rollback()

    total_inserted = int(inserted / 35)
    success_rate = (len(stocks) - total_errors) / len(stocks) * 100
    logging.info(f"Pipeline Completed - Total: {total_inserted}, Errors: {total_errors}, Success Rate: {success_rate}%")
    print(f"Total inserted: {total_inserted}, \nErrors: {total_errors}, \nSuccess Rate: {success_rate:.1f}%")
    session.close()
    
if __name__ == "__main__":
    fetch_stock_data()

