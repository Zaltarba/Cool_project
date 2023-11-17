import streamlit as st
from transformers import pipeline

# Load the sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Streamlit page configuration
st.set_page_config(page_title="Sentiment Analysis App", layout="wide")

# Page title
st.title("Sentiment Analysis with Transformers")

# Input text from user
user_input = st.text_area("Enter a sentence for sentiment analysis", "")

# Button to perform analysis
if st.button("Analyze Sentiment"):
    with st.spinner('Analyzing...'):
        # Perform sentiment analysis
        result = sentiment_analyzer(user_input)[0]
        sentiment = result['label']
        confidence = result['score']

        # Display results
        st.success(f"Sentiment: {sentiment}, Confidence: {confidence:.2f}")
