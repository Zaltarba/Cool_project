import streamlit as st

# HTML and CSS for the moving text
ticker_html = """
<div style="
    width: 100%; 
    white-space: nowrap; 
    overflow: hidden; 
    box-sizing: border-box;">
    <div style="
        display: inline-block;
        padding-left: 100%;
        animation: ticker 30s linear infinite;">
        &#128200; Stock Headline 1 - &#128200; Stock Headline 2 - &#128200; Stock Headline 3 - ...
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
st.markdown(ticker_html, unsafe_allow_html=True)