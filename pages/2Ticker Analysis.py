import streamlit as st
import yfinance as yf
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Ticker Analysis", page_icon="📈")

# Main page title
st.write("# Ticker Analysis")

# Input for ticker symbol
ticker = st.text_input('Enter ticker to be studied, e.g. MSFT, AAPL, GOOGL', '').upper()

# Hide default Streamlit style
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Function to fetch and display data
def display_ticker_data(ticker_symbol):
    if ticker_symbol:
        try:
            # Import the ticker and its information
            stock = yf.Ticker(ticker_symbol)

            # Display basic info
            st.write(f"## Fundamental Analysis of {ticker_symbol}")

            # Extract and display company information
            st.subheader("Company Information:")
            st.json(stock.info)

            # Extract and display dividends
            st.subheader("Dividends:")
            st.line_chart(stock.dividends)

            # Extract and display stock splits
            st.subheader("Stock Splits:")
            st.table(stock.splits)

            # Extracts and displays some financials 
            st.subheader("Financials:")
            st.table(stock.financials)

            # Extracts and displays the balance sheet
            st.subheader("Balance Sheet:")
            st.table(stock.balance_sheet)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display data for the entered ticker
display_ticker_data(ticker)
