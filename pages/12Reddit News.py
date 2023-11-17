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

def get_reddit_posts(subreddits):
    news_posts = []
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.hot(limit=10):
            news_posts.append(post)
    return news_posts

run_reddit_analysis = st.button('Run Reddit Analysis')

if run_reddit_analysis:
    st.write("## Reddit Posts Sentiment Analysis")
    try:
        posts = get_reddit_posts(selected_subreddits)
        sentiments = []
        confidences = []

        for post in posts:
            analysis = sentiment_analyzer(post.title)[0]
            sentiment_score = 1 if analysis['label'] == 'POSITIVE' else -1
            confidence = analysis['score']

            sentiments.append(sentiment_score)
            confidences.append(confidence)

            st.write(f"{post.title} - Sentiment: {'Positive' if sentiment_score > 0 else 'Negative'}, Confidence: {confidence:.2f}")

        # Scatter Plot
        fig, ax = plt.subplots()
        ax.scatter(sentiments, confidences, c=sentiments, cmap='RdYlGn', alpha=0.7)
        ax.set_title("Sentiment Score vs Confidence")
        ax.set_xlabel("Sentiment Score (1=Positive, -1=Negative)")
        ax.set_ylabel("Confidence")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error fetching Reddit posts: {e}")
