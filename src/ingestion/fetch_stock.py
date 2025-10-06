import yfinance as yf
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_session
from database.models import StockPrice
from ticker_loader import get_sp500_tickers

def fetch_stock_data():
    #get and store stock data
    session = get_session()

    stocks = get_sp500_tickers()
    print(f"Fetching data for {len(stocks)} stocks...")
    for ticker in stocks:
        inserted = 0
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='5d', interval='1h') #get 5 day with hourly 

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
                        open=float(row['Open']),#convert numpy float to python 
                        high=float(row['High']),
                        low=float(row['Low']),
                        close=float(row['Close']),
                        volume=int(row['Volume'])
                    )

                    session.add(stock_price)
                    inserted += 1

                    session.commit()
                    print("Data saved to database!")
            print("Successfully inserted into database")

        except Exception as e:
            print(f"Error: {e}")
            session.rollback()

    session.close()
    
if __name__ == "__main__":
    fetch_stock_data()

