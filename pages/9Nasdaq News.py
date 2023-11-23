import streamlit as st
from utils.rss_functions import *

feeds = {
    #"Nasdaq original content":"https://www.nasdaq.com/feed/nasdaq-original/rss.xml",
    "Commodities":"https://www.nasdaq.com/feed/rssoutbound?category=Commodities",
    "Crypto":"https://www.nasdaq.com/feed/rssoutbound?category=Cryptocurrencies", 
    "Dividends":"https://www.nasdaq.com/feed/rssoutbound?category=Dividends",
    "Earnings":"https://www.nasdaq.com/feed/rssoutbound?category=Earnings",
    "Investing":"https://www.nasdaq.com/feed/rssoutbound?category=Investing", 
    "Apple":"https://www.nasdaq.com/feed/rssoutbound?symbol=aapl", 
    "Amazon":"https://www.nasdaq.com/feed/rssoutbound?symbol=AMZN", 
    "Microsoft":"https://www.nasdaq.com/feed/rssoutbound?symbol=MSFT", 
}

# Streamlit layout
st.set_page_config(
	page_title="Nasdaq News",
	page_icon="📬",
)
st.sidebar.success("Select a feature above.")
st.title("Nasdaq News")

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
