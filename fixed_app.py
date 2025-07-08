import streamlit as st
import os
import pandas as pd
from datetime import datetime, timedelta

# Set page configuration with simple settings
st.set_page_config(
    page_title="Walmart Logistics Dashboard - Fixed",
    page_icon="🛒",
    layout="wide"
)

# Inject simple CSS
st.markdown("""
<style>
/* Simple styles to ensure page renders */
body {
    font-family: sans-serif;
}

/* Simple gradient background for hero section */
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

# Display a simple hero section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">Walmart Logistics Dashboard</h1>
    <p class="hero-subtitle">Fixed Version • No Image Dependencies • Simple Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Main content
st.title("Dashboard Overview")
st.write("This is a simplified version of the dashboard that doesn't rely on loading image files.")

# Add some metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Orders Today", "578", "+12%")
    
with col2:
    st.metric("Revenue", "$12,487", "+8.2%")
    
with col3:
    st.metric("Active Users", "892", "+5.1%")

with col4:
    st.metric("System Health", "99.8%", "-0.2%")

# Add a chart
st.subheader("Sales Trend")
chart_data = pd.DataFrame({
    "Date": pd.date_range(start=datetime.now() - timedelta(days=30), periods=30),
    "Sales": [100, 120, 115, 130, 140, 135, 155, 160, 165, 155, 
              170, 180, 175, 190, 200, 210, 205, 220, 230, 225, 
              240, 250, 245, 260, 270, 280, 275, 290, 300, 310]
})
st.line_chart(chart_data.set_index("Date"))

# Add some text content
st.subheader("System Status")
st.write("All systems are operating normally. The dashboard is now fixed and running without image loading errors.")

# Add a sample table
st.subheader("Recent Orders")
orders_data = {
    "Order ID": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005"],
    "Customer": ["John Smith", "Mary Johnson", "Robert Brown", "Lisa Davis", "Michael Wilson"],
    "Date": ["2025-07-08", "2025-07-07", "2025-07-07", "2025-07-06", "2025-07-06"],
    "Amount": ["$235.40", "$189.95", "$320.50", "$145.75", "$278.20"],
    "Status": ["Delivered", "Processing", "Shipped", "Delivered", "Processing"]
}
st.table(pd.DataFrame(orders_data))

# Add a button
if st.button("Refresh Data"):
    st.success("Data refreshed successfully!")
    st.balloons()
