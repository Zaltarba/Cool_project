import streamlit as st
import feedparser
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils.rss_functions import *


feeds = {
    "Top Stories":"http://feeds.marketwatch.com/marketwatch/topstories/",
    "Market Pulse":"http://feeds.marketwatch.com/marketwatch/marketpulse/",
    "Stock to Watch":"http://feeds.marketwatch.com/marketwatch/stocktowatch/",
    "Automobile":"http://feeds.marketwatch.com/marketwatch/Autoreviews/",
    # Add more feeds as needed
}

headlines_url = "http://feeds.marketwatch.com/marketwatch/realtimeheadlines/"

# Streamlit layout
st.set_page_config(
	page_title="Market Watch News",
	layout="wide",
	page_icon="📬",
)
st.sidebar.success("Select a feature above.")

# Initialize session state for each feed
for feed_key in feeds.keys():
    if feed_key not in st.session_state:
        st.session_state[feed_key] = 5  # Initialize with the first five news items
    if f"{feed_key}_more" not in st.session_state:
        st.session_state[f"{feed_key}_more"] = False  # Flag for more news

display_banner(headlines_url)
st.title("MarketWatch News")

# Create a multi-column layout
columns = st.tabs(feeds.keys())

# Displaying feeds in each column
for i, col in enumerate(columns):
    with col:
        header = list(feeds.keys())[i]
        st.title(header)
        display_feed(col, feeds[header], header)
        # Check if more news is requested
        if st.session_state[f"{header}_more"]:
            st.session_state[header] += 5
            st.session_state[f"{header}_more"] = False  # Reset the flag
# Add more columns/sections as needed
