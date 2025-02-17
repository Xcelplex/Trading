import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_financials(ticker):
    try:
        stock = yf.Ticker(ticker)
        financials = stock.financials.T  # Get yearly data
        quarterly_financials = stock.quarterly_financials.T  # Get quarterly data
        news = stock.news  # Fetch company-related news
        
        # Format index to remove timestamp
        financials.index = financials.index.strftime('%Y-%m-%d')
        quarterly_financials.index = quarterly_financials.index.strftime('%Y-%m-%d')
        
        # Calculate YoY and Quarterly Yield
        financials['YoY Yield'] = financials['Total Revenue'].pct_change() * 100
        quarterly_financials['Quarterly Yield'] = quarterly_financials['Total Revenue'].pct_change() * 100
        
        # Convert values to millions
        financials[['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income', 'EBITDA']] /= 1e6
        quarterly_financials[['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income', 'EBITDA']] /= 1e6
        
        # Combine financial statistics
        yearly_combined = financials[['Total Revenue', 'YoY Yield', 'Gross Profit', 'Operating Income', 'Net Income', 'EBITDA']]
        quarterly_combined = quarterly_financials[['Total Revenue', 'Quarterly Yield', 'Gross Profit', 'Operating Income', 'Net Income', 'EBITDA']]
        
        return yearly_combined, quarterly_combined, news
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None, None

def plot_performance(data1, data2, title1, title2, ylabel):
    if data1 is not None and data2 is not None:
        sns.set_style("dark")  # Apply dark mode style
        fig, axes = plt.subplots(1, 2, figsize=(8, 2), facecolor='#333333')  # Reduced size, side-by-side
        
        for ax, data, title in zip(axes, [data1, data2], [title1, title2]):
            ax.set_facecolor('#333333')
            data.plot(kind='bar', ax=ax, color='#1fb4aa')
            ax.set_title(title, color='#848c8c')
            ax.set_ylabel(ylabel + " (Millions)", color='#848c8c')
            ax.set_xlabel("Date", color='#848c8c')
            ax.tick_params(colors='#848c8c')
            ax.ticklabel_format(style='plain', axis='y')  # Disable scientific notation
        
        st.pyplot(fig)

def display_news(news):
    if news:
        st.sidebar.subheader("Latest News and Announcements")
        for article in news[:5]:  # Display the latest 5 news articles
            st.sidebar.write(f"**{article['title']}**")
            st.sidebar.write(f"{article['publisher']}")
            st.sidebar.write(f"[Read more]({article['link']})")
            st.sidebar.write("---")

def main():
    st.subheader("Financial Income Data Collector using Yahoo Finance")
    
    # Input section
    st.write("Enter Stock Ticker Symbol")
    ticker = st.text_input("Ticker Symbol (e.g., AAPL, TSLA, MSFT)")
    
    if st.button("Fetch Data") and ticker:
        yearly_combined, quarterly_combined, news = fetch_financials(ticker)
        
        # Yearly Data
        if yearly_combined is not None:
            st.write("Yearly Financial Data (In Millions)")
            st.dataframe(yearly_combined, use_container_width=True, height=None)
            plot_performance(yearly_combined['Total Revenue'], yearly_combined['YoY Yield'], "Yearly Revenue", "Yearly Yield", "Value")
        
        # Quarterly Data
        if quarterly_combined is not None:
            st.write("Quarterly Financial Data (In Millions)")
            st.dataframe(quarterly_combined, use_container_width=True, height=None)
            plot_performance(quarterly_combined['Total Revenue'], quarterly_combined['Quarterly Yield'], "Quarterly Revenue", "Quarterly Yield", "Value")
        
        # Display News in Sidebar
        display_news(news)

if __name__ == "__main__":
    main()


