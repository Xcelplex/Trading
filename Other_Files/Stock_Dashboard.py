import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import datetime 
from datetime import date, timedelta, time
import altair as alt
import plotly as plt
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot,init_notebook_mode
import plotly.figure_factory as ff


default_Ticker = "MSFT"
today = date.today()
default_Date_Weekago = today - timedelta(days=90)
ticker = "MSFT"
start_Date="2021-12-1"
end_Date = "2022-12-1"
#st.title("Current Stock Price Information")
ticker = st.sidebar.text_input("Stock Symbol/Ticker",default_Ticker)
start_Date = st.sidebar.text_input("Start_Date - Date Format(2023-13-3)",default_Date_Weekago)
end_Date = st.sidebar.text_input("End_Date",today)
data= yf.download(ticker,start_Date,end_Date)
#st.write(data2)
fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
ticker_list = ["MSFT","AMD","AAPL","META","GOOGL","NVDA","PYPL","AMZN","INTC","CRM" ]
data = []
tempDict = {}
tempDict_lines = {}
df_Close=[]
df_Data = []
num = 0
for i in ticker_list:
    #st.write(i)
    data= yf.download(i,start_Date,end_Date)

    fig = px.line(data, x=data.index, y=data['Adj Close'], title=i)
    #st.plotly_chart(fig)
    tempDict[i] = data
    #st.line_chart(data = tempDict[i], x = None, y=None)
    df_Close = pd.DataFrame(data['Close'])
    df_Close.rename(columns={'Close':i}, inplace = True)
    #st.write(df_Close)
    df_Data.append(df_Close)
    df_Close= pd.concat(df_Data, axis=1)
    #df_Close.index = pd.to_datetime(df_Close.index)
    df_Close.index = df_Close.index.strftime('%d-%m-%Y')
    


#colors = plt.colors.qualitative.Prism
colors = plt.colors.qualitative.Antique
for template in [ "plotly_dark"]:

    #fig = px.line(df_Close.index, y=df_Close.columns)
    fig = px.bar(df_Close, x=df_Close.index, y=df_Close.columns,color_discrete_sequence=colors,template=template)
    #fig.add_trace(ff.create_table(df_Close.index))
    fig.update_layout(coloraxis = {'colorscale':'viridis'})

fig.show()












