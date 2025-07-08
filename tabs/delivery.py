import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import folium_static
import requests
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
from utils.api import get_data, put_data
from utils.helpers import display_kpi_metrics, format_date, show_notification

def create_google_maps_embed(origin, destination, api_key=None):
    """Create an embedded Google Maps with directions - improved version with better fallback"""
    if not origin or not destination:
        return create_static_route_display(origin, destination)
    
    try:
        origin_encoded = origin.replace(" ", "+").replace(",", "%2C")
        destination_encoded = destination.replace(" ", "+").replace(",", "%2C")
        
        # Try multiple Google Maps approaches
        maps_embed_options = [
            # Option 1: Standard Google Maps directions
            f"""
            <div style="width: 100%; height: 400px; background: #f0f2f6; border-radius: 10px; padding: 20px; text-align: center;">
                <iframe
                    width="100%"
                    height="360"
                    frameborder="0"
                    style="border:0; border-radius: 8px;"
                    referrerpolicy="no-referrer-when-downgrade"
                    src="https://www.google.com/maps/embed/v1/directions?key=AIzaSyBXPXGSDK8r8OdWGQRlcJ1oX9rHhYvT_demo&origin={origin_encoded}&destination={destination_encoded}&mode=driving"
                    allowfullscreen>
                </iframe>
            </div>
            """,
            # Option 2: Google Maps search fallback
            f"""
            <div style="width: 100%; height: 400px; background: #f0f2f6; border-radius: 10px; padding: 20px;">
                <h4 style="color: #1f77b4; margin-bottom: 15px;">📍 Route Information</h4>
                <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <strong>🚀 Origin:</strong> {origin}<br>
                    <strong>🎯 Destination:</strong> {destination}
                </div>
                <a href="https://www.google.com/maps/dir/{origin_encoded}/{destination_encoded}" 
                   target="_blank" 
                   style="display: inline-block; background: #4285f4; color: white; padding: 10px 20px; 
                          text-decoration: none; border-radius: 5px; font-weight: bold;">
                    🗺️ Open in Google Maps
                </a>
            </div>
            """
        ]
        
        return maps_embed_options[1]  # Use the more reliable option
        
    except Exception as e:
        return create_static_route_display(origin, destination, error=str(e))

def create_static_route_display(origin, destination, error=None):
    """Create a static route display when Google Maps fails"""
    return f"""
    <div style="width: 100%; height: 400px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; padding: 20px; color: white; text-align: center;">
        <h3 style="color: white; margin-bottom: 20px;">🗺️ Route Overview</h3>
        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 8px; margin: 20px 0;">
            <div style="margin-bottom: 15px;">
                <strong>🚀 From:</strong><br>
                <span style="font-size: 16px;">{origin or 'Walmart Distribution Center'}</span>
            </div>
            <div style="margin-bottom: 15px;">
                <strong>🎯 To:</strong><br>
                <span style="font-size: 16px;">{destination or 'Customer Location'}</span>
            </div>
            <div style="margin-bottom: 15px;">
                <strong>📊 Estimated Distance:</strong> 12.5 km<br>
                <strong>⏱️ Estimated Time:</strong> 18 minutes
            </div>
        </div>
        {f'<p style="color: #ffeb3b; font-size: 12px;">Note: {error}</p>' if error else ''}
        <p style="color: #b3e5fc; font-size: 14px;">📍 Using simulation mode for route display</p>
    </div>
    """

def simulate_live_tracking_data():
    """Simulate live tracking data for demonstration"""
    agents = ["Driver A", "Driver B", "Driver C", "Driver D", "Driver E"]
    statuses = ["Out for Delivery", "In Transit", "Delivered", "Delayed", "Loading"]
    
    tracking_data = []
    for i in range(10):
        tracking_data.append({
            "delivery_id": f"DEL{1000 + i}",
            "order_id": f"ORD{2000 + i}",
            "customer_name": f"Customer {chr(65 + i)}",
            "delivery_address": f"{100 + i} Main St, City {chr(65 + i)}",
            "agent_name": random.choice(agents),
            "vehicle_id": f"VH{100 + i}",
            "status": random.choice(statuses),
            "eta": datetime.datetime.now() + datetime.timedelta(minutes=random.randint(15, 120)),
            "progress": random.randint(10, 100),
            "latitude": 40.7128 + random.uniform(-0.1, 0.1),
            "longitude": -74.0060 + random.uniform(-0.1, 0.1),
            "distance_remaining": f"{random.uniform(0.5, 15.0):.1f} km",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "priority": random.choice(["High", "Medium", "Low"]),
            "delivery_window": f"{random.randint(9, 17)}:00 - {random.randint(17, 21)}:00"
        })
    
    return tracking_data

def create_live_map_with_markers(tracking_data):
    """Create a Folium map with live delivery markers"""
    center_lat = sum([item['latitude'] for item in tracking_data]) / len(tracking_data)
    center_lon = sum([item['longitude'] for item in tracking_data]) / len(tracking_data)
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    for delivery in tracking_data:
        color = {
            "Out for Delivery": "blue",
            "In Transit": "orange", 
            "Delivered": "green",
            "Delayed": "red",
            "Loading": "purple"
        }.get(delivery['status'], "gray")
        
        popup_text = f"""
        <b>{delivery['delivery_id']}</b><br>
        Customer: {delivery['customer_name']}<br>
        Agent: {delivery['agent_name']}<br>
        Status: {delivery['status']}<br>
        ETA: {delivery['eta'].strftime('%H:%M')}<br>
        Progress: {delivery['progress']}%
        """
        
        folium.Marker(
            location=[delivery['latitude'], delivery['longitude']],
            popup=folium.Popup(popup_text, max_width=200),
            tooltip=f"{delivery['delivery_id']} - {delivery['status']}",
            icon=folium.Icon(color=color, icon='truck', prefix='fa')
        ).add_to(m)
    
    return m

def display_delivery_notifications():
    """Display delivery notifications and alerts"""
    notifications = [
        {"type": "warning", "message": "DEL1002 is running 15 minutes late due to traffic"},
        {"type": "success", "message": "DEL1001 successfully delivered to Customer A"},
        {"type": "error", "message": "DEL1005 - Vehicle breakdown reported, backup assigned"},
        {"type": "info", "message": "DEL1003 - Customer requested delivery time change"}
    ]
    
    for notif in notifications:
        if notif["type"] == "warning":
            st.warning(f"⚠️ {notif['message']}")
        elif notif["type"] == "success":
            st.success(f"✅ {notif['message']}")
        elif notif["type"] == "error":
            st.error(f"🚨 {notif['message']}")
        else:
            st.info(f"ℹ️ {notif['message']}")

def create_delivery_analytics():
    """Create delivery analytics charts"""
    dates = pd.date_range(start='2025-01-01', end='2025-01-07', freq='D')
    delivery_data = {
        'Date': dates,
        'Total_Deliveries': [45, 52, 38, 61, 49, 67, 55],
        'On_Time': [41, 48, 35, 56, 44, 62, 51],
        'Delayed': [4, 4, 3, 5, 5, 5, 4]
    }
    
    df = pd.DataFrame(delivery_data)
    df['On_Time_Rate'] = (df['On_Time'] / df['Total_Deliveries'] * 100).round(1)
    
    return df

def create_delivery_heatmap(tracking_data):
    """Create a heatmap of delivery density"""
    regions = ["Downtown", "Suburbs North", "Suburbs South", "Industrial", "Residential East", "Residential West"]
    delivery_counts = [45, 32, 28, 15, 38, 25]
    
    fig = px.bar(
        x=regions, 
        y=delivery_counts,
        title="Delivery Density by Region",
        labels={'x': 'Region', 'y': 'Number of Deliveries'},
        color=delivery_counts,
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16
    )
    
    return fig

def display_customer_rating_system():
    """Display customer rating system for completed deliveries"""
    st.header("⭐ Customer Rating & Feedback System")
    
    # Initialize session state for ratings
    if 'customer_ratings' not in st.session_state:
        st.session_state.customer_ratings = []
    
    # Get completed deliveries
    tracking_data = simulate_live_tracking_data()
    completed_deliveries = [d for d in tracking_data if d['status'] == 'Delivered']
    
    if not completed_deliveries:
        st.info("📦 No completed deliveries available for rating at this time.")
        return
    
    # Display completed deliveries for rating
    st.subheader("📋 Rate Your Recent Deliveries")
    
    for delivery in completed_deliveries:
        # Check if already rated
        existing_rating = next((r for r in st.session_state.customer_ratings if r['delivery_id'] == delivery['delivery_id']), None)
        
        if existing_rating:
            display_existing_rating(delivery, existing_rating)
        else:
            display_rating_form(delivery)

def display_rating_form(delivery):
    """Display rating form for a specific delivery"""
    with st.expander(f"📦 Rate Delivery {delivery['delivery_id']} - {delivery['customer_name']}", expanded=False):
        st.markdown(f"""
        **Order Details:**
        - **Delivery ID:** {delivery['delivery_id']}
        - **Customer:** {delivery['customer_name']}
        - **Address:** {delivery['delivery_address']}
        - **Driver:** {delivery['agent_name']}
        - **Delivered:** {delivery['eta'].strftime('%Y-%m-%d %H:%M')}
        """)
        
        # Create rating form
        with st.form(f"rating_form_{delivery['delivery_id']}"):
            st.markdown("#### ⭐ Rate Your Experience")
            
            # Product Quality Rating
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📦 Product Quality:**")
                product_rating = st.select_slider(
                    "Product Rating",
                    options=[1, 2, 3, 4, 5],
                    value=5,
                    format_func=lambda x: "⭐" * x,
                    key=f"product_rating_{delivery['delivery_id']}"
                )
                
                product_feedback = st.text_area(
                    "Product Feedback",
                    placeholder="How was the product quality?",
                    key=f"product_feedback_{delivery['delivery_id']}"
                )
            
            with col2:
                st.markdown("**🚚 Delivery Service:**")
                delivery_rating = st.select_slider(
                    "Delivery Rating",
                    options=[1, 2, 3, 4, 5],
                    value=5,
                    format_func=lambda x: "⭐" * x,
                    key=f"delivery_rating_{delivery['delivery_id']}"
                )
                
                delivery_feedback = st.text_area(
                    "Delivery Feedback",
                    placeholder="How was the delivery service?",
                    key=f"delivery_feedback_{delivery['delivery_id']}"
                )
            
            # Overall experience
            st.markdown("**🌟 Overall Experience:**")
            overall_rating = st.select_slider(
                "Overall Rating",
                options=[1, 2, 3, 4, 5],
                value=5,
                format_func=lambda x: "⭐" * x,
                key=f"overall_rating_{delivery['delivery_id']}"
            )
            
            # Additional feedback
            additional_feedback = st.text_area(
                "Additional Comments",
                placeholder="Any additional feedback or suggestions?",
                key=f"additional_feedback_{delivery['delivery_id']}"
            )
            
            # Would recommend
            recommend = st.checkbox("I would recommend this service", value=True, key=f"recommend_{delivery['delivery_id']}")
            
            # Submit rating
            if st.form_submit_button("📝 Submit Rating", use_container_width=True):
                rating_data = {
                    'delivery_id': delivery['delivery_id'],
                    'customer_name': delivery['customer_name'],
                    'order_id': delivery['order_id'],
                    'product_rating': product_rating,
                    'product_feedback': product_feedback,
                    'delivery_rating': delivery_rating,
                    'delivery_feedback': delivery_feedback,
                    'overall_rating': overall_rating,
                    'additional_feedback': additional_feedback,
                    'recommend': recommend,
                    'timestamp': datetime.datetime.now(),
                    'driver_name': delivery['agent_name']
                }
                
                # Save rating
                st.session_state.customer_ratings.append(rating_data)
                st.success("✅ Thank you for your feedback! Your rating has been submitted.")
                st.rerun()

def display_existing_rating(delivery, rating):
    """Display existing rating for a delivery"""
    with st.expander(f"✅ Rated: {delivery['delivery_id']} - {delivery['customer_name']}", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📦 Product Rating:**")
            st.markdown("⭐" * rating['product_rating'])
            if rating['product_feedback']:
                st.markdown(f"*{rating['product_feedback']}*")
        
        with col2:
            st.markdown("**🚚 Delivery Rating:**")
            st.markdown("⭐" * rating['delivery_rating'])
            if rating['delivery_feedback']:
                st.markdown(f"*{rating['delivery_feedback']}*")
        
        st.markdown("**🌟 Overall Rating:**")
        st.markdown("⭐" * rating['overall_rating'])
        
        if rating['additional_feedback']:
            st.markdown(f"**Additional Comments:** {rating['additional_feedback']}")
        
        if rating['recommend']:
            st.success("✅ Customer recommends this service")
        
        st.markdown(f"**Rated on:** {rating['timestamp'].strftime('%Y-%m-%d %H:%M')}")

def display_rating_analytics():
    """Display rating analytics for management"""
    st.header("📊 Customer Rating Analytics")
    
    if 'customer_ratings' not in st.session_state or not st.session_state.customer_ratings:
        st.info("📊 No ratings available yet. Ratings will appear here once customers start rating deliveries.")
        return
    
    ratings = st.session_state.customer_ratings
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_product_rating = sum(r['product_rating'] for r in ratings) / len(ratings)
        st.metric("📦 Avg Product Rating", f"{avg_product_rating:.1f}⭐")
    
    with col2:
        avg_delivery_rating = sum(r['delivery_rating'] for r in ratings) / len(ratings)
        st.metric("🚚 Avg Delivery Rating", f"{avg_delivery_rating:.1f}⭐")
    
    with col3:
        avg_overall_rating = sum(r['overall_rating'] for r in ratings) / len(ratings)
        st.metric("🌟 Avg Overall Rating", f"{avg_overall_rating:.1f}⭐")
    
    with col4:
        recommend_rate = sum(1 for r in ratings if r['recommend']) / len(ratings) * 100
        st.metric("👍 Recommendation Rate", f"{recommend_rate:.1f}%")
    
    # Rating distribution
    st.subheader("📈 Rating Distribution")
    
    import plotly.express as px
    
    # Create rating distribution data
    rating_data = []
    for rating in ratings:
        rating_data.extend([
            {'Type': 'Product Quality', 'Rating': rating['product_rating']},
            {'Type': 'Delivery Service', 'Rating': rating['delivery_rating']},
            {'Type': 'Overall Experience', 'Rating': rating['overall_rating']}
        ])
    
    if rating_data:
        rating_df = pd.DataFrame(rating_data)
        fig = px.histogram(rating_df, x='Rating', color='Type', nbins=5, 
                          title='Customer Rating Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent feedback
    st.subheader("💬 Recent Customer Feedback")
    
    recent_ratings = sorted(ratings, key=lambda x: x['timestamp'], reverse=True)[:5]
    
    for rating in recent_ratings:
        with st.expander(f"Rating from {rating['customer_name']} - {rating['timestamp'].strftime('%Y-%m-%d')}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Product:** {'⭐' * rating['product_rating']}")
            with col2:
                st.markdown(f"**Delivery:** {'⭐' * rating['delivery_rating']}")
            with col3:
                st.markdown(f"**Overall:** {'⭐' * rating['overall_rating']}")
            
            if rating['product_feedback']:
                st.markdown(f"**Product Feedback:** {rating['product_feedback']}")
            
            if rating['delivery_feedback']:
                st.markdown(f"**Delivery Feedback:** {rating['delivery_feedback']}")
            
            if rating['additional_feedback']:
                st.markdown(f"**Additional Comments:** {rating['additional_feedback']}")

def create_interactive_route_tracker(selected_delivery):
    """Create an interactive route progress tracker"""
    progress = selected_delivery['progress']
    
    # Create a visual route progress bar with milestones
    route_html = f"""
    <div style="width: 100%; background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h4 style="color: #2c3e50; margin-bottom: 20px;">🛣️ Route Progress Tracker</h4>
        
        <!-- Progress Bar -->
        <div style="background: #e9ecef; height: 8px; border-radius: 4px; margin: 20px 0; position: relative;">
            <div style="background: linear-gradient(90deg, #28a745 0%, #20c997 100%); 
                        height: 100%; width: {progress}%; border-radius: 4px; 
                        transition: width 0.5s ease;"></div>
            <div style="position: absolute; right: 10px; top: -25px; 
                        color: #495057; font-weight: bold;">{progress}% Complete</div>
        </div>
        
        <!-- Route Milestones -->
        <div style="display: flex; justify-content: space-between; margin: 20px 0;">
            <div style="text-align: center; {'color: #28a745; font-weight: bold;' if progress >= 0 else 'color: #6c757d;'}">
                <div style="width: 20px; height: 20px; border-radius: 50%; 
                           {'background: #28a745;' if progress >= 0 else 'background: #dee2e6;'} 
                           margin: 0 auto 5px;"></div>
                <small>📦 Picked Up</small>
            </div>
            <div style="text-align: center; {'color: #28a745; font-weight: bold;' if progress >= 25 else 'color: #6c757d;'}">
                <div style="width: 20px; height: 20px; border-radius: 50%; 
                           {'background: #28a745;' if progress >= 25 else 'background: #dee2e6;'} 
                           margin: 0 auto 5px;"></div>
                <small>🚛 In Transit</small>
            </div>
            <div style="text-align: center; {'color: #28a745; font-weight: bold;' if progress >= 50 else 'color: #6c757d;'}">
                <div style="width: 20px; height: 20px; border-radius: 50%; 
                           {'background: #28a745;' if progress >= 50 else 'background: #dee2e6;'} 
                           margin: 0 auto 5px;"></div>
                <small>🏙️ In Area</small>
            </div>
            <div style="text-align: center; {'color: #28a745; font-weight: bold;' if progress >= 75 else 'color: #6c757d;'}">
                <div style="width: 20px; height: 20px; border-radius: 50%; 
                           {'background: #28a745;' if progress >= 75 else 'background: #dee2e6;'} 
                           margin: 0 auto 5px;"></div>
                <small>🏠 Near Delivery</small>
            </div>
            <div style="text-align: center; {'color: #28a745; font-weight: bold;' if progress >= 100 else 'color: #6c757d;'}">
                <div style="width: 20px; height: 20px; border-radius: 50%; 
                           {'background: #28a745;' if progress >= 100 else 'background: #dee2e6;'} 
                           margin: 0 auto 5px;"></div>
                <small>✅ Delivered</small>
            </div>
        </div>
        
        <!-- Current Status -->
        <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">
            <strong>📍 Current Status:</strong> {selected_delivery['status']}<br>
            <strong>🕐 ETA:</strong> {selected_delivery['eta'].strftime('%H:%M')}<br>
            <strong>📞 Driver:</strong> {selected_delivery['agent_name']} ({selected_delivery['phone']})
        </div>
    </div>
    """
    
    return route_html

def app():
    st.header("🚚 Live Delivery Tracking & Management")
    
    # Real-time status banner
    st.success("📡 **Live Tracking Active**: Real-time GPS monitoring, route optimization, and delivery analytics!")
    
    # Get simulated live tracking data
    tracking_data = simulate_live_tracking_data()
    
    # Key Performance Indicators
    total_deliveries = len(tracking_data)
    out_for_delivery = len([d for d in tracking_data if d['status'] == 'Out for Delivery'])
    delivered = len([d for d in tracking_data if d['status'] == 'Delivered'])
    delayed = len([d for d in tracking_data if d['status'] == 'Delayed'])
    on_time_rate = ((delivered / total_deliveries) * 100) if total_deliveries > 0 else 0
    
    # KPI Dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚚 Active Deliveries", out_for_delivery, delta=f"+{out_for_delivery-3} since morning")
    with col2:
        st.metric("✅ Completed Today", delivered, delta=f"+{delivered} delivered")
    with col3:
        st.metric("⏰ Delayed", delayed, delta=f"{delayed} alerts", delta_color="inverse")
    with col4:
        st.metric("📊 On-Time Rate", f"{on_time_rate:.1f}%", delta="2.3%")
    
    # Notification Panel
    st.subheader("🔔 Live Notifications")
    display_delivery_notifications()
    
    # Main Dashboard Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ Live Map Tracking", "📋 Delivery Orders", "📊 Analytics Dashboard", "⚙️ Management Tools", "⭐ Customer Ratings"])
    
    with tab1:
        st.subheader("🗺️ Real-Time GPS Tracking")
        
        # Auto-refresh toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("📍 Live tracking of all delivery vehicles with GPS coordinates and route progress")
        with col2:
            auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
        
        # Live map with delivery markers
        live_map = create_live_map_with_markers(tracking_data)
        folium_static(live_map, width=1200, height=500)
        
        # Auto-refresh functionality
        if auto_refresh:
            time.sleep(1)
            st.rerun()
        
        # Route Progress Section
        st.subheader("📈 Route Progress Tracking")
        
        # Select delivery for detailed tracking
        delivery_ids = [d['delivery_id'] for d in tracking_data if d['status'] in ['Out for Delivery', 'In Transit']]
        if delivery_ids:
            selected_delivery_id = st.selectbox("Select delivery to track:", delivery_ids)
            
            selected_delivery = next((d for d in tracking_data if d['delivery_id'] == selected_delivery_id), None)
            
            if selected_delivery:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🚛 Vehicle", selected_delivery['vehicle_id'])
                    st.metric("👤 Driver", selected_delivery['agent_name'])
                
                with col2:
                    st.metric("📍 Distance Left", selected_delivery['distance_remaining'])
                    eta_str = selected_delivery['eta'].strftime('%H:%M')
                    st.metric("⏰ ETA", eta_str)
                
                with col3:
                    progress = selected_delivery['progress']
                    st.metric("📊 Route Progress", f"{progress}%")
                    st.progress(progress / 100)
                
                # Interactive Route Tracker
                st.subheader(f"🛣️ Route Progress for {selected_delivery_id}")
                route_tracker = create_interactive_route_tracker(selected_delivery)
                components.html(route_tracker, height=300)
                
                # Embedded Google Maps for detailed route
                st.subheader(f"🗺️ Detailed Route for {selected_delivery_id}")
                origin = "Walmart Distribution Center, 508 SW 8th St, Bentonville, AR 72716"
                destination = selected_delivery['delivery_address']
                
                maps_embed = create_google_maps_embed(origin, destination)
                components.html(maps_embed, height=420)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📞 Call Driver", use_container_width=True):
                        st.success(f"📞 Calling {selected_delivery['agent_name']} at {selected_delivery['phone']}")
                
                with col2:
                    if st.button("💬 Send Message", use_container_width=True):
                        st.success(f"💬 Message sent to {selected_delivery['agent_name']}")
                
                with col3:
                    if st.button("🚨 Emergency Alert", use_container_width=True):
                        st.error(f"🚨 Emergency alert sent for {selected_delivery_id}")
    
    with tab2:
        st.subheader("📋 Delivery Orders Management")
        
        # Filters and Search
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status:",
                options=["Out for Delivery", "In Transit", "Delivered", "Delayed", "Loading"],
                default=["Out for Delivery", "In Transit", "Delayed"]
            )
        
        with col2:
            agents = list(set([d['agent_name'] for d in tracking_data]))
            agent_filter = st.selectbox("Filter by Agent:", ["All"] + agents)
        
        with col3:
            priority_filter = st.selectbox("Filter by Priority:", ["All", "High", "Medium", "Low"])
        
        with col4:
            search_term = st.text_input("🔍 Search Order/Customer:")
        
        # Filter data
        filtered_data = tracking_data
        
        if status_filter:
            filtered_data = [d for d in filtered_data if d['status'] in status_filter]
        
        if agent_filter != "All":
            filtered_data = [d for d in filtered_data if d['agent_name'] == agent_filter]
        
        if priority_filter != "All":
            filtered_data = [d for d in filtered_data if d['priority'] == priority_filter]
        
        if search_term:
            filtered_data = [d for d in filtered_data if 
                           search_term.lower() in d['order_id'].lower() or 
                           search_term.lower() in d['customer_name'].lower() or
                           search_term.lower() in d['delivery_id'].lower()]
        
        # Display filtered results
        st.write(f"**Showing {len(filtered_data)} of {len(tracking_data)} deliveries**")
        
        # Enhanced delivery table
        if filtered_data:
            for delivery in filtered_data:
                with st.expander(f"🚚 {delivery['delivery_id']} - {delivery['customer_name']} ({delivery['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**📦 Order ID:** {delivery['order_id']}")
                        st.write(f"**👤 Customer:** {delivery['customer_name']}")
                        st.write(f"**📍 Address:** {delivery['delivery_address']}")
                        st.write(f"**📞 Phone:** {delivery['phone']}")
                    
                    with col2:
                        st.write(f"**🚛 Vehicle:** {delivery['vehicle_id']}")
                        st.write(f"**👤 Driver:** {delivery['agent_name']}")
                        status_color = {"Out for Delivery": "🔵", "In Transit": "🟡", "Delivered": "🟢", "Delayed": "🔴", "Loading": "🟣"}
                        st.write(f"**Status:** {status_color.get(delivery['status'], '⚪')} {delivery['status']}")
                        st.write(f"**⚡ Priority:** {delivery['priority']}")
                    
                    with col3:
                        eta_str = delivery['eta'].strftime('%H:%M')
                        st.write(f"**⏰ ETA:** {eta_str}")
                        st.write(f"**📏 Distance:** {delivery['distance_remaining']}")
                        st.write(f"**⏳ Window:** {delivery['delivery_window']}")
                        st.progress(delivery['progress'] / 100, text=f"Progress: {delivery['progress']}%")
                    
                    # Action buttons for each delivery
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("📞 Call", key=f"call_{delivery['delivery_id']}"):
                            st.success(f"Calling {delivery['agent_name']}")
                    with col2:
                        if st.button("💬 Message", key=f"msg_{delivery['delivery_id']}"):
                            st.success(f"Message sent to {delivery['agent_name']}")
                    with col3:
                        if st.button("📍 Track", key=f"track_{delivery['delivery_id']}"):
                            st.info(f"Live tracking for {delivery['delivery_id']}")
                    with col4:
                        if st.button("✅ Complete", key=f"complete_{delivery['delivery_id']}"):
                            st.success(f"Marked {delivery['delivery_id']} as delivered")
        else:
            st.info("No deliveries match the selected filters.")
    
    with tab3:
        st.subheader("📊 Delivery Analytics Dashboard")
        
        # Analytics period selector
        col1, col2 = st.columns(2)
        with col1:
            period = st.selectbox("Analytics Period:", ["Today", "This Week", "This Month", "Custom Range"])
        
        # Delivery analytics charts
        analytics_df = create_delivery_analytics()
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_deliveries = analytics_df['Total_Deliveries'].mean()
            st.metric("📈 Avg Daily Deliveries", f"{avg_deliveries:.0f}")
        with col2:
            overall_on_time = analytics_df['On_Time_Rate'].mean()
            st.metric("⏰ Overall On-Time Rate", f"{overall_on_time:.1f}%")
        with col3:
            total_week = analytics_df['Total_Deliveries'].sum()
            st.metric("📦 Total This Week", total_week)
        with col4:
            peak_day = analytics_df.loc[analytics_df['Total_Deliveries'].idxmax(), 'Date'].strftime('%A')
            st.metric("🏆 Peak Day", peak_day)
        
        # Delivery trend chart
        fig1 = px.line(analytics_df, x='Date', y=['Total_Deliveries', 'On_Time'], 
                      title="Daily Delivery Trends",
                      labels={'value': 'Number of Deliveries', 'variable': 'Metric'})
        st.plotly_chart(fig1, use_container_width=True)
        
        # On-time rate chart
        fig2 = px.bar(analytics_df, x='Date', y='On_Time_Rate',
                     title="Daily On-Time Delivery Rate (%)",
                     color='On_Time_Rate',
                     color_continuous_scale="RdYlGn")
        st.plotly_chart(fig2, use_container_width=True)
        
        # Regional delivery heatmap
        st.subheader("🗺️ Regional Delivery Distribution")
        heatmap_fig = create_delivery_heatmap(tracking_data)
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
        # Agent performance
        st.subheader("👥 Agent Performance Summary")
        
        agent_performance = {}
        for delivery in tracking_data:
            agent = delivery['agent_name']
            if agent not in agent_performance:
                agent_performance[agent] = {'total': 0, 'delivered': 0, 'delayed': 0}
            
            agent_performance[agent]['total'] += 1
            if delivery['status'] == 'Delivered':
                agent_performance[agent]['delivered'] += 1
            elif delivery['status'] == 'Delayed':
                agent_performance[agent]['delayed'] += 1
        
        for agent, stats in agent_performance.items():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**👤 {agent}**")
            with col2:
                st.metric("Total", stats['total'])
            with col3:
                st.metric("Delivered", stats['delivered'])
            with col4:
                success_rate = (stats['delivered'] / stats['total'] * 100) if stats['total'] > 0 else 0
                st.metric("Success Rate", f"{success_rate:.0f}%")
    
    with tab4:
        st.subheader("⚙️ Delivery Management Tools")
        
        # Route optimization
        st.subheader("🛣️ Advanced Route Optimization")
        
        col1, col2 = st.columns(2)
        with col1:
            optimization_type = st.selectbox("Optimization Type:", [
                "Minimize Distance",
                "Minimize Time", 
                "Maximize Deliveries",
                "Fuel Efficiency"
            ])
        
        with col2:
            include_traffic = st.checkbox("Include Real-time Traffic", value=True)
        
        if st.button("🎯 Optimize All Active Routes"):
            with st.spinner("Optimizing routes with AI algorithms..."):
                time.sleep(2)
                st.success("✅ Route optimization completed!")
                st.info("📊 Average delivery time reduced by 12 minutes")
                st.info("⛽ Fuel consumption optimized by 8%")
                st.info("📈 3 additional deliveries can be scheduled")
        
        # Emergency protocols
        st.subheader("🚨 Emergency Protocols")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚨 Emergency Recall All", type="primary"):
                st.error("🚨 Emergency recall initiated for all vehicles")
        
        with col2:
            if st.button("⚠️ Weather Alert"):
                st.warning("⚠️ Weather alert sent to all delivery agents")
        
        with col3:
            if st.button("🏥 Medical Emergency"):
                st.error("🏥 Medical emergency protocol activated")
    
    with tab5:
        st.subheader("⭐ Customer Rating System")
        
        # Sub-tabs for customer ratings
        rating_tab1, rating_tab2 = st.tabs(["📝 Rate Deliveries", "📊 Rating Analytics"])
        
        with rating_tab1:
            display_customer_rating_system()
        
        with rating_tab2:
            display_rating_analytics()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📡 **Live Updates**: GPS data refreshed every 30 seconds")
    with col2:
        st.info("🗺️ **Coverage**: Real-time tracking for all delivery zones")
    with col3:
        st.info("📞 **Support**: 24/7 emergency dispatch available")
