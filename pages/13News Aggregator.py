import streamlit as st
import datetime as datetime
from utils.rss_functions import *
from utils.RSS_architecture import *

# Assuming DataProvider is an Enum with your sources
source_options = [source.value for source in DataProvider]
selected_sources = st.multiselect('Select Data Sources:', source_options, default=source_options)
min_date = st.date_input("Select minimal publication date:")

feed_manager = FeedManager({feed:feeds[feed] for feed in source_options})
all_feeds = feed_manager.fetch_all_feeds()

# Function to check if an article's date is after the selected minimum date
def is_after_min_date(article_date, min_date):
    return article_date >= min_date

# Displaying the feeds
for source, categories in all_feeds.items():
    if source in selected_sources:
        st.write(f"Source: {source}")
        for category, articles in categories.items():
            st.write(f"Category: {category}")
            for article in articles:
                article_date = datetime.strptime(article['date'], '%Y-%m-%d') # Adjust the format as per your date format
                if is_after_min_date(article_date, min_date):
                    st.write(f"Title: {article['title']}")
                    # Display other fields as required
