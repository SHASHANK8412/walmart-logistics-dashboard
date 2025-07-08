import streamlit as st
from utils.url_hero import create_url_hero_section

# Set page configuration
st.set_page_config(
    page_title="Walmart Image Test",
    page_icon="🛒",
    layout="wide"
)

# Use the URL-based hero section
hero_html = create_url_hero_section(
    "Walmart Logistics Dashboard", 
    "Optimize your supply chain with real-time analytics and advanced inventory management"
)
st.markdown(hero_html, unsafe_allow_html=True)

# Add some basic content
st.write("## This is a test page")
st.write("If you can see the hero image above, the external URL approach is working.")
