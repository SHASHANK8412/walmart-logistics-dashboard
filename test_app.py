import streamlit as st

st.set_page_config(
    page_title="Walmart Logistics Dashboard",
    page_icon="🛒",
    layout="wide",
)

st.title("Walmart Logistics Dashboard")
st.write("This is a test page to fix the blank page issue")

st.markdown("""
<div style="padding: 20px; background-color: #f0f0f0; border-radius: 10px;">
    <h2>Testing Basic HTML Rendering</h2>
    <p>If you can see this, HTML rendering is working correctly.</p>
</div>
""", unsafe_allow_html=True)

if st.button("Click me to test interactivity"):
    st.success("Button clicked successfully!")
