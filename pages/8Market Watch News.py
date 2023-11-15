import streamlit as st
import feedparser
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

def display_banner():
    feed = feedparser.parse(headlines_url)

    headline_str = ' - '.join(f'&#128200; {entry.title}' for entry in feed.entries)

    text_html = """
    <div style="
        width: 100%; 
        white-space: nowrap; 
        overflow: hidden; 
        box-sizing: border-box;">
        <div style="
            display: inline-block;
            padding-left: 100%;
            animation: ticker 30s linear infinite;">
            {headline_str}
        </div>
    </div>

    <style>
    @keyframes ticker {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """
    # Display the ticker
    st.markdown(text_html, unsafe_allow_html=True)

display_banner()

# Callback function to increment news count
def increment_news_count(key):
    st.session_state[key] += 5

# Function to display a single feed
def display_feed(column, feed_url, feed_key):

    feed = feedparser.parse(feed_url)
    displayed_items = st.session_state[feed_key]

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
