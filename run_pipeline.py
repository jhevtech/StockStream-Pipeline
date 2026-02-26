from src.ingestion.fetch_stock import fetch_stock_data
from src.database.read import load_latest_data
from src.analysis.dsp import butterworth_filter, compute_fft, dsp_forecast
from datetime import datetime

def run_pipeline():
    print(f"Market Pulse Pipeline Started at {datetime.now()}")

    # Step 1: Ingest new data
    fetch_stock_data()

    # Step 2: Load latest data from DB
    df = load_latest_data()

    # Step 3: Apply DSP
    filtered = butterworth_filter(df['close'])
    freqs, magnitude = compute_fft(df['close'])
    forecast = dsp_forecast(filtered)

    print(f"Pipeline Successfully ran at {datetime.now()}")
    
    return { "df": df, "filtered": filtered,
             "freqs": freqs,
             "magnitude": magnitude,
             "forecast": forecast }

   

if __name__ == "__main__":
    run_pipeline()
