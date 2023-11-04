import streamlit as st

# Function to create the welcome page
def create_welcome_page():
    st.title("Welcome to Gamma Project!")

    # Create a container for the main welcome message
    with st.container():
        st.write("## Empower Your Investment Decisions")
        st.markdown("""
            The Gamma Project aims to assist you navigate the complexities of asset management.
            With our intuitive interface and powerful analysis tools, you can:
            
            - **Analyze** your asset allocation
            - **Track** your investments' performance
            - **Forecast** future trends with predictive analytics
            - **Learn** with up-to-date financial insights
            - **Optimize** your portfolio for better risk-adjusted returns
            
            Ready to take control of your financial future? Let's get started!
        """)

    # Create columns for feature highlights
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image("pics/img 1.png")  # Path to an image illustrating analysis
            st.write("#### In-Depth Analysis")
            st.write("Deep dive into your portfolio's performance metrics and growth potential.")

        with col2:
            st.image("pics/img 2.png")  # Path to an image illustrating tracking
            st.write("#### Real-Time Tracking")
            st.write("Stay updated with live data feeds and performance charts.")

        with col3:
            st.image("pics/img 3.png")  # Path to an image illustrating forecast
            st.write("#### Future Forecast")
            st.write("Utilize predictive analytics to forecast and strategize for future market conditions.")

    # Include a call-to-action button
    with st.container():
        st.write("---")
        if st.button("Get Started"):
            st.write("Navigating to the main dashboard...")  # Here you can redirect to another page or perform an action.
            # Redirect to the main dashboard function or app page
            # main_dashboard()  # Assuming you have a function that creates the main dashboard

# Call the function to render the welcome page
create_welcome_page()
