import streamlit as st
from transformers import pipeline

# Load the sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Streamlit page configuration
st.set_page_config(page_title="Sentiment Analysis App", layout="wide")

# Page title
st.title("Sentiment Analysis with Transformers")

# Model description
st.markdown("""
## About the Sentiment Analysis Model

This application uses a pre-trained model from the Hugging Face Transformers library for sentiment analysis. The model is based on advanced deep learning techniques using transformer architectures.

### Key Features:
- **Model Architecture**: The backbone of this model is a transformer-based neural network, often a variant of the BERT (Bidirectional Encoder Representations from Transformers) model.
- **Training Data**: The model is trained on a large dataset of labeled text data, where each text sample is associated with a sentiment label (like positive, negative, or neutral).
- **Capabilities**: It's capable of understanding the context of a sentence and determining the overall sentiment. This includes picking up on nuances and subtleties in language.
- **Use Case**: Ideal for analyzing customer feedback, social media posts, product reviews, and any text data where understanding sentiment is crucial.

### Limitations:
- **Contextual Understanding**: While highly accurate, the model may sometimes misinterpret sarcasm, irony, or complex expressions.
- **Language Support**: Primarily trained on English language data; performance on other languages may vary.

### Note:
The model's output includes both the sentiment label and a confidence score, indicating the model's certainty about the sentiment.
""")


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
