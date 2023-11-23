import streamlit as st
import datetime as datetime
from utils.rss_functions import *
from utils.RSS_architecture import *
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


st.set_page_config(
	page_title="RSS News Aggregator",
	page_icon="📳",
)
st.sidebar.success("Select a feature above.")
st.title("RSS News Aggregator 📳")	

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

# Aggregate the data with the date filter
counts = {}
for source, categories in all_feeds.items():
    if source.value in selected_sources:
        for category, articles in categories.items():
            # Filter articles based on the minimal date selected
            filtered_articles = [article for article in articles if is_after_min_date(article['date'], min_date)]
            if category not in counts:
                counts[category] = {}
            counts[category][source.value] = len(filtered_articles)

# Prepare the data for Plotly
data = []
for category, sources in counts.items():
    for source, count in sources.items():
        data.append({'Category': category, 'Source': source, 'Number of Articles': count, 'Date': min_date})

# Create a DataFrame
df = pd.DataFrame(data)

# Create the bar plot with Plotly
fig = px.bar(df, x='Source', y='Number of Articles', color='Category',
             title='Number of articles per category per data provider since ' + str(min_date),
             labels={'Number of articles': 'Number of articles since ' + str(min_date)})

# Display the plot in Streamlit
st.plotly_chart(fig)

from utils.stopwords import english_stop_words

def generate_wordcloud(source_articles):
    text = " ".join(article['title'] for article in source_articles)
    wordcloud = WordCloud(width = 800, height = 400, background_color ='black', stopwords = english_stop_words).generate(text)
    plt.figure(figsize = (8, 4), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    st.set_option('deprecation.showPyplotGlobalUse', False) # to disable warning
    st.pyplot()

# Place the word cloud in an expandable section at the desired location in your layout
with st.expander("View Word Clouds"):
    # Create tabs for each data source
    tabs = st.tabs(selected_sources)
    for tab, source in zip(tabs, DataProvider):
        with tab:
            # Assuming that the 'fetch_all_feeds' function or similar has been called 
            # and 'all_feeds' is populated with the articles data
            source_articles = [article for categories in all_feeds[source].values() for article in categories if is_after_min_date(article["date"], min_date)]
            if len(source_articles)>0:
                generate_wordcloud(source_articles)
            else:
                st.write("No recent article")

# Displaying the feeds with a card-like layout
for source, categories in all_feeds.items():
    if source.value in selected_sources:
        st.header(f"Source: {source.value}")
        for category, articles in categories.items():
            if len([article for article in articles if is_after_min_date(article['date'], min_date)]) > 0:
                with st.expander(f"Category: {category}"): 
                    for article in articles:
                        article_date = article['date']  # Adjust the format as per your date format
                        if is_after_min_date(article_date, min_date):
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.image(icons_path[source.value]) # Optional: source/category icon
                            with col2:
                                st.markdown(f"**[{article['title']}]({article['link']})**")
                                st.caption(f"{article['date']}")
                                st.write(article.get('summary', 'No summary available')[:200])
                            st.markdown("---")  # Horizontal line as a separator