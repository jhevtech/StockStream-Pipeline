import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_session
from database.models import StockPrice

# Page config
st.set_page_config(
    page_title="StockStream Pipeline",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(ticker):
    """Get stock data for a specific ticker"""
    session = get_session()
    
    results = session.query(StockPrice)\
                    .filter_by(ticker=ticker)\
                    .order_by(StockPrice.timestamp.desc())\
                    .limit(100)\
                    .all()
    
    data = []
    for row in results:
        data.append({
            'timestamp': row.timestamp,
            'open': row.open,
            'high': row.high,
            'low': row.low,
            'close': row.close,
            'volume': row.volume
        })
    
    session.close()
    df = pd.DataFrame(data)
    return df.sort_values('timestamp') if not df.empty else df

@st.cache_data(ttl=300)
def get_all_tickers():
    """Get list of all available tickers"""
    session = get_session()
    tickers = session.query(StockPrice.ticker).distinct().all()
    session.close()
    return sorted([t[0] for t in tickers])

def calculate_change(df):
    """Calculate price change between last two data points"""
    if len(df) < 2:
        return 0, 0
    latest = df.iloc[-1]['close']
    previous = df.iloc[-2]['close']
    change = latest - previous
    change_pct = (change / previous) * 100
    return change, change_pct

# Header
st.title("📈 StockStream Pipeline")
st.markdown("Automated real-time stock data ingestion and visualization")

# Get available tickers
tickers = get_all_tickers()

if not tickers:
    st.error("No data available. Please run the stock fetcher first!")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Stock Selection")
    selected_ticker = st.selectbox("Choose a stock:", tickers)
    
    st.divider()
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Fetch data
df = get_stock_data(selected_ticker)

if df.empty:
    st.warning(f"No data found for {selected_ticker}")
    st.stop()

# Calculate metrics
change, change_pct = calculate_change(df)
latest_price = df.iloc[-1]['close']
avg_volume = df['volume'].mean()

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Current Price",
        value=f"${latest_price:.2f}",
        delta=f"{change_pct:.2f}%"
    )

with col2:
    st.metric(
        label="High (Period)",
        value=f"${df['high'].max():.2f}"
    )

with col3:
    st.metric(
        label="Low (Period)",
        value=f"${df['low'].min():.2f}"
    )

with col4:
    st.metric(
        label="Avg Volume",
        value=f"{avg_volume/1e6:.2f}M"
    )

# Main candlestick chart
st.subheader(f"{selected_ticker} Price Chart")

fig = go.Figure(data=go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name=selected_ticker
))

fig.update_layout(
    title=f'{selected_ticker} Stock Price',
    yaxis_title='Price ($)',
    xaxis_title='Time',
    height=500,
    template='plotly_white',
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, use_container_width=True)

# Two column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Volume Analysis")
    volume_fig = go.Figure(data=go.Bar(
        x=df['timestamp'],
        y=df['volume'],
        marker_color='lightblue'
    ))
    volume_fig.update_layout(
        height=300,
        template='plotly_white',
        showlegend=False
    )
    st.plotly_chart(volume_fig, use_container_width=True)

with col2:
    st.subheader("Price Distribution")
    price_fig = go.Figure(data=go.Histogram(
        x=df['close'],
        nbinsx=20,
        marker_color='lightcoral'
    ))
    price_fig.update_layout(
        height=300,
        template='plotly_white',
        xaxis_title='Price',
        yaxis_title='Frequency'
    )
    st.plotly_chart(price_fig, use_container_width=True)

# Data table
st.subheader("Recent Data Points")
st.dataframe(
    df[['timestamp', 'open', 'high', 'low', 'close', 'volume']].tail(10),
    use_container_width=True,
    hide_index=True
)

# Footer
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total records: {len(df)}")