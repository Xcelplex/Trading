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
st.write(df_Close)
for i in ticker_list:
    data= yf.download(i,start_Date,end_Date)
    fig = px.line(data, x=data.index, y=data['Adj Close'], title=i)
    tempDict[i] = data
    tempDict[i].update(data)
    df_Close = pd.DataFrame(data['Close'])
    df_Close.rename(columns={'Close':i}, inplace = True)
    df_Data.append(df_Close)
    df_Close= pd.concat(df_Data, axis=1)
    df_Close.index = df_Close.index.strftime('%d-%m-%y')

st.write(df_Close.columns.to_list())
#st.write(df_Close.columns.to)

fig = make_subplots(
    rows = 2, cols =1,
    shared_xaxes = True,
    vertical_spacing = 0.04,
    specs = [[{"type": "scatter"}], 
            [{"type": "table"}],
]
)


fig.add_trace(
    go.Scatter( x=df_Close.index,
           y = df_Close.columns,
           mode="markers",
           name = "Stock Info"

    ),
    row= 1, col = 1


)
fig.add_trace(
    
    go.Table(
                               header=dict(values=[ df_Close.columns.tolist()]), 
                               cells=dict(values=[ df_Close]),
    row=2, col=1
)
)
'''

fig.add_trace(
    st.write(df_Close),
    row=2, col=1
)
'''



#####################Section to be comlpleted after getting the correct parameters
'''
fig.add_trace(
    go.Table(
        df_Close,x=df_Close.index, y=df_Close.columns,color_discrete_sequence=colors,template=template
    )
)
'''
######################
fig.update_layout(
    height = 500,
    showlegend = False,
    title_text = "Tech Stocks Information"
)
fig.show()
