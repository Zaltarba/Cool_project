import feedparser
import streamlit as st 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob

def display_banner(headlines_url):
    feed = feedparser.parse(headlines_url)

    headline_str = ' - '.join(f'&#128200; {entry.title}' for entry in feed.entries)

    text_html = f"""
    <div style="
        width: 100%; 
        white-space: nowrap; 
        overflow: hidden; 
        box-sizing: border-box;">
        <div style="
            display: inline-block;
            padding-left: 100%;
            animation: ticker 30s linear infinite;">
            {headline_str}"""+"""
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

# Callback function to increment news count
def increment_news_count(key):
    st.session_state[key] += 5

# Function to display a single feed
def display_feed(column, feed_url, feed_key):

    with st.spinner('Loading news feed...'):
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
            with st.spinner('Generating word cloud...'):
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
            sentiment = TextBlob(entry.title).sentiment.polarity

            if sentiment > 0:
                sentiment_color = 'green'
                sentiment_text = 'Positive'
            elif sentiment < 0:
                sentiment_color = 'red'
                sentiment_text = 'Negative'
            else:
                sentiment_color = 'blue'
                sentiment_text = 'Neutral'

            # Use markdown with HTML to display colored sentiment
            st.markdown(f'<p style="color:{sentiment_color};">Sentiment: {sentiment_text}</p>', unsafe_allow_html=True)

            try:
                column.write(entry.get("summary", ""))
            except AttributeError:
                pass
            column.markdown(f"[Read More]({entry.link})")
        except AttributeError:
            pass
    
    _, col4, _ = st.columns([1, 2, 1])  # Adjust the ratio as needed
    with col4:
        # Button to request more news
        if column.button("Show More", key=f"{feed_key}_btn"):
            st.session_state[f"{feed_key}_more"] = True