import pandas as pd
import os


def get_sp500_tickers():
    """Get top 50 most traded stocks - static list"""
    
    try:
        csv_path = os.path.join('data', 'sp500_stocks.csv')

        df = pd.read_csv(csv_path)

        if 'Symbol' in df.columns:
            tickers = df['Symbol'].tolist()
        elif 'Ticker' in df.columns:
            tickers = df['Ticker'].tolist()
        else: 
            print(f"Available columns: {df.columns.tolist()}")
            raise ValueError("Could not find ticker column")
        
        print(f"Loaded {len(tickers)} tickers from CSV")
        return tickers

    except Exception as e:
        print(f"Error loading tickers from CSV: {e}")
        print("Falling back to static list of top 50 tickers")

        tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'LLY', 'V',
            'JPM', 'UNH', 'XOM', 'MA', 'AVGO', 'HD', 'PG', 'JNJ', 'COST', 'ABBV',
            'ORCL', 'MRK', 'CVX', 'KO', 'NFLX', 'BAC', 'CRM', 'AMD', 'PEP', 'TMO',
            'ADBE', 'WMT', 'ACN', 'MCD', 'CSCO', 'ABT', 'LIN', 'DIS', 'INTC', 'NKE',
            'DHR', 'TXN', 'VZ', 'PM', 'CMCSA', 'WFC', 'QCOM', 'UPS', 'IBM', 'HON'
        ]

        return tickers
    

