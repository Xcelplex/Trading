import pandas as pd
import numpy as np 
import datetime
import plotly as plt
import streamlit as st
import yfinance as yf
from datetime import timedelta, date, time
import plotly.express as px
from prophet import Prophet
import matplotlib.pyplot as plt
from collections import namedtuple

#Initializing
default_Ticker = "MSFT"
today = date.today()
default_Date_Previous = today - timedelta(days=90)
ticker = "MSFT"
start_Date="2021-12-1"
end_Date = "2022-12-1"
st.title("Current Stock Price Information With General Forecast")
st.write("Note: Detailed and more accurate forecast with multiple factors involved with Deep Learning Computations is Available for Premium Customers")
ticker = st.sidebar.text_input("Stock Symbol/Ticker",default_Ticker)
start_Date = st.sidebar.text_input("Start_Date - Date Format(2023-13-3)",default_Date_Previous)
end_Date = st.sidebar.text_input("End_Date - Date Format(2023-13-3)",today)
data= yf.download(ticker,start_Date,end_Date)
#st.write(data2)
fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

#setting start and end date to get the historical view
end_Date = date.today()
start_Date = end_Date - timedelta(days = 90)

#list of tech stocks to get the information (to be altered later)
#tikcer_list = ["MSFT", "AMD", "AAPL", "META", "GOOGL", "NVDA", "PYPL", "AMZN", "INTC", "CRM"]
tempDict = []
#Downloading financial data and storing in the dataframe
df_Data = []

#for i in tikcer_list:
data = yf.download(ticker, start_Date, end_Date)

df = pd.DataFrame(data)
df_Close = pd.DataFrame(data['Close'])
df_Data= pd.DataFrame(data['Close'])
    
    

df_Close.index = df_Close.index.strftime('%Y-%m-%d')
df_Close.insert(0, "Date", df_Close.index, True)
df_Close = df_Close.reset_index(drop = True)
    

df_Data.index = df_Data.index.strftime('%Y-%m-%d')
df_Data.insert(0, "ds", df_Data.index, True)
df_Data = df_Data.reset_index(drop = True)
df_Data = df_Data.rename(columns={"Close": "y"})

df_Close['Close'] = df_Close['Close'].round(4)
    #fig = px.line(df_Close, x = df_Close['Date'], y = data['Close'], title =i)
    #fig
    #st.write(df_Close['Date'])
    #st.write("new")
    #df_Close['Close'] = pd.isnull(df_Close['Close'][i])
    #df_Close['Date'] = pd.isnull(df_Close['Date'][i])
    #df_Close['Date'] = pd.to_datetime(df_Close["Date"], format = "%d-%m-%y")


    #st.write(df_Close['Date'])
    #set_ds = set(df_Close['Date'])
    #set_y = set(df_Close['Close'])
    #df_data = {'ds': set_ds,'y':set_y}
    #s1 = pd.Series(df_Close["Date"])
   # s2 = pd.Series(df_Close["Close"])
    #nt1 = namedtuple("series1",s1.index)(*s1)
    #nt2 = namedtuple("series2",s2.index)(*s2)
    
df_data = {'ds': tuple(df_Close['Date']), 'y':tuple(df_Close['Close'])}

    
m = Prophet(interval_width=0.01, daily_seasonality=True)
model = m.fit(df_Data)
future = m.make_future_dataframe(periods=100,freq='D')
forecast = m.predict(future)
forecast.head()
#st.write(forecast)
    #st.write("Stock Price Forecast")
    #fig = px.line(forecast, x = forecast['ds'], y = forecast['yhat'])

    #fig
st.write("Current Values")
st.write(data)

st.write("Forecasted Values and Trends ")

#st.write(forecast)
forecast = forecast.rename(columns={"ds": "Time/Date"})
forecast = forecast.rename(columns={"yhat": "Closing Price"})
st.write(forecast)
#st.write(forecast)
fig = px.line(forecast, x = forecast['Time/Date'], y = forecast['Closing Price'])
#fig = px.line(df_Close, x = df_Close['Date'], y = data['Close'], title ="Top Tech Stock Trend")
fig
