import streamlit as st
import yfinance as yf
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Ticker Analysis", page_icon="📈")

# Main page title
st.write("# Ticker Analysis")

# Input for ticker symbol
ticker = st.text_input('Enter ticker to be studied, e.g. MA, META, V, AMZN, JPM, BA', '').upper()

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
            # Fetch data
            data = yf.Ticker(ticker_symbol)
            hist = data.history(period="1mo")

            # Check if data is retrieved
            if hist.empty:
                st.error("No data found for the ticker symbol.")
                return

            # Display basic info
            st.write(f"## Fundamental Analysis of {ticker_symbol}")
            st.table(data.info)

            # Display interactive chart
            fig = px.line(hist, x=hist.index, y="Close", title=f'{ticker_symbol} Closing Prices')
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display data for the entered ticker
display_ticker_data(ticker)
