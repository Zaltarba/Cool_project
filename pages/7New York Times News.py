import streamlit as st
import feedparser
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

# Callback function to increment news count
def increment_news_count(key):
    st.session_state[key] += 5

# Function to display a single feed
def display_feed(column, feed_url, feed_key):

    feed = feedparser.parse(feed_url)
    displayed_items = 5 + st.session_state[feed_key]

    # Process text for WordCloud
    text = "test "
    for entry in feed.entries[:displayed_items]:
        try:
            text += entry.title
        except AttributeError:
            pass
        try:
            text += entry.summary
        except AttributeError:
            pass

    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the ratio as needed
    with col2:
        # Create a word cloud object with desired parameters
        wordcloud = WordCloud(width=1600, height=900, background_color='black', colormap='Pastel1').generate(text)            
        # Set up the figure size and layout with a black background
        fig, ax = plt.subplots(figsize=(4, 2.25))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.set_facecolor('black')  # Set the axis background color
        fig.set_facecolor('black')  # Set the figure background color
        st.pyplot(fig)
        # Clear the current figure to ensure it does not interfere with future plots
        plt.clf()

    # Display the limited number of feed entries
    for entry in feed.entries[:displayed_items]:
        try:
            column.subheader(entry.title)
            try:
                column.write(entry.get("summary", ""))
            except AttributeError:
                pass
            column.markdown(f"[Read More]({entry.link})")
        except AttributeError:
            pass

    # Button to request more news
    if column.button("Show More", key=f"{feed_key}_btn"):
        st.session_state[f"{feed_key}_more"] = True

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
