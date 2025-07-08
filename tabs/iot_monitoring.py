import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import time
import random
from utils.helpers import display_kpi_metrics, show_notification

def app():
    """IoT Monitoring and Smart Warehouse Management"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; text-align: center;">🌐 IoT Monitoring & Smart Warehouse</h1>
        <p style="margin: 10px 0 0 0; text-align: center; font-size: 16px;">
            Real-time sensor data • Smart alerts • Predictive maintenance • Environmental monitoring
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for IoT configuration
    with st.sidebar:
        st.header("⚙️ IoT Configuration")
        
        # Sensor types
        sensor_types = st.multiselect(
            "Active Sensor Types",
            ["Temperature", "Humidity", "Motion", "Weight", "Light", "Air Quality", "Vibration", "Door Status"],
            default=["Temperature", "Humidity", "Motion", "Weight"]
        )
        
        # Refresh rate
        refresh_rate = st.slider("Refresh Rate (seconds)", 1, 60, 5)
        
        # Alert thresholds
        st.subheader("🚨 Alert Thresholds")
        temp_threshold = st.slider("Temperature Alert (°C)", 0, 50, 25)
        humidity_threshold = st.slider("Humidity Alert (%)", 0, 100, 70)
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("Auto-refresh", value=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📡 Live Dashboard", "🔍 Device Management", "📈 Analytics", "🚨 Alerts", "⚙️ Configuration"])
    
    with tab1:
        display_iot_dashboard(sensor_types, temp_threshold, humidity_threshold)
    
    with tab2:
        display_device_management()
    
    with tab3:
        display_iot_analytics()
    
    with tab4:
        display_iot_alerts()
    
    with tab5:
        display_iot_configuration()
    
    # Auto-refresh functionality
    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

def display_iot_dashboard(sensor_types, temp_threshold, humidity_threshold):
    """Display real-time IoT dashboard"""
    st.header("📡 Real-time IoT Dashboard")
    
    # Generate mock sensor data
    current_time = datetime.datetime.now()
    
    # KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        active_sensors = len(sensor_types) * 12  # 12 sensors per type
        st.metric("🔌 Active Sensors", active_sensors, "↑ 2")
    
    with col2:
        alerts_count = random.randint(0, 5)
        st.metric("🚨 Active Alerts", alerts_count, f"↑ {alerts_count}")
    
    with col3:
        system_health = random.uniform(95, 100)
        st.metric("💚 System Health", f"{system_health:.1f}%", "↑ 0.5%")
    
    with col4:
        data_points = random.randint(10000, 15000)
        st.metric("📊 Data Points/Hour", f"{data_points:,}", "↑ 5%")
    
    with col5:
        network_status = "Online"
        st.metric("🌐 Network Status", network_status, "Stable")
    
    # Real-time sensor readings
    st.subheader("📊 Real-time Sensor Readings")
    
    # Create sensor data
    sensor_data = []
    zones = ['A01', 'A02', 'A03', 'B01', 'B02', 'C01', 'C02']
    
    for zone in zones:
        for sensor_type in sensor_types:
            if sensor_type == "Temperature":
                value = random.uniform(18, 30)
                unit = "°C"
                status = "⚠️ Warning" if value > temp_threshold else "✅ Normal"
            elif sensor_type == "Humidity":
                value = random.uniform(40, 80)
                unit = "%"
                status = "⚠️ Warning" if value > humidity_threshold else "✅ Normal"
            elif sensor_type == "Motion":
                value = random.randint(0, 1)
                unit = "Detected" if value else "Clear"
                status = "🔴 Motion" if value else "✅ Clear"
            elif sensor_type == "Weight":
                value = random.uniform(0, 1000)
                unit = "kg"
                status = "✅ Normal"
            elif sensor_type == "Light":
                value = random.uniform(100, 1000)
                unit = "lux"
                status = "✅ Normal"
            elif sensor_type == "Air Quality":
                value = random.uniform(0, 500)
                unit = "AQI"
                status = "⚠️ Warning" if value > 150 else "✅ Good"
            elif sensor_type == "Vibration":
                value = random.uniform(0, 10)
                unit = "mm/s"
                status = "⚠️ Warning" if value > 5 else "✅ Normal"
            elif sensor_type == "Door Status":
                value = random.randint(0, 1)
                unit = "Open" if value else "Closed"
                status = "🔓 Open" if value else "🔒 Closed"
            
            sensor_data.append({
                'Zone': zone,
                'Sensor': sensor_type,
                'Value': value if sensor_type not in ["Motion", "Door Status"] else unit,
                'Unit': unit if sensor_type not in ["Motion", "Door Status"] else "",
                'Status': status,
                'Last Updated': current_time.strftime('%H:%M:%S')
            })
    
    # Display sensor data in a table
    df_sensors = pd.DataFrame(sensor_data)
    st.dataframe(df_sensors, use_container_width=True)
    
    # Sensor trends
    st.subheader("📈 Sensor Trends (Last 24 Hours)")
    
    # Generate trend data
    times = pd.date_range(start=current_time - datetime.timedelta(hours=24), end=current_time, freq='1H')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature trend
        temp_data = []
        for zone in zones[:4]:  # Show first 4 zones
            temps = [random.uniform(18, 30) for _ in times]
            temp_data.extend([{'Time': t, 'Zone': zone, 'Temperature': temp} for t, temp in zip(times, temps)])
        
        df_temp = pd.DataFrame(temp_data)
        fig_temp = px.line(df_temp, x='Time', y='Temperature', color='Zone', 
                          title="Temperature Trends by Zone")
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Humidity trend
        humidity_data = []
        for zone in zones[:4]:
            humidities = [random.uniform(40, 80) for _ in times]
            humidity_data.extend([{'Time': t, 'Zone': zone, 'Humidity': humidity} for t, humidity in zip(times, humidities)])
        
        df_humidity = pd.DataFrame(humidity_data)
        fig_humidity = px.line(df_humidity, x='Time', y='Humidity', color='Zone',
                              title="Humidity Trends by Zone")
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    # Zone heatmap
    st.subheader("🗺️ Zone Environmental Heatmap")
    
    # Create heatmap data
    zone_matrix = np.array([
        [22.5, 24.1, 23.8, 25.2],
        [23.2, 22.9, 24.5, 23.1],
        [24.8, 23.5, 22.2, 24.9]
    ])
    
    fig_heatmap = px.imshow(zone_matrix, 
                           labels=dict(x="Zone Column", y="Zone Row", color="Temperature (°C)"),
                           x=['A01', 'A02', 'A03', 'B01'],
                           y=['Floor 1', 'Floor 2', 'Floor 3'],
                           color_continuous_scale='RdYlBu_r',
                           title="Warehouse Temperature Distribution")
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

def display_device_management():
    """Display IoT device management interface"""
    st.header("🔍 IoT Device Management")
    
    # Device inventory
    st.subheader("📱 Device Inventory")
    
    devices = []
    device_types = ['Temperature Sensor', 'Humidity Sensor', 'Motion Detector', 'Weight Scale', 'Camera', 'Door Sensor']
    statuses = ['Online', 'Offline', 'Maintenance', 'Error']
    
    for i in range(50):
        device = {
            'Device ID': f'IOT-{1000 + i}',
            'Type': random.choice(device_types),
            'Zone': random.choice(['A01', 'A02', 'A03', 'B01', 'B02', 'C01', 'C02']),
            'Status': random.choice(statuses),
            'Battery': f"{random.randint(20, 100)}%" if random.choice([True, False]) else "Wired",
            'Last Seen': (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 180))).strftime('%H:%M'),
            'Firmware': f"v{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
        }
        devices.append(device)
    
    df_devices = pd.DataFrame(devices)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        device_type_filter = st.selectbox("Filter by Type", ['All'] + device_types)
    
    with col2:
        status_filter = st.selectbox("Filter by Status", ['All'] + statuses)
    
    with col3:
        zone_filter = st.selectbox("Filter by Zone", ['All', 'A01', 'A02', 'A03', 'B01', 'B02', 'C01', 'C02'])
    
    # Apply filters
    filtered_df = df_devices.copy()
    if device_type_filter != 'All':
        filtered_df = filtered_df[filtered_df['Type'] == device_type_filter]
    if status_filter != 'All':
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    if zone_filter != 'All':
        filtered_df = filtered_df[filtered_df['Zone'] == zone_filter]
    
    st.dataframe(filtered_df, use_container_width=True)
    
    # Device statistics
    st.subheader("📊 Device Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution
        status_counts = df_devices['Status'].value_counts()
        fig_status = px.pie(values=status_counts.values, names=status_counts.index,
                           title="Device Status Distribution")
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Device types
        type_counts = df_devices['Type'].value_counts()
        fig_types = px.bar(x=type_counts.index, y=type_counts.values,
                          title="Device Types Distribution")
        st.plotly_chart(fig_types, use_container_width=True)
    
    # Device actions
    st.subheader("🔧 Device Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📡 Scan for New Devices"):
            st.success("Scanning for new devices... Found 3 new devices!")
    
    with col2:
        if st.button("🔄 Update All Firmware"):
            st.info("Firmware update initiated for all devices")
    
    with col3:
        if st.button("🔋 Check Battery Status"):
            st.warning("5 devices have low battery")
    
    with col4:
        if st.button("🛠️ Run Diagnostics"):
            st.success("Diagnostics completed. All systems operational.")

def display_iot_analytics():
    """Display IoT analytics and insights"""
    st.header("📈 IoT Analytics & Insights")
    
    # Performance metrics
    st.subheader("📊 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        uptime = random.uniform(98, 100)
        st.metric("⏱️ System Uptime", f"{uptime:.2f}%", "↑ 0.1%")
    
    with col2:
        response_time = random.uniform(50, 200)
        st.metric("⚡ Avg Response Time", f"{response_time:.0f}ms", "↓ 5ms")
    
    with col3:
        data_accuracy = random.uniform(95, 100)
        st.metric("🎯 Data Accuracy", f"{data_accuracy:.1f}%", "↑ 0.3%")
    
    with col4:
        energy_usage = random.uniform(80, 120)
        st.metric("⚡ Energy Usage", f"{energy_usage:.0f}kWh", "↓ 5%")
    
    # Predictive analytics
    st.subheader("🔮 Predictive Analytics")
    
    # Generate predictive data
    future_dates = pd.date_range(start=datetime.datetime.now(), periods=168, freq='H')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature prediction
        temp_predictions = [20 + 5 * np.sin(i/24 * 2 * np.pi) + random.uniform(-1, 1) for i in range(168)]
        df_temp_pred = pd.DataFrame({'Time': future_dates, 'Predicted Temperature': temp_predictions})
        
        fig_temp_pred = px.line(df_temp_pred, x='Time', y='Predicted Temperature',
                               title="Temperature Prediction (Next 7 Days)")
        st.plotly_chart(fig_temp_pred, use_container_width=True)
    
    with col2:
        # Maintenance prediction
        maintenance_prob = [random.uniform(0, 1) for _ in range(168)]
        df_maintenance = pd.DataFrame({'Time': future_dates, 'Maintenance Probability': maintenance_prob})
        
        fig_maintenance = px.line(df_maintenance, x='Time', y='Maintenance Probability',
                                 title="Maintenance Probability Prediction")
        st.plotly_chart(fig_maintenance, use_container_width=True)
    
    # Data insights
    st.subheader("💡 Data Insights")
    
    insights = [
        "🔥 Zone A01 shows consistently higher temperatures during peak hours",
        "💨 Humidity levels spike during weekend operations",
        "🚪 Door sensor data indicates high traffic in Zone B01",
        "⚡ Energy consumption can be optimized by 15% with smart scheduling",
        "📊 Motion patterns suggest workflow optimization opportunities"
    ]
    
    for insight in insights:
        st.info(insight)

def display_iot_alerts():
    """Display IoT alerts and notifications"""
    st.header("🚨 IoT Alerts & Notifications")
    
    # Alert summary
    st.subheader("📋 Alert Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        critical_alerts = random.randint(0, 3)
        st.metric("🔴 Critical", critical_alerts, f"↑ {critical_alerts}")
    
    with col2:
        warning_alerts = random.randint(2, 8)
        st.metric("🟡 Warning", warning_alerts, f"↑ {warning_alerts}")
    
    with col3:
        info_alerts = random.randint(5, 15)
        st.metric("🔵 Info", info_alerts, f"↑ {info_alerts}")
    
    with col4:
        resolved_alerts = random.randint(10, 30)
        st.metric("✅ Resolved", resolved_alerts, f"↑ {resolved_alerts}")
    
    # Active alerts
    st.subheader("⚠️ Active Alerts")
    
    alerts = [
        {"Time": "2 min ago", "Type": "🔴 Critical", "Message": "Temperature sensor IOT-1023 not responding", "Zone": "A01"},
        {"Time": "5 min ago", "Type": "🟡 Warning", "Message": "High humidity detected in Zone C01", "Zone": "C01"},
        {"Time": "12 min ago", "Type": "🔵 Info", "Message": "Door sensor triggered in Zone B02", "Zone": "B02"},
        {"Time": "25 min ago", "Type": "🟡 Warning", "Message": "Low battery on motion detector IOT-1045", "Zone": "A02"},
        {"Time": "1 hour ago", "Type": "🔴 Critical", "Message": "Network connectivity lost to Zone C02", "Zone": "C02"}
    ]
    
    for alert in alerts:
        with st.expander(f"{alert['Type']} - {alert['Message']}"):
            st.write(f"**Time:** {alert['Time']}")
            st.write(f"**Zone:** {alert['Zone']}")
            st.write(f"**Status:** Active")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"Acknowledge", key=f"ack_{alert['Time']}"):
                    st.success("Alert acknowledged")
            with col2:
                if st.button(f"Resolve", key=f"resolve_{alert['Time']}"):
                    st.success("Alert resolved")
            with col3:
                if st.button(f"Escalate", key=f"escalate_{alert['Time']}"):
                    st.warning("Alert escalated to management")
    
    # Alert history
    st.subheader("📊 Alert History")
    
    # Generate alert history data
    dates = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=30), end=datetime.datetime.now(), freq='D')
    alert_history = []
    
    for date in dates:
        alert_history.append({
            'Date': date,
            'Critical': random.randint(0, 5),
            'Warning': random.randint(2, 10),
            'Info': random.randint(5, 20)
        })
    
    df_alerts = pd.DataFrame(alert_history)
    
    fig_alerts = px.line(df_alerts, x='Date', y=['Critical', 'Warning', 'Info'],
                        title="Alert Trends (Last 30 Days)")
    st.plotly_chart(fig_alerts, use_container_width=True)

def display_iot_configuration():
    """Display IoT configuration settings"""
    st.header("⚙️ IoT Configuration Settings")
    
    # System configuration
    st.subheader("🔧 System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Collection Settings**")
        collection_interval = st.slider("Collection Interval (seconds)", 1, 300, 30)
        data_retention = st.slider("Data Retention (days)", 30, 365, 90)
        auto_calibration = st.checkbox("Auto Calibration", value=True)
        
        st.write("**Alert Settings**")
        alert_cooldown = st.slider("Alert Cooldown (minutes)", 1, 60, 5)
        email_alerts = st.checkbox("Email Alerts", value=True)
        sms_alerts = st.checkbox("SMS Alerts", value=False)
    
    with col2:
        st.write("**Network Settings**")
        network_protocol = st.selectbox("Protocol", ["MQTT", "HTTP", "WebSocket"])
        encryption = st.checkbox("Enable Encryption", value=True)
        compression = st.checkbox("Enable Compression", value=True)
        
        st.write("**Maintenance Settings**")
        auto_update = st.checkbox("Auto Firmware Updates", value=True)
        maintenance_window = st.time_input("Maintenance Window Start", value=datetime.time(2, 0))
        backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
    
    # Save configuration
    if st.button("💾 Save Configuration"):
        st.success("Configuration saved successfully!")
    
    # Export/Import configuration
    st.subheader("📁 Configuration Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export Configuration"):
            st.success("Configuration exported to config.json")
    
    with col2:
        uploaded_file = st.file_uploader("📥 Import Configuration", type=['json'])
        if uploaded_file is not None:
            st.success("Configuration imported successfully!")
    
    # System status
    st.subheader("🔍 System Status")
    
    status_data = {
        'Component': ['Database', 'Message Queue', 'API Server', 'Web Interface', 'Monitoring'],
        'Status': ['Online', 'Online', 'Online', 'Online', 'Online'],
        'Uptime': ['99.9%', '99.8%', '99.7%', '99.9%', '99.6%'],
        'Last Check': ['Just now', '1 min ago', '2 min ago', 'Just now', '3 min ago']
    }
    
    df_status = pd.DataFrame(status_data)
    st.dataframe(df_status, use_container_width=True)
