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
    #start_Date=st.sidebar.text_input("Start Date", end_Date)
    #end_Date =st.sidebar.text_input("End Date", today)
    data_Stock = yf.download(ticker, start_Date, end_Date)

#######leaving this list option as it is and adding only one ticker for now, incase a default view is required in future for multiple tickers """"""""""
ticker_List = [ticker]
for i in ticker_List:
    #st.write(i)
    value = yf.Ticker(i)
    data_Incm = value.income_stmt
    data_Stock = yf.download(i, period="1mo")
    data_Quarterly_Incm = value.quarterly_income_stmt
    data_balancesheet= value.balance_sheet
    data_news = value.news
    #st.write(data_news)

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



#Ex_Incm= df_Incm.to_excel('finance_income_data.xlsx')
#Ex_Stock=df_Stock.to_excel('finance_stock_data.xlsx')
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




st.markdown("---")
     
col3 = st.columns((5,5,5), gap = 'medium')
with col3[1]:
    st.markdown('Copyright © 2023-24 Xcelplex LTD - Registeration Number - 14532208 (London, UK)')


############### News Section ################

        #title_Sentiment = df_News['sentiment_title'][i]
        #st.write(f'Title Sentiment {title_Sentiment}')
        #news_Sentimenht = df_News['sentiment_summary'][i]
        #st.write(f'News Sentiment {news_Sentimenht}')
        
        
        
    #for i in range(10):












