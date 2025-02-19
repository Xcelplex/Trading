import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import time

# Page Config
st.set_page_config(page_title="Live Trading Dashboard", layout="wide")

# Sidebar - Ticker Selection
st.sidebar.write("LIVE TRADING DASHBOARD")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", "AAPL")
update_interval = st.sidebar.slider("Refresh Rate (seconds)", 5, 60, 10)

# Fetch Live Data
def get_live_stock_data(ticker):
    df = yf.download(ticker, period="7d", interval="5m")  # 5-minute interval data
    df['SMA'] = df['Close'].rolling(window=20).mean()
    df['EMA'] = df['Close'].ewm(span=10, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    df['BB_Upper'] = df['BB_Middle'] + (df['Close'].rolling(window=20).std() * 2)
    df['BB_Lower'] = df['BB_Middle'] - (df['Close'].rolling(window=20).std() * 2)
    
    # MACD
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    return df

# **Live Data Loop**
while True:
    st.subheader(f"LIVE STOCK ANALYSIS: {ticker}")

    # Fetch Data
    df = get_live_stock_data(ticker)

    if not df.empty:
        # **Live Candlestick Chart**
        st.write("LIVE CANDLESTICK CHART WITH INDICATORS")
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

        fig.update_layout(title=f"Live {ticker} Stock Price with Indicators", xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # **Live MACD Chart**
        st.write("LIVE MACD INDICATOR")
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name="MACD", line=dict(color='purple')))
        macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name="Signal Line", line=dict(color='red')))
        
        macd_fig.update_layout(title="Live MACD & Signal Line", xaxis_title="Date", yaxis_title="MACD Value")
        st.plotly_chart(macd_fig, use_container_width=True)

        # **Live RSI Chart**
        st.write("LIVE RSI INDICATOR")
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name="RSI", line=dict(color='blue')))
        
        # RSI Overbought & Oversold Levels
        rsi_fig.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Overbought (70)")
        rsi_fig.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Oversold (30)")
        
        rsi_fig.update_layout(title="Live Relative Strength Index (RSI)", xaxis_title="Date", yaxis_title="RSI Value")
        st.plotly_chart(rsi_fig, use_container_width=True)

        # **Live Volume Chart**
        st.write("LIVE TRADING VOLUME")
        volume_fig = go.Figure()
        volume_fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='blue'))
        
        volume_fig.update_layout(title="Live Trading Volume", xaxis_title="Date", yaxis_title="Volume")
        st.plotly_chart(volume_fig, use_container_width=True)

        # Show Live Data
        st.write("LATEST STOCK DATA")
        st.dataframe(df.tail())

    else:
        st.error("No live data available. Please check the stock ticker.")

    # **Auto Refresh**
    time.sleep(update_interval)
    st.rerun()
