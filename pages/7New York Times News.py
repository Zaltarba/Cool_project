import streamlit as st
from utils.rss_functions import *

feeds = {
    "World News": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "US News": "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "Asian News":"https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml", 
    "European News":"https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml", 
    "Economy":"https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml", 
    "Buisness":"https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", 
    "Real Estate":"https://rss.nytimes.com/services/xml/rss/nyt/RealEstate.xml", 
    "Most Shared":"https://rss.nytimes.com/services/xml/rss/nyt/MostShared.xml", 
    "Most Viewed":"https://rss.nytimes.com/services/xml/rss/nyt/MostViewed.xml", 
    # Add more feeds as needed
}

# Streamlit layout
st.set_page_config(
	page_title="New Yorks Times News",
	layout="wide",
	page_icon="📬",
)
st.sidebar.success("Select a feature above.")
st.title("New Yorks Times News")

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
