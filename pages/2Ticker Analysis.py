import streamlit as st

st.set_page_config(
    page_title="Ticker Analysis",
    page_icon="📈", 
)
st.sidebar.success("Select a feature above.")

st.write("# Ticker Analysis")

ticker = st.text_input('Enter ticker to be studied, e.g. MA,META,V,AMZN,JPM,BA', '').upper()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 