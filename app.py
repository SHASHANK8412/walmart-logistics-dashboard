import streamlit as st
import os
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from streamlit_option_menu import option_menu
from tabs import TABS
from utils.helpers import show_notification
from utils.styles import inject_custom_css, create_hero_section
from utils.robust_hero import create_robust_hero_section
from utils.url_hero import create_url_hero_section
from utils.auth import is_authenticated, is_admin, show_login_form, show_registration_form, logout_user

# Set page configuration with premium settings
st.set_page_config(
    page_title="Walmart Logistics Dashboard | World-Class Operations",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://walmart.com/help',
        'Report a bug': "https://walmart.com/support",
        'About': "Walmart Logistics Dashboard - Powered by Advanced AI & Analytics"
    }
)

# Inject simple CSS to avoid blank page issue
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

# Initialize session state for authentication
if 'auth_view' not in st.session_state:
    st.session_state.auth_view = "login"

# Sidebar with modern design
with st.sidebar:
    # Modern Logo Section
    st.markdown("""
    <div style="
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -20px -20px 20px -20px;
        border-radius: 0 0 20px 20px;
        color: white;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🛒</div>
        <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-weight: 700;">Walmart</h2>
        <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9rem;">Logistics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    if is_authenticated():
        # User is authenticated, show appropriate navigation
        
        # Initialize session state for selected tab
        if 'selected_tab' not in st.session_state:
            st.session_state.selected_tab = "📦 Orders"
        
        # Define tabs based on user role
        if is_admin():
            # Admin gets full access to all tabs
            available_tabs = TABS
        else:
            # Customers get limited tabs
            available_tabs = {
                "📦 Orders": TABS["📦 Orders"],
                "📚 Inventory": TABS["📚 Inventory"],
                "🚚 Delivery": TABS["🚚 Delivery"],
                "🔗 Supply Chain": TABS["🔗 Supply Chain"]
            }
        
        # Modern Navigation with enhanced styling
        st.markdown("### 🧭 Navigation")
        selected_tab = option_menu(
            "",
            list(available_tabs.keys()),
            icons=['box-seam-fill', 'journal-text', 'truck', 'diagram-3-fill'],
            menu_icon="grid-3x3-gap-fill",
            default_index=list(available_tabs.keys()).index(st.session_state.selected_tab) if st.session_state.selected_tab in available_tabs.keys() else 0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#667eea", "font-size": "18px"}, 
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "2px 0",
                    "padding": "12px 16px",
                    "border-radius": "12px",
                    "font-family": "'Inter', sans-serif",
                    "font-weight": "500",
                    "--hover-color": "rgba(102, 126, 234, 0.1)"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "color": "white",
                    "font-weight": "600",
                    "box-shadow": "0 4px 12px rgba(102, 126, 234, 0.3)"
                }
            }
        )
        
        # Update session state
        st.session_state.selected_tab = selected_tab
        
        # Modern User Profile Section
        st.markdown("---")
        
        # Get user info
        user = st.session_state.user
        user_initials = "".join([name[0].upper() for name in user['name'].split(' ')[:2]])
        user_role = "Admin" if user['role'] == "admin" else "Customer"
        user_title = "Operations Manager" if user['role'] == "admin" else "Registered User"
        
        user_profile_html = f"""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 12px;
                    color: white;
                    font-weight: bold;
                ">{user_initials}</div>
                <div>
                    <div style="font-weight: 600; color: #1f2937;">{user['name']}</div>
                    <div style="font-size: 0.8rem; color: #6b7280;">{user_title}</div>
                </div>
            </div>
            <div style="
                background: rgba(102, 126, 234, 0.1);
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 0.8rem;
                color: #4f46e5;
                margin-bottom: 10px;
            ">
                🟢 Online • Role: {user_role}
            </div>
            <button id="logout-btn" style="
                width: 100%;
                padding: 8px 12px;
                background-color: #f3f4f6;
                border: none;
                border-radius: 6px;
                color: #4b5563;
                font-size: 0.9rem;
                cursor: pointer;
                transition: all 0.2s;
                text-align: center;
            ">🚪 Logout</button>
        </div>
        """
        
        # Add script separately to avoid f-string issues
        script_html = """
        <script>
            document.getElementById('logout-btn').addEventListener('click', function() {
                window.location.href = window.location.pathname + '?logout=true';
            });
        </script>
        """
        
        # Combine the HTML and render it
        st.markdown(user_profile_html + script_html, unsafe_allow_html=True)
        
        # Handle logout
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        
        # AI Assistant Section (only for logged-in users)
        st.markdown("### 🤖 AI Assistant")
        with st.expander("💬 Smart Assistant", expanded=False):
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 15px;
            ">
                <div style="font-size: 0.9rem; color: #4f46e5; margin-bottom: 10px;">
                    🧠 AI-Powered Analytics Ready
                </div>
                <div style="font-size: 0.8rem; color: #6b7280;">
                    Ask me about inventory, analytics, or optimization insights.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            user_query = st.text_input("Ask AI", placeholder="Ask anything about operations...", key="ai_assistant", label_visibility="hidden")
            if st.button("🚀 Ask AI", use_container_width=True):
                if user_query:
                    st.success("🤖 AI Assistant: I'm analyzing your request and preparing insights...")
            
            # Quick Actions
            st.markdown("**Quick Actions:**")
            if st.button("📊 Generate Report", use_container_width=True, key="quick_report"):
                st.info("📈 Generating comprehensive analytics report...")
            if st.button("🔍 Inventory Audit", use_container_width=True, key="quick_audit"):
                st.info("📦 Running real-time inventory audit...")

# Initialize session state for notifications
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# Check for logout parameter in URL
query_params = st.experimental_get_query_params()
if 'logout' in query_params and query_params['logout'][0] == 'true':
    logout_user()
    st.experimental_set_query_params()
    st.rerun()

# Authentication flow
if not is_authenticated():
    # User is not authenticated, show login/registration
    
    # Use the URL-based hero section that uses external images
    hero_html = create_url_hero_section(
        title="Walmart Logistics Dashboard",
        subtitle="Secure Login • Advanced Analytics • Supply Chain Excellence • Real-time Insights"
    )
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Authentication container
    st.markdown("""
    <div style="
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    ">
    """, unsafe_allow_html=True)
    
    # Switch between login and registration
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔐 Login", use_container_width=True, 
                     type="primary" if st.session_state.auth_view == "login" else "secondary"):
            st.session_state.auth_view = "login"
            st.rerun()
    
    with col2:
        if st.button("📝 Register", use_container_width=True,
                    type="primary" if st.session_state.auth_view == "register" else "secondary"):
            st.session_state.auth_view = "register"
            st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Show login or registration form based on selected view
    if st.session_state.auth_view == "login":
        show_login_form()
    else:
        show_registration_form()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer for authentication page
    st.markdown("""
    <div style="
        text-align: center;
        margin-top: 40px;
        margin-bottom: 20px;
    ">
        <p style="color: #6b7280; font-size: 0.9rem;">
            © 2025 Walmart Inc. • All Rights Reserved • Privacy Policy • Terms of Service
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # User is authenticated, show appropriate dashboard
    
    # Main content with robust hero section
    if is_admin():
        # Admin dashboard with URL-based hero section
        hero_html = create_url_hero_section(
            title="Walmart Admin Command Center",
            subtitle="Advanced AI-Powered Operations • Real-time Analytics • Smart Automation • Supply Chain Excellence"
        )
    else:
        # Customer dashboard with URL-based hero section
        hero_html = create_url_hero_section(
            title="Walmart Customer Dashboard",
            subtitle="Track Orders • View Inventory • Check Delivery Status • Supply Chain Insights"
        )
    
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Display different metrics based on user role
    if is_admin():
        # Admin metrics
        st.markdown("## 📡 Live System Status")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🟢 System Health", "99.9%", "+0.1%")
        
        with col2:
            st.metric("👥 Active Users", "1,247", "+18")
        
        with col3:
            st.metric("📦 Orders Today", "8,456", "+12.5%")
        
        with col4:
            st.metric("💰 Revenue", "$2.1M", "+8.3%")
        
        with col5:
            st.metric("⚡ Efficiency", "94.7%", "+2.1%")
            
        # Admin dashboard with advanced visualizations
        st.markdown("## 📊 Operations Overview")
        
        tab1, tab2, tab3 = st.tabs(["📈 Performance", "🌐 Network Status", "⚠️ Alerts & Issues"])
        
        with tab1:
            # Performance metrics
            st.markdown("### 📊 Key Performance Indicators")
            
            # Create two columns for charts
            perf_col1, perf_col2 = st.columns(2)
            
            with perf_col1:
                # Orders trend chart
                chart_data = pd.DataFrame({
                    "Date": pd.date_range(start=datetime.now() - timedelta(days=30), periods=30),
                    "Orders": [4521, 5292, 4489, 4227, 5512, 6023, 5193, 5762, 4980, 5104, 
                               5321, 5694, 6203, 7105, 6898, 7423, 8012, 8456, 8201, 7845,
                               8120, 8354, 8103, 8562, 8341, 8689, 8123, 8456, 8732, 9105]
                })
                
                # Create plotly chart
                fig = px.line(
                    chart_data, 
                    x="Date", 
                    y="Orders", 
                    title="Daily Orders (Last 30 Days)",
                    markers=True
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
            with perf_col2:
                # Revenue breakdown
                revenue_data = pd.DataFrame({
                    "Category": ["Electronics", "Clothing", "Food & Grocery", "Home & Garden", "Toys"],
                    "Revenue": [850000, 520000, 430000, 190000, 110000]
                })
                
                fig = px.pie(
                    revenue_data,
                    values="Revenue",
                    names="Category",
                    title="Revenue by Category",
                    hole=0.4
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # User activity metrics
            st.markdown("### 👥 User Activity")
            
            user_col1, user_col2, user_col3, user_col4 = st.columns(4)
            
            with user_col1:
                st.metric("Registered Users", "24,857", "+128 this week")
                
            with user_col2:
                st.metric("Active Today", "1,247", "5% of total")
                
            with user_col3:
                st.metric("New Signups", "34", "+8.3% vs. yesterday")
                
            with user_col4:
                st.metric("Avg. Session Time", "12m 24s", "+42s")
                
            # Display user distribution chart
            user_dist = pd.DataFrame({
                "User Type": ["Admin", "Manager", "Staff", "Customer"],
                "Count": [12, 58, 173, 24614]
            })
            
            # Create a horizontal bar chart
            fig = px.bar(
                user_dist, 
                y="User Type", 
                x="Count", 
                orientation='h',
                title="User Distribution by Role",
                color="Count",
                color_continuous_scale="Viridis"
            )
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
                
        with tab2:
            # Network status visualization
            st.markdown("### 🌐 Global Distribution Network")
            
            # Create a network map
            network_col1, network_col2 = st.columns([2, 1])
            
            with network_col1:
                # Display a world map with locations
                import folium
                from streamlit_folium import folium_static
                
                # Create world map
                m = folium.Map(location=[20, 0], zoom_start=2)
                
                # Add warehouse locations
                warehouse_locations = [
                    {"name": "Central HQ", "location": [39.0997, -94.5786], "type": "hq"},  # Kansas City
                    {"name": "West Coast DC", "location": [34.0522, -118.2437], "type": "dc"},  # Los Angeles
                    {"name": "East Coast DC", "location": [40.7128, -74.0060], "type": "dc"},  # New York
                    {"name": "South DC", "location": [29.7604, -95.3698], "type": "dc"},  # Houston
                    {"name": "Midwest DC", "location": [41.8781, -87.6298], "type": "dc"},  # Chicago
                    {"name": "Europe DC", "location": [52.3676, 4.9041], "type": "dc"},  # Amsterdam
                    {"name": "Asia DC", "location": [22.3193, 114.1694], "type": "dc"}  # Hong Kong
                ]
                
                # Add markers
                for wh in warehouse_locations:
                    icon_color = "red" if wh["type"] == "hq" else "blue"
                    folium.Marker(
                        location=wh["location"],
                        popup=wh["name"],
                        icon=folium.Icon(color=icon_color)
                    ).add_to(m)
                
                # Display map
                folium_static(m)
            
            with network_col2:
                # Display network health metrics
                st.markdown("### 📊 Network Health")
                
                # Network status indicators
                statuses = {
                    "Central HQ": {"status": "Online", "latency": "12ms", "load": 72},
                    "West Coast DC": {"status": "Online", "latency": "24ms", "load": 85},
                    "East Coast DC": {"status": "Online", "latency": "18ms", "load": 91},
                    "South DC": {"status": "Online", "latency": "22ms", "load": 64},
                    "Midwest DC": {"status": "Online", "latency": "15ms", "load": 78},
                    "Europe DC": {"status": "Online", "latency": "105ms", "load": 58},
                    "Asia DC": {"status": "Online", "latency": "180ms", "load": 42}
                }
                
                # Display status cards
                for loc, data in statuses.items():
                    color = "green" if data["status"] == "Online" else "red"
                    load_color = "green" if data["load"] < 70 else "orange" if data["load"] < 90 else "red"
                    
                    st.markdown(f"""
                    <div style="padding: 10px; margin-bottom: 10px; background-color: rgba(255,255,255,0.1); border-left: 4px solid {color}; border-radius: 4px;">
                        <div style="display: flex; justify-content: space-between;">
                            <div><strong>{loc}</strong></div>
                            <div style="color: {color};">{data["status"]}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                            <div>Latency: {data["latency"]}</div>
                            <div>Load: <span style="color: {load_color};">{data["load"]}%</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
        with tab3:
            # Alerts and issues
            st.markdown("### ⚠️ Active Alerts")
            
            # Sample alerts
            alerts = [
                {"severity": "High", "message": "Inventory shortage detected for SKU #5781 (iPhone 13 Pro)", "time": "10 minutes ago", "location": "East Coast DC"},
                {"severity": "Medium", "message": "Delivery delay for Order #7712 due to weather conditions", "time": "42 minutes ago", "location": "South DC"},
                {"severity": "Low", "message": "System update scheduled for 2:00 AM EDT", "time": "1 hour ago", "location": "Central HQ"},
                {"severity": "Medium", "message": "Warehouse capacity reaching threshold (85%)", "time": "2 hours ago", "location": "West Coast DC"},
                {"severity": "High", "message": "API latency increase detected in payment processing", "time": "3 hours ago", "location": "Central HQ"}
            ]
            
            # Display alerts
            for alert in alerts:
                if alert["severity"] == "High":
                    icon = "🔴"
                    color = "red"
                elif alert["severity"] == "Medium":
                    icon = "🟠"
                    color = "orange" 
                else:
                    icon = "🟡"
                    color = "goldenrod"
                    
                st.markdown(f"""
                <div style="padding: 10px; margin-bottom: 10px; background-color: rgba(255,255,255,0.1); border-left: 4px solid {color}; border-radius: 4px;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>{icon} <strong>{alert["severity"]} Alert</strong>: {alert["message"]}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.9em; color: #888;">
                        <div>Location: {alert["location"]}</div>
                        <div>{alert["time"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Resolution actions
            st.markdown("### 🛠️ Quick Actions")
            
            action_col1, action_col2, action_col3 = st.columns(3)
            
            with action_col1:
                if st.button("🔄 Refresh Status", key="refresh_status", use_container_width=True):
                    st.success("System status refreshed!")
            
            with action_col2:
                if st.button("📨 Send Alerts to Team", key="send_alerts", use_container_width=True):
                    st.success("Alerts sent to operations team!")
                    
            with action_col3:
                if st.button("📊 Generate Incident Report", key="gen_report", use_container_width=True):
                    st.success("Incident report being generated!")
    else:
        # Customer metrics
        st.markdown("## 📊 Your Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🛒 Your Orders", "5", "+1 this week")
        
        with col2:
            st.metric("📦 Pending Delivery", "2", "")
        
        with col3:
            st.metric("💰 Total Spent", "$425.78", "+$105.43")
        
        with col4:
            st.metric("⭐ Satisfaction", "4.8/5", "+0.2")
            
        # Customer dashboard with personalized data
        st.markdown("## 🛍️ Your Walmart Experience")
        
        tab1, tab2, tab3 = st.tabs(["📊 Activity", "🛒 Recent Orders", "⭐ Recommendations"])
        
        with tab1:
            # Customer activity overview
            st.markdown("### 📈 Your Shopping Activity")
            
            # Create two columns for charts
            act_col1, act_col2 = st.columns(2)
            
            with act_col1:
                # Spending trend
                spending_data = pd.DataFrame({
                    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
                    "Amount": [85.42, 112.33, 67.89, 159.91, 425.78]
                })
                
                fig = px.line(
                    spending_data,
                    x="Month",
                    y="Amount",
                    title="Your Monthly Spending ($)",
                    markers=True,
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
            with act_col2:
                # Category breakdown
                category_data = pd.DataFrame({
                    "Category": ["Electronics", "Clothing", "Grocery", "Home Goods"],
                    "Amount": [299.99, 75.43, 35.89, 14.47]
                })
                
                fig = px.pie(
                    category_data,
                    values="Amount",
                    names="Category",
                    title="Your Spending by Category",
                    hole=0.4
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
            # Loyalty rewards
            st.markdown("### 🌟 Your Rewards Status")
            
            # Rewards progress
            st.markdown("""
            <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="margin-top: 0;">Walmart+ Membership</h4>
                <div style="margin-bottom: 10px;">Reward Points: <strong>275 / 500</strong> needed for next reward</div>
                <div style="background-color: #eee; height: 20px; border-radius: 10px; overflow: hidden;">
                    <div style="background: linear-gradient(to right, #0071ce, #76c5f5); width: 55%; height: 100%; color: white; text-align: center; line-height: 20px; font-size: 12px;">
                        55%
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                    <strong>Next reward:</strong> $10 discount on your next order
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Benefits list
            st.markdown("### 🎁 Your Member Benefits")
            
            ben_col1, ben_col2 = st.columns(2)
            
            with ben_col1:
                st.markdown("""
                - ✅ **Free delivery** on eligible orders
                - ✅ **Member prices** on fuel
                - ✅ **Mobile scan & go** in stores
                """)
                
            with ben_col2:
                st.markdown("""
                - ✅ **Free shipping** - no minimum
                - ✅ **Early access** to promotions
                - ✅ **24/7 customer support**
                """)
                
        with tab2:
            # Recent orders
            st.markdown("### 🛒 Your Recent Orders")
            
            # Sample order data
            orders = [
                {"id": "WM12345", "date": "2023-05-15", "status": "Delivered", "items": 3, "total": "$215.99"},
                {"id": "WM12387", "date": "2023-05-02", "status": "Delivered", "items": 2, "total": "$43.85"},
                {"id": "WM12442", "date": "2023-05-18", "status": "In Transit", "items": 4, "total": "$159.91"},
                {"id": "WM12468", "date": "2023-05-20", "status": "Processing", "items": 1, "total": "$5.99"}
            ]
            
            for order in orders:
                if order["status"] == "Delivered":
                    status_color = "green"
                    status_icon = "✅"
                elif order["status"] == "In Transit":
                    status_color = "orange"
                    status_icon = "🚚"
                else:
                    status_color = "blue"
                    status_icon = "⏳"
                
                st.markdown(f"""
                <div style="padding: 15px; margin-bottom: 15px; background-color: rgba(255,255,255,0.1); border-radius: 10px;">
                    <div style="display: flex; justify-content: space-between;">
                        <div><strong>Order #{order["id"]}</strong></div>
                        <div style="color: {status_color};">{status_icon} {order["status"]}</div>
                    </div>
                    <hr style="margin: 10px 0; opacity: 0.2;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>Date: {order["date"]}</div>
                        <div>Items: {order["items"]}</div>
                        <div><strong>Total: {order["total"]}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Track button for in-transit order
            if st.button("🗺️ Track Order WM12442", use_container_width=True):
                st.info("🚚 Your order is currently in transit and expected to arrive by May 22, 2023")
                
                # Simple map showing delivery route
                import folium
                from streamlit_folium import folium_static
                
                # Create tracking map
                m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
                
                # Add warehouse and destination markers
                folium.Marker(
                    location=[39.0997, -94.5786],
                    popup="Walmart Distribution Center",
                    icon=folium.Icon(color="blue")
                ).add_to(m)
                
                folium.Marker(
                    location=[39.9526, -75.1652],
                    popup="Your Address",
                    icon=folium.Icon(color="green")
                ).add_to(m)
                
                # Add current location marker
                folium.Marker(
                    location=[40.4406, -79.9959],
                    popup="Current Location",
                    icon=folium.Icon(color="red", icon="truck")
                ).add_to(m)
                
                # Add line connecting points
                folium.PolyLine(
                    locations=[[39.0997, -94.5786], [40.4406, -79.9959], [39.9526, -75.1652]],
                    color="blue",
                    weight=3,
                    opacity=0.7
                ).add_to(m)
                
                # Display map
                folium_static(m)
                
        with tab3:
            # Personalized recommendations
            st.markdown("### ⭐ Recommended for You")
            
            # Sample product recommendations
            products = [
                {"name": "Samsung Galaxy S23", "price": "$799.99", "category": "Electronics", "image": "https://i5.walmartimages.com/seo/SAMSUNG-Galaxy-S23-128GB-Phantom-Black-Unlocked-Smartphone_3f0e176d-8199-4879-a0c5-6e1da8faf71c.6b05e22547fd017560478a59823d5cc1.jpeg", "rating": 4.8},
                {"name": "Apple AirPods Pro", "price": "$249.99", "category": "Electronics", "image": "https://i5.walmartimages.com/seo/Apple-AirPods-Pro-2nd-Generation-with-MagSafe-Case-USB-C_a029bd2c-4284-4239-8a89-8e5a768fec9d.3593c0b965b6848f2ab0f7b6ac7c9a3c.jpeg", "rating": 4.7},
                {"name": "Nike Dri-FIT T-Shirt", "price": "$24.95", "category": "Clothing", "image": "https://i5.walmartimages.com/seo/Nike-Men-s-Dri-FIT-Legend-2-0-Short-Sleeve-T-Shirt_320d3d0c-4c50-4752-a5a8-84394d546438.0c71528e6ac009cf37c05d8837d0f632.jpeg", "rating": 4.5},
                {"name": "Instant Pot Duo", "price": "$89.95", "category": "Home Goods", "image": "https://i5.walmartimages.com/seo/Instant-Pot-Duo-7-in-1-Electric-Pressure-Cooker-Slow-Cooker-Rice-Cooker-Steamer-Saut-Yogurt-Maker-and-Warmer-6-Quart-14-One-Touch-Programs_20209369-ec05-4e41-a8a7-7ba012e0e560.caeea1a53b8302967bd72ed16055988c.jpeg", "rating": 4.6},
            ]
            
            # Display products in a grid
            prod_cols = st.columns(4)
            
            for i, product in enumerate(products):
                with prod_cols[i]:
                    st.image(product["image"], use_column_width=True)
                    st.markdown(f"**{product['name']}**")
                    st.markdown(f"<span style='color: #0071ce; font-weight: bold;'>{product['price']}</span>", unsafe_allow_html=True)
                    st.markdown(f"⭐ {product['rating']}/5.0")
                    st.button(f"Add to Cart", key=f"add_{i}", use_container_width=True)
            
            # Personalized savings
            st.markdown("### 💰 Your Personalized Savings")
            
            # Display current deals
            st.markdown("""
            <div style="background-color: #fdf9e5; padding: 15px; border-radius: 10px; margin: 20px 0; color: #333;">
                <h4 style="margin-top: 0; color: #e67300;">🏷️ Special Offers Just For You</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>15% OFF</strong> your next electronics purchase with code <code>TECH15</code></li>
                    <li><strong>BOGO 50% OFF</strong> on all Nike apparel this weekend</li>
                    <li><strong>$10 CREDIT</strong> when you spend $50+ on groceries</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Call to action
            if st.button("🛍️ Browse More Recommendations", use_container_width=True):
                st.info("Taking you to your personalized shopping recommendations...")
                
            # Recently viewed
            st.markdown("### 👀 Recently Viewed")
            
            viewed_cols = st.columns(5)
            
            recent_items = ["iPhone Charger", "Levi's Jeans", "Cereal", "Running Shoes", "HDMI Cable"]
            
            for i, item in enumerate(recent_items):
                with viewed_cols[i]:
                    st.markdown(f"**{item}**")
    
    # Display the selected tab with modern container
    st.markdown("---")
    st.markdown(f"## {selected_tab}")
    
    # Tab content in modern container
    tab_container_html = """
    <div style="
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        min-height: 600px;
    ">
    """
    st.markdown(tab_container_html, unsafe_allow_html=True)
    
    # Display the selected tab based on user role
    if is_admin():
        TABS[selected_tab].app()
    else:
        # For customer role, access the available tabs dictionary defined in the sidebar
        available_tabs = {
            "📦 Orders": TABS["📦 Orders"],
            "📚 Inventory": TABS["📚 Inventory"],
            "🚚 Delivery": TABS["🚚 Delivery"],
            "🔗 Supply Chain": TABS["🔗 Supply Chain"]
        }
        available_tabs[selected_tab].app()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Modern Footer
st.markdown("---")
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px 30px;
    border-radius: 20px;
    margin: 40px 0 20px 0;
    text-align: center;
">
    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
        <div style="margin: 10px;">
            <div style="font-weight: 600; margin-bottom: 5px;">🛒 Walmart Logistics</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Advanced Operations Platform</div>
        </div>
        <div style="margin: 10px;">
            <div style="font-weight: 600; margin-bottom: 5px;">📞 24/7 Support</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">1-800-WALMART</div>
        </div>
        <div style="margin: 10px;">
            <div style="font-weight: 600; margin-bottom: 5px;">🔒 Secure & Compliant</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">SOC 2 Type II Certified</div>
        </div>
        <div style="margin: 10px;">
            <div style="font-weight: 600; margin-bottom: 5px;">🌍 Global Operations</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Serving 24 Countries</div>
        </div>
    </div>
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
        <div style="font-size: 0.9rem; opacity: 0.8;">
            © 2025 Walmart Inc. • Powered by Advanced AI & Machine Learning • Version 3.1.0
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Notifications with animations
if st.session_state.notifications:
    notification = st.session_state.notifications.pop(0)
    
    notification_types = {
        'success': ('🟢', '#10b981', 'Success'),
        'warning': ('🟡', '#f59e0b', 'Warning'),
        'error': ('🔴', '#ef4444', 'Error'),
        'info': ('🔵', '#3b82f6', 'Info')
    }
    
    icon, color, type_name = notification_types.get(notification['type'], notification_types['info'])
    
    st.markdown(f"""
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        max-width: 400px;
        animation: slideIn 0.5s ease-out;
    ">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 1.2rem; margin-right: 12px;">{icon}</span>
            <div>
                <div style="font-weight: 600; color: {color}; margin-bottom: 4px;">{type_name}</div>
                <div style="color: #374151; font-size: 0.9rem;">{notification['message']}</div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes slideIn {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)
