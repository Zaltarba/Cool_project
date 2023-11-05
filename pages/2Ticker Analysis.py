import streamlit as st
import yfinance as yf
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Ticker Analysis", page_icon="📈")

# Sidebar for additional features
st.sidebar.success("Select a feature above.")
analysis_type = st.sidebar.selectbox("Choose Analysis Type", ["Fundamental Analysis", "News Feed"])

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
            st.table(data.info.items())

            # Display interactive chart
            fig = px.line(hist, x=hist.index, y="Close", title=f'{ticker_symbol} Closing Prices')
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display based on the selected analysis type
if analysis_type == "Fundamental Analysis":
    display_ticker_data(ticker)
elif analysis_type == "News Feed":
    st.write("## News Feed")
    # [Insert news feed functionality here]

# Additional placeholder for future functionality
# ...
