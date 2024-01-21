import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import re
import datetime
from datetime import timedelta, date, time
import streamlit as st
import plotly.express as px
import yfinance as yf
import plotly.figure_factory as ff
import plotly as plt

today = date.today()
date_Diff = today - timedelta(days=364)
start_Date = date_Diff
end_Date = today
#data= yf.download(ticker,start_Date,end_Date)
st.title("Tech Stock Information-Graph")
ticker_list = ["MSFT","AMD","AAPL","META","GOOGL","NVDA","PYPL","AMZN","INTC","CRM" ]
data = []
tempDict = {}
tempDict_lines = {}
df_Close=[]
df_Data = []
num = 0
st.write(df_Close)
for i in ticker_list:
    data= yf.download(i,start_Date,end_Date)
    tempDict[i] = data
    tempDict[i].update(data)
    df_Close = pd.DataFrame(data['Close'])
    df_Close.rename(columns={'Close':i}, inplace = True)
    df_Data.append(df_Close)
    df_Close= pd.concat(df_Data, axis=1)
    df_Close.index = df_Close.index.strftime('%d-%m-%y')

st.write(df_Close.columns.to_list())

colors = plt.colors.qualitative.Antique
for template in [ "plotly_dark"]:

    #fig = px.line(df_Close.index, y=df_Close.columns)
    fig = px.bar(df_Close, x=df_Close.index, y=df_Close.columns,color_discrete_sequence=colors,template=template)
    fig.update_layout(coloraxis = {'colorscale':'viridis'})
    

fig.show()