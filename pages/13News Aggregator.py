import streamlit as st
import datetime as datetime
from utils.rss_functions import *
from utils.RSS_architecture import *
import pandas as pd 

# Assuming DataProvider is an Enum with your sources
source_options = [source.value for source in DataProvider]
selected_sources = st.multiselect('Select Data Sources:', source_options, default=source_options)
selected_feeds = [source for source in DataProvider if source.value in selected_sources]

min_date = st.date_input("Select minimal publication date:")

feed_manager = FeedManager({feed:feeds[feed] for feed in feeds.keys()})
all_feeds = feed_manager.fetch_all_feeds()

# Function to check if an article's date is after the selected minimum date
def is_after_min_date(article_date, min_date):
    return pd.to_datetime(article_date, utc=True) >= pd.to_datetime(min_date, utc=True)

for source, categories in all_feeds.items():
    if source.value in selected_sources:
        with st.expander(f"Source: {source}"):
            for category, articles in categories.items():
                with st.expander(f"Category: {category}", expanded=False):
                    for article in articles:
                        article_date = article['date'] # Adjust the format as per your date format
                        if is_after_min_date(article_date, min_date):
                            st.markdown(f"**Title:** {article['title']}\n"
                                        f"**Date:** {article_date}\n"
                                        f"**Summary:** {article.get('summary', 'No summary available')}\n"
                                        f"[Read more]({article['link']})")