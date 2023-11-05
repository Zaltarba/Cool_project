import streamlit as st
import yfinance as yf
import pandas as pd 

# Set page configuration
st.set_page_config(page_title="Ticker Analysis", page_icon="📈")

# Main page title
st.write("# Ticker Analysis")

# Input for ticker symbol
ticker_options = pd.read_csv("data/all_tickers.csv").values[:, 0].tolist()

# Use st.multiselect to let user select multiple ticker symbols
ticker = st.selectbox(
    'Select stock tickers',
    ticker_options, 
)

# Checkbox to run fundamental analysis
run_analysis = st.button('Run Fundamental Analysis')

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

            # Display dividends
            st.subheader("Dividends:")
            try:
                st.line_chart(stock.dividends)
            except Exception:
                st.warning("Dividends data not available.")

            # Display stock splits
            st.subheader("Stock Splits:")
            try:
                st.table(stock.splits)
            except Exception:
                st.warning("Stock splits data not available.")

            # Display financials
            st.subheader("Financials:")
            try:
                st.table(stock.financials)
            except Exception:
                st.warning("Financials data not available.")

            # Display balance sheet
            st.subheader("Balance Sheet:")
            try:
                st.table(stock.balance_sheet)
            except Exception:
                st.warning("Balance sheet data not available.")

        except Exception as e:
            st.error(f"An error occurred while fetching data for {ticker_symbol}: {e}")

# Run the analysis if the checkbox is checked
if run_analysis:
    display_ticker_data(ticker)
