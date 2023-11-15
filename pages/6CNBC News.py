import streamlit as st
import feedparser
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils.rss_functions import * 

feeds = {
    "Top News": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "World News": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "US News": "https://www.cnbc.com/id/15837362/device/rss/rss.html",
    "Asian News":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19832390", 
    "Finance": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
    "Investing":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069",
    "Financial Advisors":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100646281",
    "Market Insider":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20409666", 
    "Charting Asia":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=23103686", 
    "Earnings":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839135",
    "Economy":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258", 
    "Autos":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000101", 
    "Real Estate":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000115",
    "Energy":"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19836768",
    # Add more feeds as needed
}

# Streamlit layout
st.set_page_config(
	page_title="CNBC News",
	layout="wide",
	page_icon="📬",
)
st.sidebar.success("Select a feature above.")
st.title("CNBC News")

# Create a multi-column layout
columns = st.tabs(feeds.keys())

# Initialize session state for each feed
for feed_key in feeds.keys():
    if feed_key not in st.session_state:
        st.session_state[feed_key] = 5  # Initialize with the first five news items
    if f"{feed_key}_more" not in st.session_state:
        st.session_state[f"{feed_key}_more"] = False  # Flag for more news

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
