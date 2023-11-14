import streamlit as st
import feedparser
import matplotlib.pyplot as plt
from wordcloud import WordCloud

feeds = {
    "Top News": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "World News": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "US News": "https://www.cnbc.com/id/15837362/device/rss/rss.html",
    "Finance": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
    # Add more feeds as needed
}

# Streamlit layout
st.title("CNBC RSS Feed Reader")

# Create a multi-column layout
col1, col2, col3, col4 = st.tabs(feeds.keys())

# Function to display a single feed
def display_feed(column, feed_url):
    feed = feedparser.parse(feed_url)
    text = " ".join([entry.title for entry in feed.entries])
    text += " ".join([entry.summary for entry in feed.entries])
    # Create a word cloud object with desired parameters
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate(" ".join(text))
                
    # Set up the figure size and layout with a black background
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    ax.set_facecolor('black')  # Set the axis background color
    fig.set_facecolor('black')  # Set the figure background color
    st.pyplot(plt)
    # Clear the current figure to ensure it does not interfere with future plots
    plt.clf()

    for entry in feed.entries:
        column.subheader(entry.title)
        column.write(entry.summary)
        column.markdown(f"[Read More]({entry.link})")

# Displaying feeds in each column
with col1:
    st.header("Top News")
    display_feed(col1, feeds["Top News"])

with col2:
    st.header("World News")
    display_feed(col2, feeds["World News"])

with col3:
    st.header("US News")
    display_feed(col3, feeds["US News"])

with col4:
    st.header("Financial News")
    display_feed(col4, feeds["Finance"])

# Add more columns/sections as needed
