import streamlit as st
import yfinance as yf
import pandas as pd 
import praw as praw
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
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

# Streamlit Interface
default_subreddits = ['stocks', 'investing', 'StockMarket', 'wallstreetbets']
selected_subreddits = st.multiselect('Choose subreddits for analysis:', default_subreddits, default=default_subreddits)

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
        news_items = get_reddit_news(ticker, selected_subreddits)
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

def get_comment_data(ticker_symbol, subreddit_list, post_limit=10, comment_limit=10):
    all_comments = []
    sentiment_scores = []

    total_posts = len(subreddit_list) * post_limit
    processed_posts = 0

    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name)

        for post in subreddit.search(ticker_symbol, limit=post_limit):
            post.comments.replace_more(limit=0)
            for comment in post.comments.list()[:comment_limit]:
                all_comments.append(comment.body)
                analysis = TextBlob(comment.body)
                sentiment_scores.append(analysis.sentiment.polarity)

            processed_posts += 1
            progress_bar.progress(processed_posts / total_posts)

    return all_comments, sentiment_scores

run_analysis = st.button('Run Analysis')

if run_analysis:
    if not selected_subreddits:
        st.error("Please select at least one subreddit.")
    else:
        st.write("## Analysis on Reddit Comments")
        progress_bar = st.progress(0)
        try:
            comments, sentiment_scores = get_comment_data(ticker, selected_subreddits)
            progress_bar.empty()

            # Display average sentiment
            if sentiment_scores:
                average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                st.write(f"Average Sentiment Score for {ticker}: {average_sentiment:.2f}")
            else:
                st.write("No comments found for sentiment analysis.")

            # Generate and Display Word Cloud
            if comments:
                # Create a word cloud object with desired parameters
                wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate(" ".join(comments))
                
                # Set up the figure size and layout with a black background
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                ax.set_facecolor('black')  # Set the axis background color
                fig.set_facecolor('black')  # Set the figure background color
                st.pyplot(plt)
                # Clear the current figure to ensure it does not interfere with future plots
                plt.clf()
            else:
                st.write("No comments found for word cloud.")

        except Exception as e:
            progress_bar.empty()
            st.error(f"Error in analysis: {e}")

# Hide default Streamlit style
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)