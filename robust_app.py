import streamlit as st
import os
import pandas as pd
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
from tabs import TABS
from utils.helpers import show_notification
from utils.robust_hero import create_robust_hero_section
from utils.auth import is_authenticated, is_admin, show_login_form, show_registration_form, logout_user

# Set page configuration with premium settings
st.set_page_config(
    page_title="Walmart Logistics Dashboard | With Background Image",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject simple CSS
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

body {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f7f9fc;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #6e3ec0 0%, #592b9e 100%);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for authentication
if 'auth_view' not in st.session_state:
    st.session_state.auth_view = "login"

# Authentication flow
if not is_authenticated():
    # User is not authenticated, show login/registration
    
    # Use the robust hero section that gracefully handles image loading
    hero_html = create_robust_hero_section(
        title="Walmart Logistics Dashboard",
        subtitle="Secure Login • Advanced Analytics • Supply Chain Excellence • Real-time Insights",
        use_walmart_bg=True
    )
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Authentication container
    st.markdown("""
    <div style="
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 20px auto;
        max-width: 600px;
    ">
    """, unsafe_allow_html=True)
    
    # Authentication tabs
    auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
    
    with auth_tab1:
        show_login_form()
    
    with auth_tab2:
        show_registration_form()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional information section
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 0.9rem;">
        <p>This is a demonstration of the Walmart Logistics Dashboard.</p>
        <p>Use the following credentials to log in:</p>
        <p><strong>Admin:</strong> username: admin, password: admin123</p>
        <p><strong>Customer:</strong> username: user, password: user123</p>
    </div>
    """, unsafe_allow_html=True)

else:
    # User is authenticated, show appropriate dashboard
    
    # Sidebar with modern design
    with st.sidebar:
        # Modern Logo Section - Using text logo to avoid PIL errors
        st.markdown("""
        <div style="
            text-align: center;
            padding: 20px 0;
            background: linear-gradient(135deg, #6e3ec0 0%, #592b9e 100%);
            margin: -20px -20px 20px -20px;
            border-radius: 0 0 20px 20px;
            color: white;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">🛒</div>
            <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-weight: 700;">Walmart</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9rem;">Logistics Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User is authenticated, show appropriate navigation
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
                "nav-link-selected": {"background-color": "#6e3ec0", "font-weight": "bold"},
            }
        )
        
        # User info section
        st.markdown(f"""
        <div style="
            margin-top: 20px;
            padding: 15px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 10px;
            border-left: 4px solid #6e3ec0;
        ">
            <div style="font-size: 0.8rem; color: #6e3ec0;">LOGGED IN AS</div>
            <div style="font-weight: bold; margin: 5px 0;">{st.session_state.user_name}</div>
            <div style="font-size: 0.8rem; margin-bottom: 10px;">{st.session_state.user_role.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout"):
            logout_user()
            st.experimental_rerun()
    
    # Main content with robust hero section
    if is_admin():
        # Admin dashboard with robust hero section
        hero_html = create_robust_hero_section(
            title="Walmart Admin Command Center",
            subtitle="Advanced AI-Powered Operations • Real-time Analytics • Smart Automation • Supply Chain Excellence",
            use_walmart_bg=True
        )
    else:
        # Customer dashboard with robust hero section
        hero_html = create_robust_hero_section(
            title="Walmart Customer Dashboard",
            subtitle="Track Orders • View Inventory • Check Delivery Status • Supply Chain Insights",
            use_walmart_bg=True
        )
    
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Display metrics
    st.markdown("## 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Orders Today", "578", "+12%")
    
    with col2:
        st.metric("Revenue", "$12,487", "+8.2%")
    
    with col3:
        st.metric("Active Users", "892", "+5.1%")
    
    with col4:
        st.metric("System Health", "99.8%", "-0.2%")
    
    # Display selected tab content
    st.markdown(f"## {selected_tab}")
    
    # Show tab info
    st.markdown(f"The **{selected_tab}** module would be displayed here.")
    
    # Sample content
    st.info("This is a simplified version of the app that uses the Walmart background image in a robust way.")
    
    if st.button("Refresh Data"):
        st.success("Data refreshed successfully!")
        st.balloons()
