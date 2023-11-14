import streamlit as st
import feedparser
import matplotlib.pyplot as plt
from wordcloud import WordCloud

feeds = {
    "Top News": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "World News": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "US News": "https://www.cnbc.com/id/15837362/device/rss/rss.html",
    "Finance": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
    "Investing":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069",
    # Add more feeds as needed
}

# Streamlit layout
st.title("CNBC RSS Feed Reader")

# Create a multi-column layout
columns = st.tabs(feeds.keys())

# Function to display a single feed
def display_feed(column, feed_url):
    feed = feedparser.parse(feed_url)
    try:
        text = " ".join([entry.title for entry in feed.entries])
    except AttributeError:
        pass
    try:
        text += " ".join([entry.summary for entry in feed.entries])
    except AttributeError:
        pass

    # Create a word cloud object with desired parameters
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate(text)            
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
for i, col in enumerate(columns):

    with col:
        header = list(feeds.keys())[i]
        st.header(header)
        display_feed(col, feeds[header])

# Add more columns/sections as needed
