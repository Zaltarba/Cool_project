import streamlit as st
import yfinance as yf
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import numpy as np
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="Portfolio Optimizer",
    layout="wide",
    page_icon="📈",
)
st.sidebar.success("Select a feature above.")
st.title("Portfolio Optimizer 🚀")	

# Define styles for matplotlib and seaborn inside functions

def plot_cum_returns(data, title):    
    daily_cum_returns = (1 + data.dropna().pct_change()).cumprod()*100
    fig = px.line(daily_cum_returns, title=title)
    return fig

def plot_efficient_frontier_and_max_sharpe(mu, S, r: float):
    # Import matplotlib here to ensure the style is applied correctly
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('dark_background')
    sns.set(style="darkgrid")
    
    # Efficient frontier plotting code...

# Main layout
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    start_date = st.date_input("Start Date", datetime(2013, 1, 1))
with col2:
    end_date = st.date_input("End Date")  # Defaults to current date
with col3:
    r = st.number_input("Risk-free rate", value=0.02)
with col4:
    expected_return_method = st.selectbox(
        "Expected Return Method", 
        ["Mean historical return", "Exponentially-weighted mean historical return"]
    )

if expected_return_method == "Exponentially-weighted mean historical return":
    span = st.slider("Time span for the EMA", min_value=30, max_value=1000, value=500, step=10)

tickers_string = st.text_input(
    'Enter stock tickers separated by commas WITHOUT spaces, e.g. "MA,META,V,AMZN,JPM,BA"',
    ''
).upper()
tickers = tickers_string.split(',')

if st.button('Analyze Portfolio'):
    try:
        # Data fetching and processing code...

        # Display everything on Streamlit using tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Prices", "Correlations", "Returns", "Optimized Portfolio"])
        
        with tab1:
            st.plotly_chart(fig_price, use_container_width=True)
        
        with tab2:
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with tab3:
            st.plotly_chart(fig_cum_returns, use_container_width=True)
        
        with tab4:
            st.subheader('Portfolio Weights and Performance')
            st.dataframe(weights_df)
            st.plotly_chart(fig_cum_returns_optimized, use_container_width=True)
            st.image(fig_efficient_frontier.getvalue())
            
            st.metric(label="Expected Annual Return", value=f"{expected_annual_return:.2%}")
            st.metric(label="Annual Volatility", value=f"{annual_volatility:.2%}")
            st.metric(label="Sharpe Ratio", value=f"{sharpe_ratio:.2f}")

    except ValueError:
        st.error('Please enter valid stock tickers separated by commas WITHOUT spaces.')

# Custom styles
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stTabs > .tablist > li > button {
        padding: 10px 20px;
        border: none;
        margin: 0 2px;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
