import streamlit as st
import praw
from transformers import pipeline
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from utils.reddit_api_key import *

# Initialize Reddit connection
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent=reddit_user_agent)

# Initialize sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Streamlit Interface
st.title("Reddit Sentiment Analysis")

default_subreddits = ['stocks', 'investing', 'StockMarket', 'wallstreetbets']
selected_subreddits = st.multiselect('Choose subreddits for analysis:', default_subreddits, default=default_subreddits)

ticker = st.text_input('Enter a stock ticker for analysis:', 'AAPL')

def get_reddit_posts(subreddits, ticker_symbol):
    news_posts = []
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.search(ticker_symbol, limit=10, sort='hot'):
            news_posts.append(post)
    return news_posts

run_reddit_analysis = st.button('Run Reddit Analysis')

if run_reddit_analysis:
    st.write("## Reddit Posts Analysis")
    try:
        posts = get_reddit_posts(selected_subreddits, ticker)
        sentiments = []
        for post in posts:
            analysis = sentiment_analyzer(post.title)
            sentiment = analysis[0]['label']
            sentiments.append(sentiment)
            st.write(f"{post.title} - Sentiment: {sentiment}")

        # Count sentiment occurrences
        sentiment_count = Counter(sentiments)

        # Plotting
        fig, ax = plt.subplots()
        ax.bar(sentiment_count.keys(), sentiment_count.values())
        ax.set_title("Sentiment Distribution")
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error fetching Reddit posts: {e}")

# Optional: Add more functionality like word cloud or detailed analysis per post
