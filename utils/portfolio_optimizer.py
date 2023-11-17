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
import plotly.graph_objs as go
import copy
from wordcloud import WordCloud
import pickle as pkl

@st.cache_data
def plot_cum_returns(data, title):	
	daily_cum_returns = (1 + data.dropna().pct_change()).cumprod()*100
	fig = px.line(daily_cum_returns, title=title)
	return fig

@st.cache_data
def plot_efficient_frontier_and_max_sharpe(mu, S, r):
	ef = EfficientFrontier(mu, S)
	ef_max_sharpe = copy.deepcopy(ef)
		
	# Find the max sharpe portfolio
	ef_max_sharpe.max_sharpe(risk_free_rate=r)
	ret_tangent, std_tangent, _ = ef_max_sharpe.portfolio_performance()
		
	# Generate random portfolios
	n_samples = 10000
	w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
	rets = w.dot(ef.expected_returns)
	stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
	sharpes = rets / stds
		
	# Create a scatter plot of the random portfolios
	scatter = go.Scatter(
		x=stds, y=rets, mode='markers', 
		marker=dict(size=5, color=sharpes, colorscale='Viridis', showscale=True, colorbar=dict(x=-0.25)),
		name='Random Portfolios'
	)
		
	# Mark the max Sharpe portfolio
	max_sharpe = go.Scatter(
		x=[std_tangent], y=[ret_tangent], mode='markers', 
		marker=dict(color='red', size=10, line=dict(width=2, color='DarkSlateGrey')),
		name='Max Sharpe Ratio'
	)
		
	# Combine plots
	data = [scatter, max_sharpe]
		
	# Layout configuration
	layout = go.Layout(
		title='Efficient Frontier with Max Sharpe Ratio',
		yaxis=dict(title='Expected Return'),
		xaxis=dict(title='Volatility'),
		showlegend=True,
		margin=dict(t=20, b=20, l=20, r=20), 
	)
		
	fig = go.Figure(data=data, layout=layout)
	return fig

# Cache the stock data retrieval
@st.cache_data
def get_stock_data(tickers, start_date, end_date):
	return yf.download(tickers, start=start_date, end=end_date)['Adj Close']  # We use the adjusted close price to avoid issues with dividends payings stocks

# Cache the calculations of expected returns and sample covariance
@st.cache_data
def calculate_metrics(stocks_df, expected_return_method, span):
	if expected_return_method == "Mean historical return":
		mu = expected_returns.mean_historical_return(stocks_df)
	elif expected_return_method == "Exponentially-weighted mean historical return":
		mu = expected_returns.ema_historical_return(stocks_df, span=span)
	S = risk_models.sample_cov(stocks_df)
	return mu, S