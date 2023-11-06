import streamlit as st
import yfinance as yf
import pandas as pd 
import praw as praw
import textblob as textblob

# Set page configuration
st.set_page_config(page_title="Ticker Analysis", page_icon="📈")

# Main page title
st.title("Ticker Analysis 📈")

# Input for ticker symbol
ticker_options = pd.read_csv("data/all_tickers.csv").values[:, 0].tolist()

# Use st.multiselect to let user select multiple ticker symbols
ticker = st.selectbox(
    'Select stock tickers',
    ticker_options, 
)

# Checkbox to run fundamental analysis
run_fundamental_analysis = st.button('Run Fundamental Analysis')

# Function to fetch and display data
def display_ticker_data(ticker_symbol):
    if ticker_symbol:
        try:
            # Import the ticker and its information
            stock = yf.Ticker(ticker_symbol)

            # Create tabs for different data sections
            tab1, tab2, tab3, tab4 = st.tabs(["Dividends", "Stock Splits", "Financials", "Balance Sheet"])

            # Display dividends in the first tab
            with tab1:
                try:
                    st.line_chart(stock.dividends)
                except Exception:
                    st.warning("Dividends data not available.")

            # Display stock splits in the second tab
            with tab2:
                try:
                    st.table(stock.splits)
                except Exception:
                    st.warning("Stock splits data not available.")

            # Display financials in the third tab
            with tab3:
                try:
                    st.table(stock.financials)
                except Exception:
                    st.warning("Financials data not available.")

            # Display balance sheet in the fourth tab
            with tab4:
                try:
                    st.table(stock.balance_sheet)
                except Exception:
                    st.warning("Balance sheet data not available.")

        except Exception as e:
            st.error(f"An error occurred while fetching data for {ticker_symbol}: {e}")


# Run the analysis if the checkbox is checked
if run_fundamental_analysis:
    display_ticker_data(ticker)

# Reddit API credentials
reddit_client_id = 'tTKTJ5YX5qM2ej16P4Oofg'
reddit_client_secret = '9_iF4UzlsCZdcvQETlpbmf62-Ovd4w'
reddit_user_agent = 'streamlit.com.gamma.myredditapp:v1.2.3 (by /u/daniel98smith)'


# Initialize Reddit connection
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent=reddit_user_agent)

def get_reddit_news(ticker_symbol, subreddits=None):
    if subreddits is None:
        subreddits = ['stocks', 'investing', 'StockMarket', 'wallstreetbets']  # Default subreddits

    news_posts = []

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Fetch top popular posts
        for post in subreddit.search(ticker_symbol, limit=5, sort='hot'):  
            news_posts.append({'title': post.title, 'url': post.url, 'subreddit': subreddit_name, 'type': 'popular'})

        # Fetch latest posts
        for post in subreddit.search(ticker_symbol, limit=5, sort='new'):
            news_posts.append({'title': post.title, 'url': post.url, 'subreddit': subreddit_name, 'type': 'latest'})

    return news_posts

# Checkbox to run fundamental analysis
run_reddit_analysis = st.button('Run Reddit Analysis')

# Run the analysis if the checkbox is checked
if run_reddit_analysis:
    st.write("## Latest News on Reddit")
    try:
        news_items = get_reddit_news(ticker)
        if news_items:
            tab1, tab2 = st.tabs(["Popular News", "Latest News"])
            with tab1:
                for item in [ni for ni in news_items if ni['type'] == 'popular']:
                    st.write(f"[{item['title']}]({item['url']}) - {item['subreddit']}")
            with tab2:
                for item in [ni for ni in news_items if ni['type'] == 'latest']:
                    st.write(f"[{item['title']}]({item['url']}) - {item['subreddit']}")
        else:
            st.write("No news found for this ticker.")
    except Exception as e:
        st.error(f"Error fetching news: {e}")

def get_comment_sentiment(ticker_symbol, subreddit_list=['stocks', 'investing', 'StockMarket', 'wallstreetbets'], post_limit=10, comment_limit=10):
    sentiment_scores = []

    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name)

        for post in subreddit.search(ticker_symbol, limit=post_limit):
            post.comments.replace_more(limit=0)  # Load all comments, limit=0 to avoid loading nested comments
            for comment in post.comments.list()[:comment_limit]:  # Analyze top comments per post
                analysis = textblob.TextBlob(comment.body)
                sentiment_scores.append(analysis.sentiment.polarity)

    if sentiment_scores:
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    else:
        average_sentiment = 0

    return average_sentiment

# Streamlit Interface
run_sentiment_analysis = st.button('Run Sentiment Analysis')

if run_sentiment_analysis:
    st.write("## Sentiment Analysis on Reddit Comments")
    try:
        sentiment_score = get_comment_sentiment(ticker)
        st.write(f"Average Sentiment Score for {ticker}: {sentiment_score:.2f}")
    except Exception as e:
        st.error(f"Error in sentiment analysis: {e}")

# Hide default Streamlit style
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)