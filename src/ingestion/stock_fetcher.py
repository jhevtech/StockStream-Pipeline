import yfinance as yf
import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_session
from database.models import StockPrice

class StockFetcher:
    # fetches real time stock data using yfinance and store in postgresql

    def __init__(self, tickers=None):
        self.tickers = tickers or ['AAPL', 'GOOGL', 'MSFT', 'TSLA'] #initialize with default tickers with custom list

    #get and store in db
    def fetch_and_store(self, period='1d', interval='15m'): 
        session = get_session()
        total_inserted = 0

        print(f"Fetching {interval} data for {len(self.tickers)} stocks...")

        for ticker in self.tickers:

            inserted_count = 0
            try:
                print(f"Processing {ticker}...")

                stock = yf.Ticker(ticker)
                data = stock.history(period=period, interval=interval)

                if data.empty:
                    print(f"No data available for {ticker}")
                    continue

            #store each time period
                
                for timestamp, row in data.iterrows():
                    #check if record already exists
                    existing = session.query(StockPrice).filter_by(
                        ticker=ticker,
                        timestamp=timestamp.to_pydatetiem()
                    ).first()

                    if not existing:
                        stock_price = StockPrice(
                            ticker=ticker,
                            timestamp=timestamp.to_pydatetime() ,
                            open=float(row['Open']),
                            high=float(row['High']), 
                            low=float(row['Low']),
                            close=float(row['Close']),
                            volume=int(row['Volume'])
                        )
                            
                    session.add(stock_price)
                    inserted_count += 1

                # Commit after each ticker
                    session.commit()
                    total_inserted += inserted_count
                    print(f"{ticker}: {inserted_count} new records inserted")
                
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                session.rollback()
    
        session.close()
        print(f"\n Pipeline completed! Total records inserted: {total_inserted}")
        return total_inserted
    
    def get_latest_data(self, ticker, limit=10):
        #Get latest stored data for a ticker
        session = get_session()
        
        try:
            query = session.query(StockPrice)\
                          .filter_by(ticker=ticker)\
                          .order_by(StockPrice.timestamp.desc())\
                          .limit(limit)
            
            results = query.all()
            
            # Convert to DataFrame
            data = [{
                'ticker': row.ticker,
                'timestamp': row.timestamp,
                'open': row.open,
                'high': row.high,
                'low': row.low,
                'close': row.close,
                'volume': row.volume
            } for row in results]
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Error retrieving {ticker} data: {e}")
            return pd.DataFrame()
        finally:
            session.close()

def main():    
    # Popular tech stocks for test
    tech_stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    
    print("=== Market Pulse Data Ingestion ===")
    print(f"Timestamp: {datetime.now()}")
    
    # Initialize fetcher
    fetcher = StockFetcher(tickers=tech_stocks)
    
    # Fetch today's data with 15-minute intervals  
    records_inserted = fetcher.fetch_and_store(period='1d', interval='15m')
    
    if records_inserted > 0:
        print("\n Sample of latest AAPL data:")
        sample_data = fetcher.get_latest_data('AAPL', limit=5)
        print(sample_data.head())
    else:
        print(" No new data inserted (might already be up to date)")

if __name__ == "__main__":
    main()              


