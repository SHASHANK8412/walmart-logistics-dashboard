import streamlit as st
import os

# Set page configuration
st.set_page_config(
    page_title="Walmart Logistics Dashboard - Test",
    page_icon="🛒",
    layout="wide"
)

# Add simple CSS
st.markdown("""
<style>
body {
    font-family: Arial, sans-serif;
}

.hero-section {
    padding: 60px 40px;
    margin: 20px 0 40px 0;
    text-align: center;
    background: linear-gradient(135deg, #6e3ec0 0%, #592b9e 100%);
    color: white;
    border-radius: 15px;
}

.hero-title {
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 20px;
}

.hero-subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# Simple hero section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Walmart Logistics Dashboard</h1>
    <p class="hero-subtitle">Advanced Analytics • Supply Chain Excellence • Real-time Insights</p>
</div>
""", unsafe_allow_html=True)

# Main content
st.title("Test App")
st.write("This is a simple test app to fix the blank page issue.")

# Display Walmart logo as text instead of image to avoid PIL errors
st.markdown("""
<div style="
    background-color: #0071dc;
    color: white;
    text-align: center;
    padding: 20px;
    border-radius: 10px;
    font-size: 24px;
    font-weight: bold;
    margin: 20px 0;
">
    WALMART
</div>
""", unsafe_allow_html=True)

st.success("Using text-based logo instead of image to avoid PIL errors")
    
# Add some test metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Orders", "578", "+12%")
    
with col2:
    st.metric("Revenue", "$12,487", "+8.2%")
    
with col3:
    st.metric("Customers", "892", "+5.1%")

# Test button
if st.button("Click Me"):
    st.balloons()
    st.write("Button clicked!")
