import streamlit as st
import feedparser

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
col1, col2, col3 = st.columns(3)

# Function to display a single feed
def display_feed(column, feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        column.subheader(entry.title)
        column.write(entry.summary)
        column.markdown(f"[Read More]({entry.link})")

# Displaying feeds in each column
with col1:
    st.header("Column 1")
    display_feed(col1, feeds["Top News"])

with col2:
    st.header("Column 2")
    display_feed(col2, feeds["World News"])

with col3:
    st.header("Column 3")
    display_feed(col3, feeds["US News"])

# Add more columns/sections as needed
