import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Pair Analysis",
    page_icon="💸", 
)
st.sidebar.success("Select a feature above.")

st.title("Pair Analysis 💸")

col1, col2 = st.columns(2)
with col1:
    ticker_1 = st.text_input('Enter first ticker to be studied, e.g. MA,META,V,AMZN,JPM,BA', '').upper()
with col2:
    ticker_2 = st.text_input('Enter second ticker to be studied, e.g. MA,META,V,AMZN,JPM,BA', '').upper()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 