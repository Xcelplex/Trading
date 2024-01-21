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
import plotly.graph_objects as go
from plotly.offline import iplot,init_notebook_mode
from plotly.subplots import make_subplots


today = date.today()
date_Diff = today - timedelta(days=364)
start_Date = date_Diff
end_Date = today
#data= yf.download(ticker,start_Date,end_Date)
st.title("Tech Stock Information")
ticker_list = ["MSFT","AMD","AAPL","META","GOOGL","NVDA","PYPL","AMZN","INTC","CRM" ]
data = []
tempDict = {}
tempDict_lines = {}
df_Close=[]
df_Data = []
num = 0
for i in ticker_list:
    data= yf.download(i,start_Date,end_Date)
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=i)
    tempDict[i] = data
    df_Close = pd.DataFrame(data['Close'])
    df_Close.rename(columns={'Close':i}, inplace = True)
    df_Data.append(df_Close)
    df_Close= pd.concat(df_Data, axis=1)
    df_Close.index = df_Close.index.strftime('%d-%m-%Y')
    

st.write(df_Close)
#colors = plt.colors.qualitative.Prism

colors = plt.colors.qualitative.Antique
for template in [ "plotly_dark"]:

    #fig = px.line(df_Close.index, y=df_Close.columns)
    #fig = px.area(df_Close, x=df_Close.index, y=df_Close.columns,color_discrete_sequence=colors,template=template)
    fig = px.bar(df_Close,x=df_Close.index, y=df_Close.columns,color_discrete_sequence=colors,template=template)
    fig.update_layout(coloraxis = {'colorscale':'viridis'},margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="Black",)

fig.show()

























