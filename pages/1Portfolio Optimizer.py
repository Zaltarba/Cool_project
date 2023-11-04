import streamlit as st
import yfinance as yf
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import copy
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
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


def plot_efficient_frontier_and_max_sharpe(mu, S, r:float): 
	# Optimize portfolio for max Sharpe ratio and plot it out with efficient frontier curve
	ef = EfficientFrontier(mu, S)
	fig, ax = plt.subplots(figsize=(0.75*8,0.75*4.5))
	ef_max_sharpe = copy.deepcopy(ef)
	#plotting.plot_efficient_frontier(ef, ax=ax, show_assets=False)
	# Find the max sharpe portfolio
	ef_max_sharpe.max_sharpe(risk_free_rate=r)
	ret_tangent, std_tangent, _ = ef_max_sharpe.portfolio_performance()
	ax.scatter(std_tangent, ret_tangent, marker="*", s=100, c="r", label="Max Sharpe")
	# Generate random portfolios
	n_samples = 1000
	w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
	rets = w.dot(ef.expected_returns)
	stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
	sharpes = rets / stds
	ax.scatter(stds, rets, marker=".", c=sharpes, cmap="viridis_r")
	# Output
	ax.legend()
	return fig
		
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
	try :
		stocks_df = yf.download(tickers, start=start_date, end=end_date)['Adj Close']  # Get Stock Prices using pandas_datareader Library	
		fig_price = px.line(stocks_df, title='Price of Individual Stocks')  # Plot Individual Stock Prices
		# Plot Individual Cumulative Returns
		fig_cum_returns = plot_cum_returns(stocks_df, 'Cumulative Returns of Individual Stocks Starting with $100')
		# Calculatge and Plot Correlation Matrix between Stocks
		corr_df = stocks_df.corr().round(2)
		fig_corr = px.imshow(corr_df, text_auto=True, title = 'Correlation between Stocks')
		# Calculate expected returns and sample covariance matrix for portfolio optimization later
		if expected_return_method == "Mean historical return":
			mu = expected_returns.mean_historical_return(stocks_df)
		elif expected_return_method == "Exponentially-weighted mean historical return":
			mu = expected_returns.ema_historical_return(stocks_df, span=span)
		S = risk_models.sample_cov(stocks_df)
		# Plot efficient frontier curve
		fig = plot_efficient_frontier_and_max_sharpe(mu, S, r)
		fig_efficient_frontier = BytesIO()
		fig.savefig(fig_efficient_frontier, format="png")
				
		# Get optimized weights
		ef = EfficientFrontier(mu, S)
		ef.max_sharpe(risk_free_rate=r)
		weights = ef.clean_weights()
		expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance()
		weights_df = pd.DataFrame.from_dict(weights, orient = 'index')
		weights_df.columns = ['weights']
		
		# Calculate returns of portfolio with optimized weights
		stocks_df['Optimized Portfolio'] = 0
		for ticker, weight in weights.items():
			stocks_df['Optimized Portfolio'] += stocks_df[ticker]*weight
		
		# Plot Cumulative Returns of Optimized Portfolio
		fig_cum_returns_optimized = plot_cum_returns(stocks_df['Optimized Portfolio'], 'Cumulative Returns of Optimized Portfolio Starting with $100')
		
		# Display everything on Streamlit using tabs
		tab1, tab2, tab3, tab4 = st.tabs(["Prices", "Correlations", "Returns", "Optimized Portfolio"])
		with tab1:
			fig_price = px.line(stocks_df, title='Price of Individual Stocks')
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
