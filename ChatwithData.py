
import streamlit as st
#import pandasai from PandasAI
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import yfinance as yf
from datetime import date, timedelta, time
import plotly.express as px
import pandas as pd
import openai

#initializing the values in sidebar
default_Ticker = "MSFT"
today = date.today()
default_Date_Weekago = today = timedelta(days = 30)
ticker = "MSFT"
start_Date = "2021-12-1"
end_Date = "2022-12-1"

#taking the input of the values from the side bar
st.title("Chat with your Data - GenAI Powered Data Query Tool")
st.write("Enter the Stock Symbol/Ticker and Period in side bar to start quering the information about the data")
st.write("Currently Only available for Premium Users - Contact us for more information")
ticker= st.sidebar.text_input("Stock Symbol/Ticker", default_Ticker)
start_Date = st.sidebar.text_input("Start_Date - Date Format YYYY-MM-D", start_Date)
end_Date = st.sidebar.text_input("Start_Date - Date Format YYYY-MM-D", end_Date)


#downloading the important data in relation to the input ticker
data_Stock = yf.download(ticker, start_Date, end_Date)
df_Stock= pd.DataFrame(data_Stock)
value = yf.Ticker(ticker)
data_Quarterly_CashFlow = value.quarterly_cashflow
data_Income_Statement = value.income_stmt
data_Share_Value = value.get_shares_full(start= start_Date, end = end_Date)
#data_Share_Value = data_Share_Value.rename(column={"0":"Share Value"})

#converting the downloaded information to data frames
df_Stock= pd.DataFrame(data_Stock)
df_Quarterly_CashFlow = pd.DataFrame(data_Quarterly_CashFlow)
df_Income_Statement = pd.DataFrame(data_Income_Statement)
df_Share_Value = pd.DataFrame(data_Share_Value)

with st.expander("Data Detail Preview"):
    st.write("Stock Data")
    st.write(data_Stock)
    st.write("Quarterly Data")
    st.write(data_Quarterly_CashFlow)
    st.write("Income Statement")
    st.write(data_Income_Statement)
    st.write("data_Share_Value")
    st.write(data_Share_Value)
query = st.text_area("Chat with Financial Data")
st.write(query) 
#fig = px.line(data_Share_Value, x = data_Share_Value.index, y = data_Share_Value, title = "Share Value Trend")
#fig
#LLM API for converting chat to dataframe/pandas commands
#openai.api_key = ("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")
openai.api_key = st.secrets["OpenAI_API_Key"]
llm = OpenAI(openai.api_key)
#llm = OpenAI(api_token=os.environ["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"])
query_engine_Stock  = SmartDataframe(df_Stock, config={"llm":llm})
query_engine_QF = SmartDataframe(df_Quarterly_CashFlow, config={"llm":llm})
query_engine_IS  = SmartDataframe(df_Income_Statement, config={"llm":llm})
query_engine_SV  = SmartDataframe(df_Share_Value, config={"llm":llm})
answer_data = query_engine_Stock.chat(query)
answer_data_QF = query_engine_QF.chat(query)
answer_data_IS = query_engine_IS.chat(query)
answer_data_SV = query_engine_SV.chat(query)
st.write(answer_data)
#st.write(answer_data_QF)

