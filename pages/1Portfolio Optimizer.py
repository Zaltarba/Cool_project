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


st.set_page_config(
	page_title="Portfolio Optimizer",
	layout="wide",
	page_icon="💸",
)
st.sidebar.success("Select a feature above.")
st.title("Portfolio Optimizer 🚀")	

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
else:
	span = 0

ticker_options = pd.read_csv("data/all_tickers.csv").values[:, 0].tolist()

# Use st.multiselect to let user select multiple ticker symbols
tickers = st.multiselect(
    'Select stock tickers',
    ticker_options,
    default=["AAPL", "GOOGL"]  # You can set default selections here
)

if st.button('Analyze Portfolio'):
	try :
		stocks_df = get_stock_data(tickers, start_date, end_date)
		fig_price = px.line(stocks_df, title='Price of Individual Stocks')  # Plot Individual Stock Prices
		# Plot Individual Cumulative Returns
		fig_cum_returns = plot_cum_returns(stocks_df, 'Cumulative Returns of Individual Stocks Starting with $100')
		# Calculatge and Plot Correlation Matrix between Stocks
		corr_df = stocks_df.corr().round(2)
		fig_corr = px.imshow(corr_df, text_auto=True, title = 'Correlation between Stocks')
		# Calculate expected returns and sample covariance matrix for portfolio optimization later
		mu, S = calculate_metrics(stocks_df, expected_return_method, span)
		# Plot efficient frontier curve
		fig_efficient_frontier = plot_efficient_frontier_and_max_sharpe(mu, S, r)	
		# Get optimized weights
		ef = EfficientFrontier(mu, S)
		ef.max_sharpe(risk_free_rate=r)
		weights = ef.clean_weights()
		expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance()
		weights_df = pd.DataFrame.from_dict(weights, orient = 'index')
		weights_df.columns = ['weights']
		# Calculate returns of portfolio with optimized weights
		stocks_df['Optimized Portfolio'] = 0
		text_wordcloud = ''
		for ticker, weight in weights.items():
			stocks_df['Optimized Portfolio'] += stocks_df[ticker]*weight
			text_wordcloud += "ticker"*int(weight*1000)
		wordcloud = WordCloud().generate(text_wordcloud)
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

			# Use columns to arrange the data frame and metrics side by side
			col1, col2 = st.columns((3, 1))
			with col1:
				st.dataframe(weights_df)

			with col2:
				st.metric(label="Expected Annual Return", value=f"{expected_annual_return:.2%}")
				st.metric(label="Annual Volatility", value=f"{annual_volatility:.2%}")
				st.metric(label="Sharpe Ratio", value=f"{sharpe_ratio:.2f}")

			plt.imshow(wordcloud, interpolation='bilinear')
			plt.axis("off")
			plt.show()
			st.pyplot()

			# Display the graphs in full width below the metrics and dataframe
			st.plotly_chart(fig_cum_returns_optimized, use_container_width=True)

			st.plotly_chart(fig_efficient_frontier, use_container_width=True)

	except ValueError:
		st.error('Please enter valid stock tickers separated by commas WITHOUT spaces.')

# Add a button and expander for the explanation of portfolio optimization
if st.button('Learn More about Portfolio Optimization'):
    with st.expander("How is portfolio optimization computed?"):
        st.write("""
            Portfolio optimization is the process of selecting the best portfolio (asset distribution), out of the set of all portfolios being considered, according to some objective. The objective typically maximizes factors such as expected return, and minimizes costs like financial risk.
            
            Factors that affect portfolio optimization include:
            
            - **Risk Preference:** How much risk is the investor willing to take.
            - **Market Expectations:** Expected returns of the assets, which can be based on historical data or other prediction models.
            - **Covariance Matrix:** It represents how the returns of the assets move together.
            - **Constraints:** These may include budget constraints, risk constraints, or regulatory constraints.
            
            The **Efficient Frontier** is a key concept, representing the set of optimal portfolios that offer the highest expected return for a defined level of risk or the lowest risk for a given level of expected return.
            
            **Modern Portfolio Theory (MPT)** is a common method used, which relies on the variance of asset returns as a proxy for risk. The goal is to find the set of weights (the proportion of total portfolio value invested in each asset) that minimizes the portfolio variance for a given expected return.
            
            The portfolio with the highest Sharpe ratio (expected return minus the risk-free rate, divided by the standard deviation of portfolio return) is considered the most efficient under the MPT framework.
            """)


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
