import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome on my project ! 👋")

st.markdown(
    """
    Welcome on this website, this is a personnal project aiming to group 
    in a user friendly interface tools needed for decision making in asset management
    """
    )

st.write("## About me")

st.markdown(
    """
    Graduating student with in-depth knowledge in finance, machine 
    learning, statistics and econometrics. Highly motivated for a quantitative researcher 
    position involving the use of econometric methods. I am seeking full-time employment.
    """
    )

st.sidebar.success("Select a feature above.")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 