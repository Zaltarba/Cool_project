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

icons_path = {
    "CNBC": "pics/CNBC_icon.jpg",
    "MarketWatch": "pics/MW_icon.jpg",
    "New York Times": "pics/NYT_icon.jpg",
    # Add more as needed
}

import matplotlib.pyplot as plt

# Count the number of articles per category per data provider
article_counts = {source.value: {category: len(articles) for category, articles in categories.items()} for source, categories in all_feeds.items()}

# Data for plotting
categories = set()
for counts in article_counts.values():
    categories.update(counts.keys())
categories = list(categories)
data_provider_names = list(article_counts.keys())
bar_data = {category: [article_counts.get(provider, {}).get(category, 0) for provider in data_provider_names] for category in categories}

# Plotting
fig, ax = plt.subplots()

# We need to set the position of each bar along the x-axis
bar_width = 0.35
index = np.arange(len(data_provider_names))

for i, category in enumerate(categories):
    ax.bar(index + i*bar_width, bar_data[category], bar_width, label=category)

ax.set_xlabel('Data Provider')
ax.set_ylabel('Number of Articles')
ax.set_title('Number of articles per category per data provider')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(data_provider_names)
ax.legend()

st.pyplot(fig)


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