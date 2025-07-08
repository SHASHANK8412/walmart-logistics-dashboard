import streamlit as st

# Set page config
st.set_page_config(
    page_title="Simple Image Test",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("Image Loading Test")

# Test direct HTML image loading
st.markdown("""
## Direct HTML Image Test

### External Image:
<img src="https://www.logodesignlove.com/wp-content/uploads/2019/07/walmart-logo-01.jpg" width="200">

### CSS Background Image:
<div style="
    width: 100%;
    height: 300px;
    background-image: url('https://corporate.walmart.com/content/dam/corporate/en_us/design-assets/header-meta/corporate-building-minimal.jpg');
    background-size: cover;
    background-position: center;
    border-radius: 10px;
"></div>
""", unsafe_allow_html=True)

# Test Streamlit's image display
st.write("## Streamlit Image Display")
st.image("https://www.logodesignlove.com/wp-content/uploads/2019/07/walmart-logo-01.jpg", width=200)

# Provide helpful explanation
st.write("""
## Troubleshooting
If you can see the images above:
1. External HTML images work
2. CSS background images work
3. Streamlit's image function works

If any are not visible, it may indicate network/connection issues or content blocking.
""")
