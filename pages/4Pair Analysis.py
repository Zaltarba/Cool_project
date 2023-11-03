import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Ticker Analysis",
    page_icon="📈", 
)
st.sidebar.success("Select a feature above.")

st.write("# Ticker Analysis")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 