from utils.reddit_api_key import *
import streamlit as st
import praw
from transformers import pipeline
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

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
        titles = []

        for post in posts:
            analysis = sentiment_analyzer(post.title)[0]
            sentiment_score = 1 if analysis['label'] == 'POSITIVE' else -1
            confidence = analysis['score']

            sentiments.append(sentiment_score)
            confidences.append(confidence)
            titles.append(post.title)

            st.write(f"{post.title} - Sentiment: {'Positive' if sentiment_score > 0 else 'Negative'}, Confidence: {confidence:.2f}")

        # Scatter Plot with Plotly
        fig = px.scatter(x=sentiments, y=confidences, text=titles, color=px.colors.qualitative.Plotly,
                         labels={'x': 'Sentiment Score (1=Positive, -1=Negative)', 'y': 'Confidence'})
        fig.update_traces(textposition='top center')
        fig.update_layout(title="Sentiment Score vs Confidence")
        st.plotly_chart(fig, use_container_width=True)

        # Word Cloud
        wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate(" ".join(titles))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    except Exception as e:
        st.error(f"Error fetching Reddit posts: {e}")

# Additional features and functionality can be added as needed
