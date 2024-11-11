import numpy as np
import pandas as pd
import streamlit as st 
import plotly.express as px
import yfinance as yf
import datetime
from datetime import timedelta, date, time
import altair as alt
import plotly as plt
import plotly.graph_objects as go
import os
from openai import OpenAI 
from langchain.agents import AgentType, initialize_agent
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nixtla import NixtlaClient



#Setting API Keys 
nixtla_client = NixtlaClient(api_key = "nixak-D2Wuj7TvEPvUFA6KT9vR9kwyNysYEGQjvDbvkQ8hYHNTcDBSsA255FWc9aEJhc1y7qi5wz93OJzWvYmn")

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Date", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'



st.set_page_config(
    page_title = "Tech Financial Dashboard",
    layout = "wide",
    initial_sidebar_state="expanded"
    )
alt.themes.enable("dark")

default_Ticker = "MSFT"
today = datetime.date.today()
date_Diff = today - datetime.timedelta(days = 364)
start_Date = date_Diff
end_Date = today
temp_Dict = {}
df_Data = []
df_Close=[]
data_Stock = []
df_Revenue_Data = []
df_Q_Revenue_Data=[]

#ticker_List = ["AMD","MSFT","AAPL","META","GOOGL","NVDA","PYPL","AMZN","INTC","CRM" ]

with st.sidebar:
    st.title('Company Financial Dashboard')
    ticker = st.sidebar.text_input("Stock Symbol/Ticker", default_Ticker)
    data_Stock = yf.download(ticker, start_Date, end_Date)

#######leaving this list option as it is and adding only one ticker for now, incase a default view is required in future for multiple tickers """"""""""
ticker_List = [ticker]
for i in ticker_List:

    value = yf.Ticker(i)
    data_Incm = value.income_stmt
    data_Stock = yf.download(i, period="1mo")
    data_Quarterly_Incm = value.quarterly_income_stmt
    data_balancesheet= value.balance_sheet
    data_news = value.news


    #####Converting data downloaded to dataframes to use in graphs##############
    df_Incm = pd.DataFrame(data_Incm)
    df_Stock= pd.DataFrame(data_Stock)
    df_Quarterly_Incm = pd.DataFrame(data_Quarterly_Incm)
    data_Revenue = df_Incm.loc['Total Revenue']
    df_Revenue = pd.DataFrame(data_Revenue)
    df_Revenue.index = df_Revenue.index.strftime('%Y')
    df_Revenue.index = pd.to_datetime(df_Revenue.index)
    df_Revenue.rename(columns={'Total Revenue':i}, inplace = True)
    df_Revenue_Data.append(df_Revenue)
    df_Revenue = pd.concat(df_Revenue_Data, axis = 1)


    #Extracting Stock Price Information
    df_Close = pd.DataFrame(data_Stock['Close'])
    df_Close.rename(columns={'Close':i}, inplace = True)
    df_Data.append(df_Close)
    df_Close = pd.concat(df_Data, axis = 1)


    #Extracting Quarterly Revenue Information
    data_Quarterly_Revenue = df_Quarterly_Incm.loc['Total Revenue']
    df_Quarterly_Revenue = pd.DataFrame(data_Quarterly_Revenue)
    df_Quarterly_Revenue.index = df_Quarterly_Revenue.index.strftime('%Y')
    df_Quarterly_Revenue.index = pd.to_datetime(df_Quarterly_Revenue.index)
    df_Quarterly_Revenue.rename(columns={'Total Revenue':i}, inplace = True)
    df_Q_Revenue_Data.append(df_Quarterly_Revenue)
    df_Q_Revenue = pd.concat(df_Q_Revenue_Data, axis=1)

    #GenAI based Stock Price Forecast
    data_GenAI_Stock = yf.download(i, period = "1mo")
    df_GenAI_Stock = pd.DataFrame(data_GenAI_Stock['Close'])
    df_GenAI_Stock.rename(columns={'Close':'value'}, inplace = True)
    df_GenAI_Stock.reset_index(inplace= True)
    #timegpt_fcst_df_stock = nixtla = nixtla_client.forecast(df=df_GenAI_Stock, h=3500, freq = 'H', time_col = 'Date', target_col = 'value')
    #nixtla_client.plot(df,timegpt_fcst_df_stock, time_col = 'Date', target_col = 'value')

    #GenAI based Quarterly Revenue Forecast 
    data_GenAI_QRev = yf.download(i, period = "1mo")
    df_GenAI_QRev = pd.DataFrame(data_GenAI_QRev['Close'])
    df_GenAI_QRev.rename(columns={'Close':'value'}, inplace = True)
    df_GenAI_QRev.reset_index(inplace= True)
    #timegpt_fcst_df_QRev = nixtla = nixtla_client.forecast(df=df_GenAI_QRev, h=12, freq = 'MS', time_col = 'Date', target_col = 'value')
    
    #GenAI based Yearly Revenue Forecast
    data_GenAI_YRev = yf.download(i, period = "1mo")
    df_GenAI_YRev = pd.DataFrame(data_GenAI_YRev['Close'])
    df_GenAI_YRev.rename(columns={'Close':'value'}, inplace = True)
    df_GenAI_YRev.reset_index(inplace= True)
    #timegpt_fcst_df_YRev = nixtla = nixtla_client.forecast(df=df_GenAI_YRev, h=36, freq = 'MS', time_col = 'Date', target_col = 'value', model = 'timegpt-1-long-horizon')

    #GenAI Based Advanced Level Forecast
    news_Ticker= yf.Ticker(i)
    News = news_Ticker.news
    #st.write(News)
    data_News =[0]

    for i in range(len(News)):
        df_News = News[i]['title']
        data_News.append(df_News)

    df = pd.DataFrame(data_News, columns = ['News'])
    df = df.drop([0])
    df.to_csv("News.csv", header= ['News'])
    df['title']= df['News']
    df['description'] = df['News']

    analyzer = SentimentIntensityAnalyzer()
    negative = []
    neutral = []
    positive = []
    sA_News = []
    adata = []

    for n in range(df.shape[0]):
        title = df.iloc[n,1]
        description = df.iloc[n, 2]
        title_analyzed = analyzer.polarity_scores(title)
        description_analyzed = analyzer.polarity_scores(description)
        negative.append(((title_analyzed['neg']) + (description_analyzed['neg']))/2)
        neutral.append(((title_analyzed['neu']) + (description_analyzed['neu'])) / 2)
        positive.append(((title_analyzed['pos']) + (description_analyzed['pos'])) / 2)



        df_negative = pd.DataFrame(negative, columns = ["Values"])
        df_neutral = pd.DataFrame(neutral, columns = ["Values"])
        df_positive = pd.DataFrame(positive, columns = ["Values"])



        df["Negative"] = df_negative["Values"]
        df["Neutral"] = df_neutral["Values"]
        df["Positive"] = df_positive["Values"]




        if(df["Negative"].mean() > df["Positive"].mean()):  
            if(df["Negative"].mean() > 0.1):
                SA_News = 0.2 # allocating the value in negetive sentiment 
                #Sentiment Analytics, range from 0-3, with 0 being extreme bearish and 3 being extreme bullish
                #SA = 1
                Ex_Severity = 0.001
                #percentage increase/decline in market share in past one year
                #pct_i_mk_sh = 
                Factors = (SA_News*(Ex_Severity)) 

            else:
                SA_News = 0.4 # value with lesser severity
                #Sentiment Analytics, range from 0-3, with 0 being extreme bearish and 3 being extreme bullish
                #SA = 1
                Ex_Severity = 0.001
                #percentage increase/decline in market share in past one year
                #pct_i_mk_sh = 
                Factors = (SA_News*(Ex_Severity)) 

        else:
            if(df["Positive"].mean() > 0.1):
                SA_News = 1.4 #allocating the value in positive sentiment 
                #Sentiment Analytics, range from 0-3, with 0 being extreme bearish and 3 being extreme bullish
                #SA = 1
                Ex_Severity = 0.001
                #percentage increase/decline in market share in past one year
                #pct_i_mk_sh = 
                Factors = (SA_News*(Ex_Severity)) 

            else: 
                SA_News = 1.2
                #Sentiment Analytics, range from 0-3, with 0 being extreme bearish and 3 being extreme bullish
                #SA = 1
                Ex_Severity = 0.001
                #percentage increase/decline in market share in past one year
                #pct_i_mk_sh = 
                Factors = (SA_News*(Ex_Severity)) 
                sA_News.append(Factors)
                
        #adata[["Negative","Neutral","Positive"]] = df[["Negative","Neutral","Positive"]].copy()
        df_SA_News = pd.DataFrame(sA_News, columns=["Values"])
        df["SA_News"] = df_SA_News["Values"]
    



    Date = datetime.date.today()
    date_Value = [Date]

    #reversing the order of the dataframe from top down to bottom to top
    #setting the time range of 62 days for the time being 
    for i in range(62):
        date_Value_Tmp = Date - timedelta(i+1)
        date_Value.append(date_Value_Tmp)
    date_Value_DF = pd.DataFrame(date_Value, columns = ["ds"])
    date_Value_DF=date_Value_DF.iloc[::-1].reset_index(drop=True)
    date_Value_DF['ds'] = pd.to_datetime(date_Value_DF['ds'])
    #st.write(date_Value_DF)


    #extracting the data from past 2 Months in consistent with 62 Days time frame specified above
    #naming the columns and adding unique_id column as required by TimeGPT Model 
    adata_GenAI = yf.download("AAPL", period ="2Mo")
    adata_GenAI = pd.DataFrame(adata_GenAI["Close"])
    df["Date"]  = Date
    df.set_index('Date')
    df['Date'] = pd.to_datetime(df['Date'])
    df_TimeGPT = pd.merge(adata_GenAI,df,on='Date',how='left').fillna(0)
    df_TimeGPT['unique_id'] = "XCEL"

    #lower score column names title and description corresponds to the fields extracted from yfinance
    #Concatinating two tables
    df_TimeGPT = pd.concat([df_TimeGPT, pd.DataFrame([df_TimeGPT.iloc[-1]])], ignore_index=True)
    row_Index = len(df_TimeGPT) -1
    df_TimeGPT.loc[len(df_TimeGPT)-1,"Date"] =  df.loc[1,"Date"]
    df_TimeGPT.loc[len(df_TimeGPT)-1,"SA_News"] = df.loc[1,"SA_News"]

    #getting the mean values from the columns, then calculating the average of those columns and then adding that to SA_News of the column.
    #Diving it by factor .02 (common denominator value extracted from the columns of SA_News)
    df_TimeGPT.loc[len(df_TimeGPT)-1,"Close"]=df_TimeGPT.loc[len(df_TimeGPT)-1, "Close"] + (df_TimeGPT.loc[len(df_TimeGPT)-1,"Close"]*df_TimeGPT.loc[len(df_TimeGPT)-1,"SA_News"]*2)
    df_TimeGPT_NCol = df_TimeGPT.drop(columns = ["News", "title","description"])
    df_TimeGPT_NCol = df_TimeGPT_NCol[['unique_id','Date','Close','SA_News','Negative','Neutral','Positive']]
    df_TimeGPT_NCol_Avg = np.around(np.mean( np.nanmean(df[['SA_News','Negative', 'Neutral', 'Positive']], axis=0),axis =0), decimals = 4)

    ##lower score column names title and description corresponds to the fields extracted from yfinance
    df_TimeGPT_Tmp = df_TimeGPT.drop(columns=["News","title", "description"])
    df[['Date']] = df_TimeGPT.iloc[-1]['Date']
    #getting the last value of the Close column by using iloc[-1], iloc[0] corresponds to the top most value
    df[['Close']] = df_TimeGPT_Tmp.iloc[-1][['Close']]
    df_TimeGPT_Ex = df.drop(columns = ["News", "title","description"])
    df_TimeGPT_Ex['unique_id'] = "XCEL"
    df_TimeGPT_Ex = df_TimeGPT_Ex[['unique_id','Date','Close','SA_News','Negative','Neutral','Positive']]

    #calculating the average values from 
    df_TimeGPT_NCol.loc[len(df_TimeGPT_NCol)-1,'Negative'] = df_TimeGPT_NCol_Avg
    df_TimeGPT_NCol.rename(columns={'Close': 'y', 'Date': 'ds', 'SA_News': 'Exogenous1', 'Negative': 'Exogenous2'}, inplace=True)
    df_TimeGPT_Data = df_TimeGPT_NCol.drop(columns=["Neutral","Positive"])

    ##merging previously extracted date_Value_DF with df_TimeGPT_Data to eliminate inconsistent interval issue while running timeGPT forecast
    df_TimeGPT_Nex_Data = pd.merge(date_Value_DF,df_TimeGPT_Data, on='ds',how='left').fillna(0)
    df_TimeGPT_Nex_Data['unique_id'] = "XCEL"
    df_TimeGPT_Nex_Data = df_TimeGPT_Nex_Data[['unique_id','ds','y','Exogenous1','Exogenous2']]

    #updating the 0 values for weekends with last weekday value
    #yfinance gives no dates and values for weekend. SO, updating the information with closing price of Friday on weekends
    for i in range(len(df_TimeGPT_Nex_Data)):
        
        if i == 0:
            df_TimeGPT_Nex_Data.loc[i,'y'] = df_TimeGPT_Nex_Data.loc[i+2,'y']
        elif df_TimeGPT_Nex_Data.loc[i]['y'] == 0:
            df_TimeGPT_Nex_Data.loc[i,'y'] = df_TimeGPT_Nex_Data.loc[i-1,'y']
    df_Constant_Val1 = df_TimeGPT_Nex_Data.loc[len(df_TimeGPT_Nex_Data)-1,'Exogenous1']
    df_Constant_Val2 = df_TimeGPT_Nex_Data.loc[len(df_TimeGPT_Nex_Data)-1,'Exogenous2']

    for i in range(len(df_TimeGPT_Nex_Data)):
        df_TimeGPT_Nex_Data.loc[i,'Exogenous1'] = df_TimeGPT_Nex_Data.loc[i]['y']*(df_Constant_Val1*.1)
        df_TimeGPT_Nex_Data.loc[i,'Exogenous2'] = df_TimeGPT_Nex_Data.loc[i]['y']*(df_Constant_Val2*.1)


    #getting the y columns dropped from the table and generating a new table only with exogenous values as per TimeGPT Model
    df_TimeGPT_Nex_Data_NY = df_TimeGPT_Nex_Data.drop(columns = ["y"])




st.title('CURRENT FINANCIAL STATS')
col1 = st.columns((5,5,5,5,5), gap = 'medium' )

with col1[0] : 
    #########Yearly Revenue Loss/Gain ##################################
    st.markdown('YEARLY REVENUE')
    yoy_Return = ((df_Revenue[ticker].iloc[0]-df_Revenue[ticker].iloc[1])/df_Revenue[ticker][0])*100
    formated_YRevenue = format_number(df_Revenue[ticker].iloc[0]) 
    yoy_Return = round(yoy_Return, 2)
    st.metric(label= ticker, value = formated_YRevenue, delta = yoy_Return)
with col1[1]:
    #######Quarterly Gain/Loss Information###########################
    st.markdown('QUARTERLY REVENUE')
    qoq_Return = ((df_Q_Revenue[ticker].iloc[0]-df_Q_Revenue[ticker].iloc[1])/df_Q_Revenue[ticker][1])*100
    formated_QRevenue = format_number(df_Q_Revenue[ticker].iloc[0])
    qoq_Return = round(qoq_Return, 2)
    st.metric(label = ticker, value = formated_QRevenue, delta = qoq_Return)
with col1[2]:
    #################Stock Price Information#################
    #st.subheader('Stock Price')
    st.markdown('STOCK PRICE')
    stock_Price = df_Close[ticker].iloc[0]
    stock_Price = round(stock_Price, 2)
    stock_Price_GL = ((df_Close[ticker].iloc[1] - df_Close[ticker].iloc[0])/df_Close[ticker][0])*100
    stock_Price_GL = round(stock_Price_GL,2)
    label_SP = f'{stock_Price_GL}%'
    st.metric(label = ticker, value = stock_Price, delta = label_SP )
with col1[3]:
    st.markdown('Company Performance')
    company_Performance = (df_Incm.iloc[:,0].loc['EBITDA']/df_Incm.iloc[:,0].loc['Total Revenue'])*100
    #st.write(company_Performance)
    if (company_Performance < 10):
            st.subheader('OK')
    if (company_Performance > 10 and company_Performance < 30):
        st.subheader('GOOD')
    else:
        st.subheader('VERY GOOD')
with col1[4]:
    st.markdown('Company Confidence')
    company_Rev_F1 = ((df_Revenue.iloc[:,0].iloc[0]-df_Revenue.iloc[:,0].iloc[1])/df_Revenue.iloc[:,0].iloc[1])*100
    company_Rev_F2 = ((df_Revenue.iloc[:,0].iloc[1]-df_Revenue.iloc[:,0].iloc[2])/df_Revenue.iloc[:,0].iloc[2])*100
    company_Rev_F3 = ((df_Revenue.iloc[:,0].iloc[1]-df_Revenue.iloc[:,0].iloc[2])/df_Revenue.iloc[:,0].iloc[2])*100
    company_Rev_AV = (company_Rev_F1 + company_Rev_F2 +company_Rev_F3)/3
    company_Per_F4 = (df_Incm.iloc[:,0].loc['EBITDA']/df_Incm.iloc[:,0].loc['Total Revenue'])*100
    company_Per_F5 = (df_Incm.iloc[:,1].loc['EBITDA']/df_Incm.iloc[:,1].loc['Total Revenue'])*100
    company_Per_F6 = (df_Incm.iloc[:,2].loc['EBITDA']/df_Incm.iloc[:,2].loc['Total Revenue'])*100
    company_Per_AV = (company_Per_F4 + company_Per_F5 +company_Per_F6)/3

    if (company_Rev_AV < 0 and company_Per_AV < 10):
        st.subheader('Average')
    if (company_Rev_AV > 0 and company_Per_AV > 10 and company_Per_AV < 30):
        st.subheader('High')
    if (company_Rev_AV < 0 and company_Per_AV > 10 and company_Per_AV < 30):
        st.subheader('High')
    if (company_Rev_AV > 10 and company_Per_AV > 30):
        st.subheader('Very High')
    if (company_Rev_AV < 10 and company_Per_AV > 30):
        st.subheader('Very High')
    

st.markdown('---')

col2 = st.columns(( 5,5), gap = 'medium')

with col2[0]:

    st.markdown("STOCK PERFORMANCE (1 MONTH INTERVAL)")
    #colors1 = plt.colors.qualitative.Antique
    colors1 = plt.colors.qualitative.Pastel
    colors2 = plt.colors.qualitative.T10
    colors = plt.colors.qualitative.D3

    #colors1 = "rgb(251,128,114)"

    fig2 = px.bar(df_Close, df_Close.index, df_Close.columns, color_discrete_sequence=colors1)
    fig2.layout.width = 700
    fig2.layout.height = 400
    
    fig2
    ############Pie Chart for Gross Profit and EBITDA#########################    
    st.markdown("QUARTERLY REVENUE TREND")
    fig4 = px.area(df_Quarterly_Incm, df_Quarterly_Incm.loc['Total Revenue'], y = df_Quarterly_Incm.columns,color_discrete_sequence=colors2)
    fig4.update_layout(coloraxis = {'colorscale':'viridis'})
    fig4.layout.width = 700
    fig4.layout.height = 350
    fig4

    
    
    
with col2[1]:

    st.markdown('YEARLY REVENUE BREAKDOWN')
    value_Ticker = yf.Ticker(ticker)
    data_Incm_Ticker = value_Ticker.income_stmt
    df_Incm_Ticker = pd.DataFrame(data_Incm_Ticker)
    #st.write(df_Incm_MSFT)
    labels = ['Gross Profit','Cost of Revenue', 'EBITDA']
    values = [df_Incm_Ticker.iloc[:,0].loc["Gross Profit"], df_Incm_Ticker.iloc[:,0].loc["Cost Of Revenue"],df_Incm_Ticker.iloc[:,0].loc["EBITDA"]]
    fig3 = px.pie(df_Incm_Ticker, values = values, names = labels, color_discrete_sequence= px.colors.sequential.Darkmint_r )
    fig3.layout.width = 700
    fig3.layout.height = 400
    fig3
    

    st.markdown("REVENUE TREND (3 YEAR INTERVAL)")
    fig1 = px.line(df_Revenue, df_Revenue.index, y = df_Revenue.columns,color_discrete_sequence=colors1)
    fig1.update_layout(coloraxis = {'colorscale':'viridis'})
    fig1.layout.width = 700
    fig1.layout.height = 350
    fig1


st.markdown('---')

#st.title('GenAI Based Advanced Level Company Performance Forecast')
st.markdown("GENAI BASED ADVANCED LEVEL COMPANY PERFORMANCE")
col4 = st.columns((7,20,3), gap = 'medium')
with col4[0]:
    st.markdown("Company Performance Forecast")
with col4[1]:
    timegpt_Fcst_Ex = nixtla_client.forecast(df=df_TimeGPT_Nex_Data, X_df=df_TimeGPT_Nex_Data_NY, h=63, level=[80, 90])
    fig8 = nixtla_client.plot(
        df_TimeGPT_Nex_Data[['unique_id', 'ds', 'y']], 
        timegpt_Fcst_Ex, 
        max_insample_length=365, 
        level=[80, 90], 
    )
    fig8
st.markdown("---")    

col5 = st.columns((7,20,3), gap = 'medium')
with col5[1]:
    st.markdown('Copyright © 2023-24 Xcelplex LTD - Registeration Number - 14532208 (London, UK)')









