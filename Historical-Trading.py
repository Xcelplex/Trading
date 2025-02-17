import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Trading Dashboard", layout="wide")

# Sidebar - Ticker Selection
st.sidebar.write("TRADING DASHBOARD")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL")
date_range = st.sidebar.slider("Select Date Range", 10, 365, 60)
sma_window = st.sidebar.slider("SMA Window", 5, 50, 20)
ema_window = st.sidebar.slider("EMA Window", 5, 50, 10)
macd_short = st.sidebar.slider("MACD Short Window", 5, 50, 12)
macd_long = st.sidebar.slider("MACD Long Window", 10, 100, 26)
macd_signal = st.sidebar.slider("MACD Signal Window", 5, 50, 9)
rsi_window = st.sidebar.slider("RSI Window", 5, 50, 14)

# Fetch Data
def get_stock_data(ticker, days):
    df = yf.download(ticker, period=f"{days}d")
    df['SMA'] = df['Close'].rolling(window=sma_window).mean()
    df['EMA'] = df['Close'].ewm(span=ema_window, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    df['BB_Upper'] = df['BB_Middle'] + (df['Close'].rolling(window=20).std() * 2)
    df['BB_Lower'] = df['BB_Middle'] - (df['Close'].rolling(window=20).std() * 2)
    
    # MACD
    df['MACD'] = df['Close'].ewm(span=macd_short, adjust=False).mean() - df['Close'].ewm(span=macd_long, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=macd_signal, adjust=False).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

# Main Content
st.subheader(f"STOCK ANALYSIS: {ticker}")

# Fetch Data
df = get_stock_data(ticker, date_range)

if not df.empty:
    # **Candlestick Chart with Indicators**
    st.write("CANDLESTICK CHART WITH INDICATORS")
    fig = go.Figure()
    
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name="Candlestick"
    ))
    
    # SMA & EMA
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], mode='lines', name="SMA", line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines', name="EMA", line=dict(color='orange')))
    
    # Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], mode='lines', name="Bollinger Upper", line=dict(color='gray', dash='dot')))
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], mode='lines', name="Bollinger Lower", line=dict(color='gray', dash='dot')))

    fig.update_layout(title=f"{ticker} Stock Price with Indicators", xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # **MACD Chart**
    st.write("MACD INDICATOR")
    macd_fig = go.Figure()
    macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name="MACD", line=dict(color='purple')))
    macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name="Signal Line", line=dict(color='red')))
    
    macd_fig.update_layout(title="MACD & Signal Line", xaxis_title="Date", yaxis_title="MACD Value")
    st.plotly_chart(macd_fig, use_container_width=True)

    # **RSI Chart**
    st.write("RSI INDICATOR")
    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name="RSI", line=dict(color='blue')))
    
    # RSI Overbought & Oversold Levels
    rsi_fig.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Overbought (70)")
    rsi_fig.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Oversold (30)")
    
    rsi_fig.update_layout(title="Relative Strength Index (RSI)", xaxis_title="Date", yaxis_title="RSI Value")
    st.plotly_chart(rsi_fig, use_container_width=True)

    # **Volume Bar Chart**
    st.write("TRADING VOLUME")
    volume_fig = go.Figure()
    volume_fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='blue'))
    
    volume_fig.update_layout(title="Trading Volume", xaxis_title="Date", yaxis_title="Volume")
    st.plotly_chart(volume_fig, use_container_width=True)

    # Show Data
    st.write("RECENT DATA")
    st.dataframe(df.tail())

else:
    st.error("No data found. Please enter a valid stock ticker.")

# Custom Styling
st.markdown(
    """
    <style>
    .stSidebar {background-color: 3e3f40;}
    </style>
    """,
    unsafe_allow_html=True
)

