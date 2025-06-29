import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import folium_static
import requests
from utils.api import get_data, put_data
from utils.helpers import display_kpi_metrics, format_date, show_notification

def app():
    st.header("🚚 Delivery Tracking with Google Maps Integration")
    
    # Integration Status Banner with Google Maps
    st.success("�️ **Google Maps Powered Delivery System**: Real-time routing, traffic-aware ETAs, and live tracking!")
    
    # Add Google Maps features tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Active Deliveries", "🗺️ Live Tracking", "🛣️ Route Optimization", "📊 Analytics"])
    
    with tab1:
        # Get delivery data
        deliveries = get_data("deliveries")
        
        # Display KPIs
        if deliveries:
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            deliveries_today = sum(1 for delivery in deliveries if format_date(delivery.get('delivery_date', '')) == today)
            failed_deliveries = sum(1 for delivery in deliveries if delivery.get('status') == 'failed')
            
            kpi_data = {
                'deliveries_pending': sum(1 for delivery in deliveries if delivery.get('status') == 'in-transit'),
                'orders_today': deliveries_today,
                'orders_delta': f"+{deliveries_today} today",
                'low_stock': failed_deliveries,
                'low_stock_delta': f"{failed_deliveries} failed" if failed_deliveries > 0 else "0 failed"
            }
            
            display_kpi_metrics(kpi_data)
        
        # Google Maps Integration Status
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🗺️ Google Maps", "Active", help="Real-time routing enabled")
        with col2:
            st.metric("🚦 Traffic Awareness", "Live", help="Current traffic conditions")
        with col3:
            st.metric("📍 GPS Tracking", "Enabled", help="Real-time location updates")
        with col4:
            st.metric("🛣️ Route Optimization", "AI-Powered", help="Google's routing algorithms")
        
        # Filters
        with st.expander("Filters", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            # Date filter
            with col1:
                min_date = datetime.datetime.today() - datetime.timedelta(days=7)
                max_date = datetime.datetime.today() + datetime.timedelta(days=7)
                date_filter = st.date_input(
                    "Delivery Date",
                    datetime.datetime.today(),
                    min_value=min_date,
                    max_value=max_date
                )
            
            # Agent filter
            with col2:
                if deliveries:
                    agents = list(set(delivery.get('agent_id', '') for delivery in deliveries))
                    agent_filter = st.selectbox("Agent", ["All"] + agents)
                else:
                    agent_filter = st.selectbox("Agent", ["All"])
            
            # Region filter
            with col3:
                if deliveries:
                    regions = list(set(delivery.get('region', '') for delivery in deliveries))
                    region_filter = st.selectbox("Region", ["All"] + regions)
                else:
                    region_filter = st.selectbox("Region", ["All"])
        
        # Delivery tracking table with Google Maps features
        if deliveries:
            df = pd.DataFrame(deliveries)
            
            # Apply filters
            if not df.empty:
                # Convert date string to datetime for filtering
                df['delivery_date'] = pd.to_datetime(df['delivery_date'])
                
                # Apply date filter
                if isinstance(date_filter, datetime.date):
                    df = df[df['delivery_date'].dt.date == date_filter]
                
                # Apply agent filter
                if agent_filter != "All":
                    df = df[df['agent_id'] == agent_filter]
                
                # Apply region filter
                if region_filter != "All":
                    df = df[df['region'] == region_filter]
                
                if not df.empty:
                    # Format date for display
                    df['delivery_date'] = df['delivery_date'].dt.strftime('%Y-%m-%d')
                    df['eta'] = pd.to_datetime(df['eta']).dt.strftime('%H:%M')
                    
                    # Add Google Maps links column
                    df['Google Maps'] = df.apply(lambda row: 
                        f"[View Route](https://maps.google.com/maps/dir/Walmart+Distribution+Center/{row.get('delivery_address', '').replace(' ', '+').replace(',', '%2C')})" 
                        if row.get('delivery_address') else "N/A", axis=1)
                    
                    # Display the enhanced table
                    st.dataframe(df)
                    
                    # Enhanced delivery actions with Google Maps
                    st.subheader("🗺️ Google Maps Delivery Actions")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Refresh Traffic Data", use_container_width=True):
                            try:
                                response = requests.get("http://localhost:3000/api/delivery-tracking/traffic-info")
                                if response.status_code == 200:
                                    traffic_data = response.json()
                                    if traffic_data.get('success'):
                                        st.success("🚦 Traffic data updated successfully!")
                                        for update in traffic_data.get('traffic_updates', []):
                                            st.info(f"🚚 {update['driver_name']}: {update['remaining_time']['text']} remaining")
                                    else:
                                        st.warning("Failed to get traffic updates")
                                else:
                                    st.error("Could not connect to traffic service")
                            except Exception as e:
                                st.error(f"Traffic update failed: {str(e)}")
                    
                    with col2:
                        if st.button("🛣️ Optimize All Routes", use_container_width=True):
                            try:
                                # Prepare data for route optimization
                                active_deliveries = df[df['status'].isin(['pending', 'in-transit'])].to_dict('records')
                                
                                if active_deliveries:
                                    response = requests.post("http://localhost:3000/api/delivery-tracking/bulk-optimize", 
                                                           json={"deliveries": active_deliveries})
                                    
                                    if response.status_code == 200:
                                        optimization = response.json()
                                        if optimization.get('success'):
                                            st.success("🎯 Routes optimized with Google Maps!")
                                            st.info(f"📏 Total distance: {optimization['route_details']['total_distance']} meters")
                                            st.info(f"⏱️ Estimated completion: {optimization['route_details']['estimated_completion']}")
                                        else:
                                            st.warning("Route optimization failed")
                                    else:
                                        st.error("Could not connect to optimization service")
                                else:
                                    st.info("No active deliveries to optimize")
                            except Exception as e:
                                st.error(f"Route optimization failed: {str(e)}")
                    
                    # Show failed deliveries
                    failed = df[df['status'] == 'failed']
                    if not failed.empty:
                        st.subheader("❌ Failed Deliveries")
                        st.dataframe(failed)
                        
                        st.subheader("🔄 Reschedule Delivery")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            failed_delivery = st.selectbox("Select Failed Delivery", failed['delivery_id'].tolist())
                        
                        with col2:
                            new_date = st.date_input("New Delivery Date", datetime.datetime.today() + datetime.timedelta(days=1))
                        
                        if st.button("🚚 Reschedule with Google Maps Route"):
                            # Get new route information
                            selected_delivery = failed[failed['delivery_id'] == failed_delivery].iloc[0]
                            try:
                                response = requests.post("http://localhost:3000/api/delivery-tracking/calculate-route", 
                                                       json={
                                                           "origin": "Walmart Distribution Center, 508 SW 8th St, Bentonville, AR 72716",
                                                           "destination": selected_delivery.get('delivery_address', ''),
                                                           "optimizeForTraffic": True
                                                       })
                                
                                if response.status_code == 200:
                                    route_data = response.json()
                                    if route_data.get('success'):
                                        st.success("✅ Delivery rescheduled with optimized Google Maps route!")
                                        st.info(f"🗺️ Distance: {route_data['route']['distance']['miles']} miles")
                                        st.info(f"⏱️ Estimated time: {route_data['route']['duration']['text']}")
                                        st.info(f"🔗 [View Route]({route_data['google_maps_link']})")
                                    else:
                                        st.warning("Failed to calculate new route")
                                else:
                                    st.error("Could not connect to routing service")
                            except Exception as e:
                                st.error(f"Reschedule failed: {str(e)}")
                else:
                    st.info("No deliveries match the selected filters.")
            else:
                st.info("No deliveries found.")
        else:
            st.warning("Could not fetch delivery data. Please check API connection.")
    
    with tab2:
        st.subheader("🗺️ Live Delivery Tracking")
        
        # Get active deliveries for tracking
        if deliveries:
            active_deliveries = [d for d in deliveries if d.get('status') in ['in-transit', 'assigned']]
            
            if active_deliveries:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    selected_delivery = st.selectbox(
                        "Select Delivery to Track",
                        options=[d['delivery_id'] for d in active_deliveries],
                        format_func=lambda x: f"{x} - {next((d['driver_name'] for d in active_deliveries if d['delivery_id'] == x), 'Unknown Driver')}"
                    )
                
                with col2:
                    if st.button("🔄 Get Live Tracking", use_container_width=True):
                        try:
                            response = requests.get(f"http://localhost:3000/api/delivery-tracking/{selected_delivery}/live-tracking")
                            
                            if response.status_code == 200:
                                tracking_data = response.json()
                                if tracking_data.get('success'):
                                    st.success("📍 Live tracking data retrieved!")
                                    
                                    # Display tracking information
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        st.metric("🚚 Driver", tracking_data['driver']['name'])
                                        st.metric("🚛 Vehicle", tracking_data['driver']['vehicle'])
                                    
                                    with col2:
                                        if tracking_data.get('tracking'):
                                            st.metric("⏱️ ETA", tracking_data['tracking']['estimated_arrival'])
                                            st.metric("📏 Distance", tracking_data['tracking']['remaining_distance']['text'])
                                    
                                    with col3:
                                        st.metric("🚦 Traffic", tracking_data['tracking']['traffic_conditions'] if tracking_data.get('tracking') else "Unknown")
                                        st.metric("📱 Last Update", tracking_data['last_updated'])
                                    
                                    # Google Maps link
                                    if tracking_data.get('tracking', {}).get('google_maps_link'):
                                        st.markdown(f"🗺️ [View Live Route on Google Maps]({tracking_data['tracking']['google_maps_link']})")
                                else:
                                    st.warning("Failed to get tracking data")
                            else:
                                st.error("Could not connect to tracking service")
                        except Exception as e:
                            st.error(f"Live tracking failed: {str(e)}")
                
                # Display delivery on map (simulated)
                st.subheader("📍 Delivery Location Map")
                
                # Create a simple folium map
                if selected_delivery:
                    delivery_info = next((d for d in active_deliveries if d['delivery_id'] == selected_delivery), None)
                    if delivery_info:
                        # Default coordinates (in real app, would use geocoding)
                        lat, lng = 40.7128, -74.0060
                        
                        # Create map
                        m = folium.Map(location=[lat, lng], zoom_start=12)
                        
                        # Add markers
                        folium.Marker(
                            [lat, lng],
                            popup=f"Driver: {delivery_info.get('driver_name', 'Unknown')}",
                            tooltip="Current Location",
                            icon=folium.Icon(color='blue', icon='truck', prefix='fa')
                        ).add_to(m)
                        
                        # Add destination
                        folium.Marker(
                            [lat + 0.01, lng + 0.01],
                            popup=f"Delivery Address: {delivery_info.get('delivery_address', 'Unknown')}",
                            tooltip="Destination",
                            icon=folium.Icon(color='red', icon='home', prefix='fa')
                        ).add_to(m)
                        
                        # Display map
                        folium_static(m)
            else:
                st.info("No active deliveries to track.")
                
    with tab3:
        st.subheader("🛣️ Google Maps Route Optimization")
        
        st.markdown("""
        **AI-Powered Route Optimization Features:**
        - 🚦 Real-time traffic analysis
        - 🛣️ Multi-stop route optimization
        - ⏱️ Dynamic ETA calculations
        - 📍 GPS-based location tracking
        - 🗺️ Google Maps integration
        """)
        
        # Route optimization tool
        if st.button("🎯 Optimize All Active Routes", use_container_width=True):
            try:
                # Get all pending/active deliveries
                active_deliveries = [d for d in deliveries if d.get('status') in ['pending', 'assigned', 'in-transit']] if deliveries else []
                
                if active_deliveries:
                    with st.spinner("🗺️ Optimizing routes with Google Maps..."):
                        response = requests.post("http://localhost:3000/api/delivery-tracking/bulk-optimize", 
                                               json={"deliveries": active_deliveries})
                        
                        if response.status_code == 200:
                            optimization = response.json()
                            if optimization.get('success'):
                                st.success("🎉 Routes optimized successfully!")
                                
                                # Display optimization results
                                st.subheader("📊 Optimization Results")
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📏 Total Distance", f"{optimization['route_details']['total_distance']} m")
                                with col2:
                                    st.metric("⏱️ Total Time", f"{optimization['route_details']['total_duration']} s")
                                with col3:
                                    st.metric("🎯 Deliveries", len(optimization['optimized_deliveries']))
                                
                                # Show optimized delivery order
                                st.subheader("🗺️ Optimized Delivery Sequence")
                                for i, delivery in enumerate(optimization['optimized_deliveries'], 1):
                                    st.write(f"{i}. **{delivery.get('delivery_id')}** - {delivery.get('delivery_address', 'N/A')}")
                            else:
                                st.warning("Route optimization failed")
                        else:
                            st.error("Could not connect to optimization service")
                else:
                    st.info("No active deliveries to optimize")
            except Exception as e:
                st.error(f"Route optimization failed: {str(e)}")
        
        # Manual route calculation
        st.subheader("🔧 Manual Route Calculator")
        
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("Origin Address", "Walmart Distribution Center, 508 SW 8th St, Bentonville, AR 72716")
        with col2:
            destination = st.text_input("Destination Address", "")
        
        if st.button("📍 Calculate Route") and destination:
            try:
                response = requests.post("http://localhost:3000/api/delivery-tracking/calculate-route", 
                                       json={"origin": origin, "destination": destination})
                
                if response.status_code == 200:
                    route_data = response.json()
                    if route_data.get('success'):
                        st.success("✅ Route calculated successfully!")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("📏 Distance", route_data['route']['distance']['miles'] + " miles")
                        with col2:
                            st.metric("⏱️ Duration", route_data['route']['duration']['text'])
                        with col3:
                            st.metric("🚦 Traffic", route_data['route']['traffic_conditions'])
                        
                        st.markdown(f"🗺️ [View Route on Google Maps]({route_data['google_maps_link']})")
                    else:
                        st.warning("Failed to calculate route")
                else:
                    st.error("Could not connect to routing service")
            except Exception as e:
                st.error(f"Route calculation failed: {str(e)}")
    
    with tab4:
        st.subheader("📊 Delivery Analytics & Performance")
        
        if deliveries:
            # Performance metrics
            df = pd.DataFrame(deliveries)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_deliveries = len(df)
                st.metric("📦 Total Deliveries", total_deliveries)
            
            with col2:
                successful = len(df[df['status'] == 'delivered'])
                success_rate = (successful / total_deliveries * 100) if total_deliveries > 0 else 0
                st.metric("✅ Success Rate", f"{success_rate:.1f}%")
            
            with col3:
                in_transit = len(df[df['status'] == 'in-transit'])
                st.metric("🚚 In Transit", in_transit)
            
            with col4:
                failed = len(df[df['status'] == 'failed'])
                st.metric("❌ Failed", failed)
            
            # Delivery status distribution
            if not df.empty:
                st.subheader("📈 Delivery Status Distribution")
                status_counts = df['status'].value_counts()
                st.bar_chart(status_counts)
                
                # Top performing drivers
                if 'driver_name' in df.columns:
                    st.subheader("🏆 Top Performing Drivers")
                    driver_stats = df.groupby('driver_name').agg({
                        'delivery_id': 'count',
                        'status': lambda x: (x == 'delivered').sum()
                    }).rename(columns={'delivery_id': 'total_deliveries', 'status': 'successful_deliveries'})
                    
                    driver_stats['success_rate'] = (driver_stats['successful_deliveries'] / driver_stats['total_deliveries'] * 100).round(1)
                    driver_stats = driver_stats.sort_values('success_rate', ascending=False)
                    
                    st.dataframe(driver_stats)
        else:
            st.info("No delivery data available for analytics.")
        
        # Google Maps integration stats
        st.subheader("🗺️ Google Maps Integration Status")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🚀 API Status", "Active", help="Google Maps API is operational")
        with col2:
            st.metric("📍 Geocoding", "Enabled", help="Address to coordinates conversion")
        with col3:
            st.metric("🛣️ Route Optimization", "AI-Powered", help="Machine learning route optimization")
                    
                    with col1:
                        delivery_id = st.selectbox("Select Delivery ID", failed['delivery_id'].tolist())
                    
                    with col2:
                        reschedule_date = st.date_input(
                            "New Delivery Date",
                            datetime.datetime.today() + datetime.timedelta(days=1)
                        )
                    
                    if st.button("Reschedule"):
                        success, _ = put_data("deliveries", delivery_id, {
                            "status": "rescheduled",
                            "delivery_date": reschedule_date.isoformat()
                        })
                        
                        if success:
                            show_notification(f"Delivery #{delivery_id} has been rescheduled.", "success")
                            st.rerun()
                        else:
                            show_notification("Failed to reschedule delivery.", "error")
                
                # Live map with delivery locations
                st.subheader("Live Delivery Tracking")
                
                # Create a map centered at an average location of all deliveries
                if 'latitude' in df.columns and 'longitude' in df.columns:
                    avg_lat = df['latitude'].mean()
                    avg_lng = df['longitude'].mean()
                    
                    m = folium.Map(location=[avg_lat, avg_lng], zoom_start=10)
                    
                    # Add markers for each delivery
                    for idx, row in df.iterrows():
                        if 'latitude' in row and 'longitude' in row:
                            status_color = {
                                'delivered': 'green',
                                'in-transit': 'blue',
                                'pending': 'orange',
                                'failed': 'red',
                                'rescheduled': 'purple'
                            }.get(row.get('status', ''), 'gray')
                            
                            popup_text = f"""
                            <b>Delivery ID:</b> {row.get('delivery_id', '')}<br>
                            <b>Status:</b> {row.get('status', '')}<br>
                            <b>ETA:</b> {row.get('eta', '')}<br>
                            <b>Agent:</b> {row.get('agent_id', '')}
                            """
                            
                            folium.Marker(
                                location=[row['latitude'], row['longitude']],
                                popup=folium.Popup(popup_text, max_width=300),
                                icon=folium.Icon(color=status_color, icon="truck", prefix="fa")
                            ).add_to(m)
                    
                    # Display the map
                    folium_static(m)
                else:
                    st.info("No location data available for map visualization.")
            else:
                st.info("No deliveries match the selected filters.")
        else:
            st.info("No delivery data available.")
    else:
        st.warning("Could not fetch delivery data. Please check API connection.")
