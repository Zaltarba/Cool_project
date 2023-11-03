import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import math

# Function to calculate the option payoff based on option type
def calculate_option_payoff(option_type, stock_price, strike_price):
    if option_type == "European Call":
        return max(stock_price - strike_price, 0)
    elif option_type == "European Put":
        return max(strike_price - stock_price, 0)

# Function to perform Monte Carlo simulation for option pricing and visualize results
def monte_carlo_option_pricing(option_type, stock_price, strike_price, volatility, risk_free_rate, time_to_maturity, num_simulations):
    dt = time_to_maturity / 252  # Assuming 252 trading days in a year
    option_payoffs = []
    price_paths = []

    for _ in range(num_simulations):
        price_path = []
        stock_price_copy = stock_price

        for _ in range(int(252 * time_to_maturity)):
            drift = (risk_free_rate - 0.5 * volatility**2) * dt
            shock = volatility * math.sqrt(dt) * np.random.normal(0, 1)
            stock_price_copy *= math.exp(drift + shock)
            price_path.append(stock_price_copy)

        price_paths.append(price_path)
        option_payoff = calculate_option_payoff(option_type, stock_price_copy, strike_price)
        option_payoffs.append(option_payoff)

    option_price = np.exp(-risk_free_rate * time_to_maturity) * np.mean(option_payoffs)
    return option_price, price_paths

# set layout to wide
st.set_page_config(layout="wide")
st.sidebar.success("Select a feature above.")
st.title("Monte Carlo Simulation for Option Pricing")
st.write("This app performs Monte Carlo simulation for option pricing and visualizes the simulated price paths.")

col1, col2 = st.columns([0.3, 0.7], gap = 'large')
with col1:
    st.write("## Input Parameters")
    option_type = st.selectbox("Option Type", ("European Call", "European Put"))  # "European Call" or "European Put"  
    stock_price = st.number_input("Stock Price", value=100)
    strike_price = st.number_input("Strike Price", value=100)
    volatility = st.number_input("Volatility", value=0.2)  # Annualized volatility (e.g., 20%)
    risk_free_rate = st.number_input("Risk-free Rate", value=0.05)  # Annual risk-free interest rate (e.g., 5%)
    time_to_maturity = st.number_input("Time to Maturity", value=1)  # Time to maturity in years
    num_simulations = st.number_input("Number of Simulations", value=10)

with col2:
    st.write("## Output")
    # Calculate the option price using Monte Carlo simulation and obtain price paths
    option_price, price_paths = monte_carlo_option_pricing(option_type, stock_price, strike_price, volatility, risk_free_rate, time_to_maturity, num_simulations)

    st.metric("The estimated option price is: ", f"{option_price:.2f}")

    # Combine the simulated price paths into a single DataFrame
    df = pd.DataFrame(price_paths).T
    # Rename columns
    df.columns = [f"Path {i+1}" for i in range(num_simulations)]

    # Create an interactive plot using Plotly Express
    fig = px.line(df, labels={"index": "Time Steps", "value": "Stock Price"}, title="Simulated Price Paths")

    st.plotly_chart(fig, use_container_width=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 