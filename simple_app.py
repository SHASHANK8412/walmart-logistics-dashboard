import streamlit as st
import os
from streamlit_option_menu import option_menu
from tabs import TABS
from utils.helpers import show_notification
from utils.auth import is_authenticated, is_admin, show_login_form, show_registration_form, logout_user
from utils.fix_blank import fix_blank_page_css, create_simple_hero

# Set page configuration
st.set_page_config(
    page_title="Walmart Logistics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Apply simple CSS to fix blank page
fix_blank_page_css()

# Initialize session state for authentication
if 'auth_view' not in st.session_state:
    st.session_state.auth_view = "login"

# Check if user is authenticated
if not is_authenticated():
    # Show login container
    st.title("Welcome to Walmart Logistics Dashboard")
    
    # Simple hero section
    hero_html = create_simple_hero(
        title="Walmart Logistics Dashboard",
        subtitle="Secure Login • Advanced Analytics • Supply Chain Excellence • Real-time Insights"
    )
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Authentication tabs
    auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
    
    with auth_tab1:
        show_login_form()
    
    with auth_tab2:
        show_registration_form()

else:
    # User is authenticated, show appropriate dashboard
    
    # Sidebar with navigation options
    with st.sidebar:
        # Use absolute path for the image to prevent PIL.UnidentifiedImageError
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "walmart_logo.png")
        st.image(image_path, width=200)
        
        selected_tab = option_menu(
            menu_title="Main Menu",
            options=list(TABS.keys()),
            icons=["speedometer2", "box", "truck", "graph-up", "gear", "people", "shield-lock"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"font-size": "16px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#0071ce"},
            }
        )
    
    # Main content
    if is_admin():
        hero_html = create_simple_hero(
            title="Walmart Admin Command Center",
            subtitle="Advanced AI-Powered Operations • Real-time Analytics • Smart Automation"
        )
    else:
        hero_html = create_simple_hero(
            title="Walmart Customer Dashboard",
            subtitle="Track Orders • View Inventory • Check Delivery Status"
        )
    
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Display selected tab content
    TABS[selected_tab]()
