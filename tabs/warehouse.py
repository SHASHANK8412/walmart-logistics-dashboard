import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from matplotlib.colors import LinearSegmentedColormap
import datetime
import random
import time
import qrcode
from io import BytesIO
import base64
from utils.api import get_data, post_data
from utils.helpers import display_kpi_metrics, show_notification

def app():
    """Main comprehensive warehouse management interface"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; text-align: center;">🏭 Comprehensive Warehouse Management System</h1>
        <p style="margin: 10px 0 0 0; text-align: center; font-size: 16px;">
            Real-time tracking • Inventory control • Space optimization • Multi-location support
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'warehouse_user_role' not in st.session_state:
        st.session_state.warehouse_user_role = 'Admin'
    if 'selected_warehouse' not in st.session_state:
        st.session_state.selected_warehouse = 'WH001'
    
    # Sidebar for user control and navigation
    with st.sidebar:
        st.header("👤 User Access Control")
        
        # User role selection
        user_role = st.selectbox(
            "Current User Role",
            ["Admin", "Warehouse Manager", "Supervisor", "Operator", "Viewer"],
            index=0
        )
        st.session_state.warehouse_user_role = user_role
        
        # Warehouse selection
        st.subheader("🏢 Warehouse Selection")
        warehouses = {
            "WH001": "Main Distribution Center (Dallas, TX)",
            "WH002": "Regional Hub North (Chicago, IL)",
            "WH003": "Regional Hub South (Atlanta, GA)",
            "WH004": "Specialty Warehouse (Austin, TX)"
        }
        
        selected_warehouse = st.selectbox(
            "Select Warehouse",
            list(warehouses.keys()),
            format_func=lambda x: warehouses[x]
        )
        st.session_state.selected_warehouse = selected_warehouse
        
        # Navigation
        st.subheader("📋 WMS Modules")
        page = st.selectbox(
            "Select Module",
            [
                "📊 Dashboard",
                "🗺️ Warehouse Layout",
                "📦 Inventory Management",
                "🏷️ Barcode Scanner",
                "📥 Receiving & Shipping",
                "🚀 Advanced Features",
                "📈 Analytics & Reports",
                "📱 Mobile Operations",
                "⚙️ Settings"
            ]
        )
    
    # Main content area
    if page == "📊 Dashboard":
        display_dashboard()
    elif page == "🗺️ Warehouse Layout":
        display_warehouse_layout()
    elif page == "📦 Inventory Management":
        display_inventory_management()
    elif page == "🏷️ Barcode Scanner":
        display_barcode_scanner()
    elif page == "📥 Receiving & Shipping":
        display_receiving_shipping()
    elif page == "🚀 Advanced Features":
        display_advanced_features()
    elif page == "📈 Analytics & Reports":
        display_analytics_reports()
    elif page == "📱 Mobile Operations":
        display_mobile_operations()
    elif page == "⚙️ Settings":
        display_settings()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #6c757d; padding: 20px;">
        🏭 <strong>Walmart Warehouse Management System</strong> | 
        👤 User: {user_role} | 
        🏢 Warehouse: {warehouses[selected_warehouse]} | 
        🕒 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

def display_dashboard():
    """Display warehouse dashboard with KPIs and quick actions"""
    st.header("📊 Warehouse Management Dashboard")
    
    # Real-time KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📦 Total Inventory", "45,231", "↑ 2.3%")
    
    with col2:
        st.metric("🏢 Active Locations", "4", "→ 0%")
    
    with col3:
        st.metric("⚡ Orders Today", "127", "↑ 15%")
    
    with col4:
        st.metric("📈 Efficiency", "94.2%", "↑ 1.2%")
    
    with col5:
        st.metric("🎯 Accuracy", "99.3%", "↑ 0.8%")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("� New Receipt", use_container_width=True):
            st.session_state.show_receipt_form = True
            st.rerun()
    
    with col2:
        if st.button("� New Shipment", use_container_width=True):
            st.session_state.show_shipment_form = True
            st.rerun()
    
    with col3:
        if st.button("� Item Lookup", use_container_width=True):
            st.session_state.show_item_lookup = True
            st.rerun()
    
    with col4:
        if st.button("📊 Generate Report", use_container_width=True, key="warehouse_dashboard_report"):
            st.session_state.show_report_generator = True
            st.rerun()
    
    # Show forms/interfaces based on session state
    if st.session_state.get('show_receipt_form', False):
        display_receipt_form()
    
    if st.session_state.get('show_shipment_form', False):
        display_shipment_form()
    
    if st.session_state.get('show_item_lookup', False):
        display_item_lookup()
    
    if st.session_state.get('show_report_generator', False):
        display_report_generator()
    
    # Live Activity Feed
    st.subheader("📡 Live Activity Feed")
    
    # Simulate live activities
    activities = [
        {"time": "2 min ago", "action": "Item ABC123 received", "user": "John Doe", "location": "WH001"},
        {"time": "5 min ago", "action": "Pick task completed", "user": "Jane Smith", "location": "Z004"},
        {"time": "8 min ago", "action": "Low stock alert: XYZ789", "user": "System", "location": "WH001"},
        {"time": "12 min ago", "action": "Shipment prepared", "user": "Bob Johnson", "location": "Z005"},
    ]
    
    for activity in activities:
        st.info(f"**{activity['time']}** - {activity['action']} by {activity['user']} @ {activity['location']}")

def display_warehouse_layout():
    """Display warehouse layout and zone management"""
    st.header("🗺️ Warehouse Layout & Zone Management")
    
    # Create warehouse zones
    warehouse_zones = {
        "A01": {"name": "Electronics Zone", "capacity": 1000, "current_stock": 850, "type": "High Value"},
        "A02": {"name": "Grocery Zone", "capacity": 2000, "current_stock": 1600, "type": "Fast Moving"},
        "A03": {"name": "Clothing Zone", "capacity": 1500, "current_stock": 1200, "type": "Seasonal"},
        "B01": {"name": "Bulk Storage", "capacity": 5000, "current_stock": 3500, "type": "Bulk Items"},
        "B02": {"name": "Fragile Items", "capacity": 500, "current_stock": 300, "type": "Special Care"},
        "C01": {"name": "Refrigerated", "capacity": 800, "current_stock": 650, "type": "Temperature Controlled"},
        "C02": {"name": "Hazardous Materials", "capacity": 200, "current_stock": 150, "type": "Restricted Access"},
        "D01": {"name": "Returns Processing", "capacity": 300, "current_stock": 100, "type": "Quality Control"}
    }
    
    # Zone layout visualization
    st.subheader("🏗️ Zone Layout Overview")
    
    cols = st.columns(4)
    for i, (zone_id, zone) in enumerate(warehouse_zones.items()):
        with cols[i % 4]:
            utilization = (zone["current_stock"] / zone["capacity"] * 100) if zone["capacity"] > 0 else 0
            
            # Color coding based on utilization
            if utilization < 50:
                color = "#28a745"  # Green
            elif utilization < 80:
                color = "#ffc107"  # Yellow
            else:
                color = "#dc3545"  # Red
            
            zone_html = f"""
            <div style="
                border: 2px solid {color};
                border-radius: 12px;
                padding: 15px;
                margin: 10px 0;
                background: white;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{zone_id}</h4>
                <p style="margin: 5px 0; color: #6c757d; font-size: 12px;">{zone['name']}</p>
                <p style="margin: 5px 0; color: #6c757d; font-size: 10px;">{zone['type']}</p>
                <div style="background: {color}; color: white; padding: 8px; border-radius: 6px; margin: 10px 0;">
                    <strong>{utilization:.1f}% Full</strong>
                </div>
                <p style="margin: 5px 0; font-size: 11px;">
                    {zone['current_stock']:,} / {zone['capacity']:,} units
                </p>
            </div>
            """
            st.markdown(zone_html, unsafe_allow_html=True)
    
    # Interactive warehouse map
    st.subheader("🗺️ Interactive Warehouse Map")
    
    # Create a simple warehouse layout
    zones_data = []
    for zone_id, zone in warehouse_zones.items():
        zones_data.append({
            'Zone': zone_id,
            'Name': zone['name'],
            'Utilization': zone['current_stock'] / zone['capacity'] * 100,
            'Type': zone['type']
        })
    
    zones_df = pd.DataFrame(zones_data)
    
    # Create bar chart
    fig = px.bar(zones_df, x='Zone', y='Utilization', color='Type', 
                title='Zone Utilization by Type',
                labels={'Utilization': 'Utilization %'})
    st.plotly_chart(fig, use_container_width=True)

def display_inventory_management():
    """Display comprehensive inventory management"""
    st.header("📦 Comprehensive Inventory Management")
    
    # Inventory tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Stock Levels", "🔍 Item Search", "📝 Bulk Actions", "📋 Reports"])
    
    with tab1:
        st.subheader("📊 Current Stock Levels")
        
        # Generate sample inventory data
        inventory_data = []
        products = ["iPhone 15 Pro", "Samsung Galaxy S24", "Dell Laptop", "Nike Air Max", "Adidas Sneakers",
                   "Organic Apples", "Whole Milk", "Bread Loaf", "Chicken Breast", "Salmon Fillet"]
        
        for product in products:
            stock_level = random.randint(0, 500)
            reorder_point = random.randint(20, 100)
            max_stock = random.randint(300, 1000)
            zone = random.choice(["A01", "A02", "A03", "B01", "B02", "C01"])
            
            inventory_data.append({
                "SKU": f"SKU{random.randint(1000, 9999)}",
                "Product": product,
                "Zone": zone,
                "Current Stock": stock_level,
                "Reorder Point": reorder_point,
                "Max Stock": max_stock,
                "Status": "Low Stock" if stock_level < reorder_point else "Normal",
                "Last Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        
        df = pd.DataFrame(inventory_data)
        st.dataframe(df, use_container_width=True)
        
        # Stock alerts
        low_stock_items = df[df["Status"] == "Low Stock"]
        if not low_stock_items.empty:
            st.warning(f"⚠️ {len(low_stock_items)} items are below reorder point!")
    
    with tab2:
        st.subheader("🔍 Advanced Item Search")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Search Products")
            zone_filter = st.selectbox("Filter by Zone", ["All", "A01", "A02", "A03", "B01", "B02", "C01"])
        
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All", "Normal", "Low Stock"])
            category_filter = st.selectbox("Category", ["All", "Electronics", "Clothing", "Grocery"])
        
        with col3:
            min_qty = st.number_input("Min Quantity", min_value=0, value=0)
            max_qty = st.number_input("Max Quantity", min_value=0, value=1000)
        
        if st.button("🔍 Search"):
            st.success("Search completed! Results would be displayed here.")
    
    with tab3:
        st.subheader("📝 Bulk Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Bulk Updates:**")
            
            if st.button("📊 Update Stock Levels", use_container_width=True):
                st.success("Stock levels updated successfully!")
            
            if st.button("🏷️ Update Prices", use_container_width=True):
                st.success("Prices updated successfully!")
            
            if st.button("📍 Move Items", use_container_width=True):
                st.success("Items moved successfully!")
        
        with col2:
            st.markdown("**Import/Export:**")
            
            uploaded_file = st.file_uploader("Import CSV", type="csv")
            if uploaded_file:
                st.success("File uploaded successfully!")
            
            if st.button("📥 Export Inventory", use_container_width=True):
                st.success("Inventory exported successfully!")
    
    with tab4:
        st.subheader("📋 Inventory Reports")
        
        # Report options
        report_type = st.selectbox("Report Type", [
            "Stock Levels Report", "Movement Report", "ABC Analysis", "Cycle Count Report"
        ])
        
        date_range = st.date_input("Date Range", value=[datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()])
        
        if st.button("📊 Generate Report", key="warehouse_inventory_report"):
            st.success(f"{report_type} generated successfully!")

def display_barcode_scanner():
    """Display barcode scanning interface"""
    st.header("🏷️ Barcode/QR Code Scanner")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📱 Scanner Interface")
        
        # Simulate scanner
        st.info("📷 Camera interface would appear here in a real implementation")
        
        # Manual entry option
        st.subheader("⌨️ Manual Entry")
        scanned_code = st.text_input("Enter barcode/QR code manually")
        
        scan_type = st.radio("Scan Type", ["📦 Receive Item", "🔍 Locate Item", "📤 Ship Item", "📊 Count Inventory"])
        
        if st.button("🔍 Process Scan"):
            if scanned_code:
                st.success(f"✅ Processed scan for: {scanned_code}")
                
                # Show scan results
                scan_result = {
                    "Barcode": scanned_code,
                    "Product": random.choice(["iPhone 15", "Samsung TV", "Nike Shoes"]),
                    "Location": f"Zone {random.choice(['A01', 'A02', 'B01'])}",
                    "Quantity": random.randint(1, 100),
                    "Status": "Success"
                }
                
                # st.json(scan_result)  # HIDDEN: Do not show raw code or debug output
    
    with col2:
        st.subheader("🏷️ Generate QR Code")
        
        item_data = st.text_input("Enter item data for QR code")
        
        if item_data:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(item_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for display
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            st.markdown(f'<img src="data:image/png;base64,{img_str}" width="200">', unsafe_allow_html=True)
        
        st.subheader("📋 Scan History")
        
        # Sample scan history
        scan_history = [
            {"Time": "10:30 AM", "Code": "123456789", "Action": "Receive", "Result": "Success"},
            {"Time": "10:25 AM", "Code": "987654321", "Action": "Locate", "Result": "Success"},
            {"Time": "10:20 AM", "Code": "456789123", "Action": "Ship", "Result": "Success"},
            {"Time": "10:15 AM", "Code": "789123456", "Action": "Count", "Result": "Error"}
        ]
        
        for scan in scan_history:
            result_color = "green" if scan["Result"] == "Success" else "red"
            st.markdown(f"**{scan['Time']}** - {scan['Code']} ({scan['Action']}) - <span style='color: {result_color}'>{scan['Result']}</span>", 
                       unsafe_allow_html=True)

def display_receiving_shipping():
    """Display receiving and shipping management"""
    st.header("📥 Receiving & Shipping Management")
    
    tab1, tab2, tab3 = st.tabs(["📥 Receiving", "📤 Shipping", "🚚 Tracking"])
    
    with tab1:
        st.subheader("📥 Goods Receiving")
        
        # Receiving form
        with st.form("receiving_form"):
            st.markdown("#### 📋 New Receipt Entry")
            
            col1, col2 = st.columns(2)
            with col1:
                supplier = st.text_input("Supplier Name")
                purchase_order = st.text_input("Purchase Order #")
                receipt_date = st.date_input("Receipt Date", datetime.date.today())
            
            with col2:
                delivery_note = st.text_input("Delivery Note #")
                received_by = st.text_input("Received By")
                zone_assignment = st.selectbox("Assign to Zone", ["A01", "A02", "A03", "B01", "B02", "C01"])
            
            # Items received
            st.markdown("#### 📦 Items Received")
            num_items = st.number_input("Number of Items", min_value=1, max_value=10, value=1)
            
            if st.form_submit_button("📥 Process Receipt"):
                st.success("✅ Receipt processed successfully!")
                
                receipt_summary = {
                    "Receipt ID": f"REC{random.randint(10000, 99999)}",
                    "Supplier": supplier,
                    "PO Number": purchase_order,
                    "Date": receipt_date.strftime("%Y-%m-%d"),
                    "Items Count": num_items,
                    "Zone": zone_assignment
                }
                
                # st.json(receipt_summary)  # HIDDEN: Do not show raw code or debug output
    
    with tab2:
        st.subheader("📤 Outgoing Shipments")
        
        # Generate sample shipment data
        shipment_data = []
        for i in range(10):
            shipment_data.append({
                "Shipment ID": f"SHIP{random.randint(10000, 99999)}",
                "Customer": f"Customer {chr(65 + i)}",
                "Order ID": f"ORD{random.randint(1000, 9999)}",
                "Status": random.choice(["Pending", "Picking", "Packed", "Shipped", "Delivered"]),
                "Priority": random.choice(["High", "Medium", "Low"]),
                "Ship Date": (datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),
                "Carrier": random.choice(["FedEx", "UPS", "DHL", "USPS"])
            })
        
        shipments_df = pd.DataFrame(shipment_data)
        st.dataframe(shipments_df, use_container_width=True)
        
        # Shipment actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📦 Create New Shipment"):
                st.info("New shipment form would open here")
        with col2:
            if st.button("🏷️ Print Labels"):
                st.success("Labels sent to printer")
        with col3:
            if st.button("📊 Shipment Report"):
                st.info("Generating shipment report...")
    
    with tab3:
        st.subheader("🚚 Live Delivery Tracking")
        
        # Display active deliveries
        active_deliveries = [
            {"Tracking": "TRK123456", "Status": "In Transit", "ETA": "2 hours", "Location": "Dallas, TX"},
            {"Tracking": "TRK789012", "Status": "Out for Delivery", "ETA": "45 minutes", "Location": "Local Hub"},
            {"Tracking": "TRK345678", "Status": "Delivered", "ETA": "Completed", "Location": "Customer"},
        ]
        
        for delivery in active_deliveries:
            status_colors = {"In Transit": "blue", "Out for Delivery": "orange", "Delivered": "green"}
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; 
                        border-left: 4px solid {status_colors.get(delivery['Status'], 'gray')};">
                <strong>{delivery['Tracking']}</strong> - {delivery['Status']}<br>
                📍 {delivery['Location']} | ⏱️ ETA: {delivery['ETA']}
            </div>
            """, unsafe_allow_html=True)

def display_advanced_features():
    """Display advanced WMS features"""
    st.header("🚀 Advanced WMS Features")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📡 RFID Tracking", "🤖 Automation", "🔮 Predictive Analytics", "🌡️ IoT Sensors"])
    
    with tab1:
        st.subheader("📡 RFID Real-time Tracking")
        
        # RFID gate status
        rfid_gates = [
            {"Gate": "RFID_GATE_01", "Name": "Main Entrance", "Status": "Active", "Last Read": "2 min ago"},
            {"Gate": "RFID_GATE_02", "Name": "Shipping Dock", "Status": "Active", "Last Read": "30 sec ago"},
            {"Gate": "RFID_GATE_03", "Name": "Receiving Dock", "Status": "Active", "Last Read": "1 min ago"},
            {"Gate": "RFID_GATE_04", "Name": "Cold Storage", "Status": "Maintenance", "Last Read": "1 hour ago"}
        ]
        
        for gate in rfid_gates:
            status_color = {"Active": "green", "Maintenance": "red", "Offline": "gray"}
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{gate['Name']}** ({gate['Gate']})")
            with col2:
                st.markdown(f"<span style='color: {status_color[gate['Status']]}'>{gate['Status']}</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"📡 {gate['Last Read']}")
        
        # Live RFID readings
        st.subheader("📊 Live RFID Readings")
        
        if st.button("🔄 Refresh Live Data"):
            rfid_readings = []
            for i in range(5):
                rfid_readings.append({
                    "Timestamp": datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 30)),
                    "RFID_Tag": f"RFID{random.randint(100000, 999999)}",
                    "Gate": random.choice(["RFID_GATE_01", "RFID_GATE_02", "RFID_GATE_03"]),
                    "Direction": random.choice(["IN", "OUT"]),
                    "Product": random.choice(["iPhone 15", "Samsung TV", "Nike Shoes", "Organic Milk", "Laptop"])
                })
            
            rfid_df = pd.DataFrame(rfid_readings)
            rfid_df["Timestamp"] = rfid_df["Timestamp"].dt.strftime("%H:%M:%S")
            st.dataframe(rfid_df, use_container_width=True)
    
    with tab2:
        st.subheader("🤖 Warehouse Automation")
        
        # Automation rules
        automation_rules = [
            {"Rule": "Auto Reorder", "Status": "Enabled", "Threshold": "20%", "Action": "Generate PO"},
            {"Rule": "Zone Optimization", "Status": "Enabled", "Frequency": "Daily", "Action": "Rearrange Items"},
            {"Rule": "Pick Wave Planning", "Status": "Enabled", "Batch Size": "10", "Action": "Optimize Routes"}
        ]
        
        for rule in automation_rules:
            with st.expander(f"{rule['Rule']} - {rule['Status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Status:** {rule['Status']}")
                    st.write(f"**Action:** {rule['Action']}")
                with col2:
                    if "Threshold" in rule:
                        st.write(f"**Threshold:** {rule['Threshold']}")
                    if "Frequency" in rule:
                        st.write(f"**Frequency:** {rule['Frequency']}")
                    if "Batch Size" in rule:
                        st.write(f"**Batch Size:** {rule['Batch Size']}")
    
    with tab3:
        st.subheader("🔮 Predictive Analytics")
        
        # Demand forecasting
        st.markdown("#### 📈 Demand Forecasting")
        
        forecast_data = []
        products = ["iPhone 15", "Samsung TV", "Nike Shoes", "Organic Milk", "Laptop"]
        
        for product in products:
            forecast_data.append({
                "Product": product,
                "Current Stock": random.randint(50, 500),
                "Forecasted Demand (7 days)": random.randint(20, 200),
                "Recommended Action": random.choice(["Reorder", "Increase Stock", "Maintain", "Reduce"]),
                "Confidence": f"{random.randint(75, 95)}%"
            })
        
        forecast_df = pd.DataFrame(forecast_data)
        st.dataframe(forecast_df, use_container_width=True)
        
        # Seasonal analysis chart
        st.markdown("#### 🌍 Seasonal Analysis")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        seasonal_data = {
            'Month': months,
            'Electronics': [100, 90, 95, 110, 105, 120, 115, 125, 130, 140, 180, 200],
            'Clothing': [80, 85, 100, 120, 110, 90, 85, 90, 110, 130, 160, 150],
            'Grocery': [120, 115, 110, 105, 108, 125, 130, 128, 115, 110, 140, 160]
        }
        
        seasonal_df = pd.DataFrame(seasonal_data)
        
        fig = px.line(seasonal_df, x='Month', y=['Electronics', 'Clothing', 'Grocery'], 
                     title='Seasonal Demand Patterns')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🌡️ IoT Sensor Network")
        
        # Environmental monitoring
        sensor_data = [
            {"Zone": "Cold Storage A", "Temperature": "2.5°C", "Humidity": "65%", "Status": "Normal"},
            {"Zone": "Cold Storage B", "Temperature": "3.1°C", "Humidity": "68%", "Status": "Warning"},
            {"Zone": "Main Warehouse", "Temperature": "22°C", "Humidity": "45%", "Status": "Normal"},
            {"Zone": "Electronics Zone", "Temperature": "20°C", "Humidity": "40%", "Status": "Normal"}
        ]
        
        for sensor in sensor_data:
            status_color = {"Normal": "green", "Warning": "orange", "Critical": "red"}
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"**{sensor['Zone']}**")
            with col2:
                st.markdown(f"🌡️ {sensor['Temperature']}")
            with col3:
                st.markdown(f"💧 {sensor['Humidity']}")
            with col4:
                st.markdown(f"<span style='color: {status_color[sensor['Status']]}'>{sensor['Status']}</span>", unsafe_allow_html=True)

def display_analytics_reports():
    """Display analytics and reporting dashboard"""
    st.header("📈 Analytics & Reporting Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📊 Performance", "📈 Trends", "💰 Cost Analysis"])
    
    with tab1:
        st.subheader("📊 Performance Metrics")
        
        # KPI cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Orders/Day", "145", delta="12%")
        with col2:
            st.metric("🎯 Accuracy Rate", "99.3%", delta="0.8%")
        with col3:
            st.metric("⚡ Productivity", "89%", delta="5%")
        with col4:
            st.metric("📊 Utilization", "81%", delta="3%")
        
        # Performance chart
        dates = pd.date_range(start='2025-01-01', end='2025-01-07', freq='D')
        performance_data = pd.DataFrame({
            'Date': dates,
            'Orders_Processed': [120, 135, 98, 156, 142, 178, 165],
            'Accuracy_Rate': [99.2, 99.5, 98.8, 99.1, 99.3, 99.7, 99.4]
        })
        
        fig = px.line(performance_data, x='Date', y='Orders_Processed', title='Daily Orders Processed')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Inventory Trends")
        
        # Inventory turnover analysis
        categories = ['Electronics', 'Clothing', 'Grocery', 'Home & Garden', 'Sports']
        turnover_data = pd.DataFrame({
            'Category': categories,
            'Turnover_Rate': [12.5, 8.2, 15.8, 6.4, 9.1],
            'Stock_Value': [125000, 89000, 67000, 45000, 38000]
        })
        
        fig = px.bar(turnover_data, x='Category', y='Turnover_Rate', title='Inventory Turnover by Category')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("💰 Cost Analysis")
        
        # Cost breakdown
        cost_data = pd.DataFrame({
            'Cost Category': ['Labor', 'Equipment', 'Utilities', 'Maintenance', 'Other'],
            'Monthly Cost': [25000, 8000, 3500, 2000, 1500]
        })
        
        fig = px.pie(cost_data, values='Monthly Cost', names='Cost Category', title="Monthly Cost Breakdown")
        st.plotly_chart(fig, use_container_width=True)

def display_mobile_operations():
    """Display mobile operations interface"""
    st.header("📱 Mobile Operations")
    
    st.info("📱 **Mobile-Optimized Interface** - Optimized for smartphones and tablets")
    
    # Mobile-specific features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📷 Quick Scan")
        if st.button("📱 Launch Camera Scanner", use_container_width=True):
            st.success("📱 Camera scanner launched!")
        
        if st.button("📋 View Tasks", use_container_width=True):
            st.success("📋 Task list opened!")
        
        if st.button("📊 Stock Check", use_container_width=True):
            st.success("📊 Stock check initiated!")
    
    with col2:
        st.markdown("### ⚡ Quick Actions")
        if st.button("📥 Quick Receipt", use_container_width=True):
            st.success("📥 Quick receipt mode!")
        
        if st.button("📤 Quick Ship", use_container_width=True):
            st.success("📤 Quick shipping mode!")
        
        if st.button("🔄 Cycle Count", use_container_width=True):
            st.success("🔄 Cycle count started!")

def display_settings():
    """Display system settings"""
    st.header("⚙️ System Settings")
    
    tab1, tab2, tab3 = st.tabs(["🏢 Warehouse Config", "👥 User Management", "🔔 Notifications"])
    
    with tab1:
        st.subheader("🏢 Warehouse Configuration")
        
        # Warehouse settings
        warehouse_name = st.text_input("Warehouse Name", value="Main Distribution Center")
        warehouse_address = st.text_area("Address", value="123 Warehouse Ave, Dallas, TX")
        
        # Zone configuration
        st.markdown("#### 🗺️ Zone Configuration")
        
        zones = ["A01", "A02", "A03", "B01", "B02", "C01"]
        for zone in zones:
            with st.expander(f"Zone {zone}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.number_input(f"Capacity", value=1000, key=f"capacity_{zone}")
                with col2:
                    st.selectbox(f"Type", ["High Value", "Fast Moving", "Seasonal", "Bulk Items"], key=f"type_{zone}")
    
    with tab2:
        st.subheader("👥 User Management")
        
        # User roles
        roles = ["Admin", "Manager", "Supervisor", "Operator", "Viewer"]
        for role in roles:
            with st.expander(f"{role} Role"):
                permissions = st.multiselect(
                    f"Permissions for {role}",
                    ["view_all", "edit_all", "delete_all", "manage_users", "system_config"],
                    key=f"permissions_{role}"
                )
    
    with tab3:
        st.subheader("🔔 Notification Settings")
        
        # Notification configuration
        st.checkbox("Low Stock Alerts", value=True)
        st.checkbox("System Integration Alerts", value=True)
        st.checkbox("Daily Reports", value=True)
        st.checkbox("Emergency Notifications", value=True)
        
        # Notification channels
        st.multiselect(
            "Notification Channels",
            ["Email", "SMS", "Push Notification", "In-App"],
            default=["Email", "In-App"]
        )

def display_receipt_form():
    """Display receipt form for new receipt entry"""
    st.markdown("---")
    st.header("📥 New Receipt Entry")
    
    # Close button
    if st.button("❌ Close", key="close_receipt"):
        st.session_state.show_receipt_form = False
        st.rerun()
    
    with st.form("quick_receipt_form"):
        st.markdown("#### 📋 Receipt Information")
        
        col1, col2 = st.columns(2)
        with col1:
            supplier = st.text_input("Supplier Name", placeholder="Enter supplier name")
            purchase_order = st.text_input("Purchase Order #", placeholder="PO-12345")
            receipt_date = st.date_input("Receipt Date", datetime.date.today())
            expected_items = st.number_input("Expected Items", min_value=1, max_value=100, value=1)
        
        with col2:
            delivery_note = st.text_input("Delivery Note #", placeholder="DN-67890")
            received_by = st.text_input("Received By", value=st.session_state.warehouse_user_role)
            zone_assignment = st.selectbox("Assign to Zone", ["A01", "A02", "A03", "B01", "B02", "C01"])
            carrier = st.selectbox("Carrier", ["FedEx", "UPS", "DHL", "USPS", "Direct Delivery"])
        
        # Items section
        st.markdown("#### 📦 Item Details")
        
        items_data = []
        for i in range(expected_items):
            st.markdown(f"**Item {i+1}:**")
            item_col1, item_col2, item_col3, item_col4 = st.columns(4)
            
            with item_col1:
                sku = st.text_input(f"SKU", key=f"sku_{i}", placeholder="SKU-001")
            with item_col2:
                product_name = st.text_input(f"Product", key=f"product_{i}", placeholder="Product name")
            with item_col3:
                quantity = st.number_input(f"Quantity", min_value=1, key=f"qty_{i}", value=1)
            with item_col4:
                condition = st.selectbox(f"Condition", ["Good", "Damaged", "Partial"], key=f"condition_{i}")
            
            items_data.append({
                "SKU": sku,
                "Product": product_name,
                "Quantity": quantity,
                "Condition": condition
            })
        
        if st.form_submit_button("📥 Process Receipt", use_container_width=True):
            if supplier and purchase_order:
                # Generate receipt
                receipt_id = f"REC{random.randint(10000, 99999)}"
                
                # Create receipt document
                receipt_data = {
                    "Receipt ID": receipt_id,
                    "Date": receipt_date.strftime("%Y-%m-%d"),
                    "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "Supplier": supplier,
                    "Purchase Order": purchase_order,
                    "Delivery Note": delivery_note,
                    "Received By": received_by,
                    "Warehouse": st.session_state.selected_warehouse,
                    "Zone Assignment": zone_assignment,
                    "Carrier": carrier,
                    "Total Items": expected_items,
                    "Items": items_data
                }
                
                # Display formatted receipt
                display_formatted_receipt(receipt_data)
                
                # AUTO-GENERATE WAREHOUSE RECEIPT FOR RECEIVING
                st.markdown("---")
                st.markdown("### 🏪 **AUTOMATIC WAREHOUSE RECEIVING RECEIPT**")
                
                # Import receipt generator
                from utils.receipts import auto_generate_warehouse_receipt, display_auto_receipt
                
                # Prepare warehouse receipt data for receiving
                warehouse_receipt_data = {
                    "order_id": purchase_order,
                    "picking_id": receipt_id,
                    "customer_name": f"Receiving from {supplier}",
                    "delivery_address": f"Warehouse {st.session_state.selected_warehouse}, Zone {zone_assignment}",
                    "warehouse_location": st.session_state.selected_warehouse,
                    "zone": zone_assignment,
                    "assigned_worker": received_by,
                    "delivery_id": delivery_note,
                    "agent_assigned": f"{carrier} Delivery Agent",
                    "eta": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "items": [
                        {
                            "name": item["Product"],
                            "quantity": item["Quantity"],
                            "location": f"{st.session_state.selected_warehouse}-{zone_assignment}",
                            "status": "RECEIVED"
                        }
                        for item in items_data
                    ],
                    "total_weight": sum(item["Quantity"] for item in items_data) * 2.5,  # Estimate weight
                    "packaging_type": "Incoming Inventory"
                }
                
                # Generate warehouse receipt
                warehouse_receipt_result = auto_generate_warehouse_receipt(warehouse_receipt_data)
                
                # Display the warehouse receipt
                display_auto_receipt(warehouse_receipt_result)
                
                # Reset form
                st.session_state.show_receipt_form = False
                st.success("✅ Receipt processed successfully!")
                
                # Add to activity feed (simulate)
                if 'warehouse_activities' not in st.session_state:
                    st.session_state.warehouse_activities = []
                
                st.session_state.warehouse_activities.append({
                    "time": "Just now",
                    "action": f"Receipt {receipt_id} processed",
                    "user": received_by,
                    "location": zone_assignment
                })
            else:
                st.error("Please fill in required fields: Supplier and Purchase Order")

def display_shipment_form():
    """Display shipment form for new shipment entry"""
    st.markdown("---")
    st.header("📦 New Shipment Entry")
    
    # Close button
    if st.button("❌ Close", key="close_shipment"):
        st.session_state.show_shipment_form = False
        st.rerun()
    
    with st.form("quick_shipment_form"):
        st.markdown("#### 📋 Shipment Information")
        
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name", placeholder="Customer ABC Corp")
            order_id = st.text_input("Order ID", placeholder="ORD-12345")
            ship_date = st.date_input("Ship Date", datetime.date.today())
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        with col2:
            shipping_address = st.text_area("Shipping Address", placeholder="123 Main St, City, State, ZIP")
            carrier = st.selectbox("Carrier", ["FedEx", "UPS", "DHL", "USPS"])
            service_type = st.selectbox("Service Type", ["Standard", "Express", "Overnight", "Ground"])
            prepared_by = st.text_input("Prepared By", value=st.session_state.warehouse_user_role)
        
        # Items section
        st.markdown("#### 📦 Items to Ship")
        num_items = st.number_input("Number of Items", min_value=1, max_value=20, value=1)
        
        items_data = []
        total_weight = 0
        
        for i in range(num_items):
            st.markdown(f"**Item {i+1}:**")
            item_col1, item_col2, item_col3, item_col4 = st.columns(4)
            
            with item_col1:
                sku = st.text_input(f"SKU", key=f"ship_sku_{i}", placeholder="SKU-001")
            with item_col2:
                product_name = st.text_input(f"Product", key=f"ship_product_{i}", placeholder="Product name")
            with item_col3:
                quantity = st.number_input(f"Quantity", min_value=1, key=f"ship_qty_{i}", value=1)
            with item_col4:
                weight = st.number_input(f"Weight (lbs)", min_value=0.1, key=f"ship_weight_{i}", value=1.0)
            
            total_weight += weight * quantity
            
            items_data.append({
                "SKU": sku,
                "Product": product_name,
                "Quantity": quantity,
                "Weight": weight,
                "Total Weight": weight * quantity
            })
        
        if st.form_submit_button("📦 Create Shipment", use_container_width=True):
            if customer_name and order_id:
                # Generate shipment
                shipment_id = f"SHIP{random.randint(10000, 99999)}"
                tracking_number = f"TRK{random.randint(100000, 999999)}"
                
                # Create shipment document
                shipment_data = {
                    "Shipment ID": shipment_id,
                    "Tracking Number": tracking_number,
                    "Date": ship_date.strftime("%Y-%m-%d"),
                    "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "Customer": customer_name,
                    "Order ID": order_id,
                    "Shipping Address": shipping_address,
                    "Priority": priority,
                    "Carrier": carrier,
                    "Service Type": service_type,
                    "Prepared By": prepared_by,
                    "Warehouse": st.session_state.selected_warehouse,
                    "Total Items": num_items,
                    "Total Weight": f"{total_weight:.2f} lbs",
                    "Items": items_data
                }
                
                # Display formatted shipment
                display_formatted_shipment(shipment_data)
                
                # AUTO-GENERATE WAREHOUSE RECEIPT FOR SHIPMENT
                st.markdown("---")
                st.markdown("### 🏪 **AUTOMATIC WAREHOUSE RECEIPT**")
                
                # Import receipt generator
                from utils.receipts import auto_generate_warehouse_receipt, display_auto_receipt
                
                # Prepare warehouse receipt data
                warehouse_receipt_data = {
                    "order_id": order_id,
                    "picking_id": shipment_id,
                    "customer_name": customer_name,
                    "delivery_address": shipping_address,
                    "warehouse_location": st.session_state.selected_warehouse,
                    "zone": f"Zone-{random.choice(['A', 'B', 'C'])}{random.randint(1, 10)}",
                    "assigned_worker": prepared_by,
                    "delivery_id": tracking_number,
                    "agent_assigned": f"{carrier} Delivery Agent",
                    "eta": (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "items": [
                        {
                            "name": item["Product"],
                            "quantity": item["Quantity"],
                            "location": f"{st.session_state.selected_warehouse}-{item['SKU']}",
                            "status": "PICKED"
                        }
                        for item in items_data
                    ],
                    "total_weight": total_weight,
                    "packaging_type": "Standard Box"
                }
                
                # Generate warehouse receipt
                warehouse_receipt_result = auto_generate_warehouse_receipt(warehouse_receipt_data)
                
                # Display the warehouse receipt
                display_auto_receipt(warehouse_receipt_result)
                
                # Reset form
                st.session_state.show_shipment_form = False
                st.success("✅ Shipment created successfully!")
                
                # Add to activity feed
                if 'warehouse_activities' not in st.session_state:
                    st.session_state.warehouse_activities = []
                
                st.session_state.warehouse_activities.append({
                    "time": "Just now",
                    "action": f"Shipment {shipment_id} created",
                    "user": prepared_by,
                    "location": st.session_state.selected_warehouse
                })
            else:
                st.error("Please fill in required fields: Customer Name and Order ID")

def display_item_lookup():
    """Display item lookup interface"""
    st.markdown("---")
    st.header("🔍 Item Lookup")
    
    # Close button
    if st.button("❌ Close", key="close_lookup"):
        st.session_state.show_item_lookup = False
        st.rerun()
    
    # Search options
    search_type = st.radio("Search by:", ["SKU", "Product Name", "Barcode", "Zone"])
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if search_type == "SKU":
            search_value = st.text_input("Enter SKU", placeholder="SKU-12345")
        elif search_type == "Product Name":
            search_value = st.text_input("Enter Product Name", placeholder="iPhone 15 Pro")
        elif search_type == "Barcode":
            search_value = st.text_input("Enter Barcode", placeholder="123456789012")
        else:  # Zone
            search_value = st.selectbox("Select Zone", ["A01", "A02", "A03", "B01", "B02", "C01"])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        search_button = st.button("🔍 Search", use_container_width=True)
    
    if search_button and search_value:
        # Simulate search results
        if search_type == "Zone":
            # Show all items in the zone
            st.subheader(f"📦 Items in Zone {search_value}")
            
            # Generate sample items for the zone
            zone_items = []
            products = ["iPhone 15 Pro", "Samsung Galaxy S24", "Dell Laptop", "Nike Air Max", "Adidas Sneakers"]
            
            for i, product in enumerate(products):
                zone_items.append({
                    "SKU": f"SKU{random.randint(1000, 9999)}",
                    "Product": product,
                    "Zone": search_value,
                    "Location": f"Row {random.randint(1, 10)}, Shelf {random.randint(1, 5)}",
                    "Quantity": random.randint(10, 500),
                    "Status": random.choice(["Available", "Reserved", "Low Stock"]),
                    "Last Updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            
            df = pd.DataFrame(zone_items)
            st.dataframe(df, use_container_width=True)
            
        else:
            # Show individual item details
            st.subheader(f"📋 Item Details for: {search_value}")
            
            # Generate sample item details
            item_details = {
                "SKU": search_value if search_type == "SKU" else f"SKU{random.randint(1000, 9999)}",
                "Product Name": search_value if search_type == "Product Name" else random.choice(["iPhone 15 Pro", "Samsung Galaxy S24", "Dell Laptop"]),
                "Barcode": search_value if search_type == "Barcode" else f"{random.randint(100000000000, 999999999999)}",
                "Zone": random.choice(["A01", "A02", "A03", "B01", "B02", "C01"]),
                "Location": f"Row {random.randint(1, 10)}, Shelf {random.randint(1, 5)}",
                "Current Stock": random.randint(0, 500),
                "Reserved": random.randint(0, 50),
                "Available": random.randint(0, 450),
                "Reorder Point": random.randint(20, 100),
                "Max Stock": random.randint(500, 1000),
                "Unit Price": f"${random.randint(10, 1000):.2f}",
                "Supplier": random.choice(["Supplier A", "Supplier B", "Supplier C"]),
                "Category": random.choice(["Electronics", "Clothing", "Grocery", "Sports"]),
                "Status": random.choice(["Active", "Inactive", "Discontinued"]),
                "Last Movement": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Created Date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
            }
            
            # Display in a nice format
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📦 Basic Information:**")
                st.write(f"**SKU:** {item_details['SKU']}")
                st.write(f"**Product:** {item_details['Product Name']}")
                st.write(f"**Barcode:** {item_details['Barcode']}")
                st.write(f"**Category:** {item_details['Category']}")
                st.write(f"**Status:** {item_details['Status']}")
                st.write(f"**Unit Price:** {item_details['Unit Price']}")
                st.write(f"**Supplier:** {item_details['Supplier']}")
                
            with col2:
                st.markdown("**📍 Location & Stock:**")
                st.write(f"**Zone:** {item_details['Zone']}")
                st.write(f"**Location:** {item_details['Location']}")
                st.write(f"**Current Stock:** {item_details['Current Stock']}")
                st.write(f"**Reserved:** {item_details['Reserved']}")
                st.write(f"**Available:** {item_details['Available']}")
                st.write(f"**Reorder Point:** {item_details['Reorder Point']}")
                st.write(f"**Max Stock:** {item_details['Max Stock']}")
            
            # Stock status
            if item_details['Current Stock'] < item_details['Reorder Point']:
                st.error("⚠️ **Low Stock Alert!** This item is below the reorder point.")
            elif item_details['Current Stock'] > item_details['Max Stock'] * 0.9:
                st.warning("📈 **High Stock Level** - Consider reviewing reorder quantities.")
            else:
                st.success("✅ **Stock Level Normal**")
            
            # Action buttons
            st.markdown("#### ⚡ Quick Actions")
            action_col1, action_col2, action_col3, action_col4 = st.columns(4)
            
            with action_col1:
                if st.button("📝 Update Stock"):
                    st.info("Stock update form would open here")
            
            with action_col2:
                if st.button("📍 Move Item"):
                    st.info("Item move form would open here")
            
            with action_col3:
                if st.button("📋 View History"):
                    st.info("Item history would display here")
            
            with action_col4:
                if st.button("🏷️ Print Label"):
                    st.success("Label sent to printer")

def display_report_generator():
    """Display report generator interface"""
    st.markdown("---")
    st.header("📊 Report Generator")
    
    # Close button
    if st.button("❌ Close", key="close_report"):
        st.session_state.show_report_generator = False
        st.rerun()
    
    # Report configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        report_type = st.selectbox("Report Type", [
            "📦 Inventory Summary Report",
            "📈 Stock Movement Report", 
            "📊 Zone Utilization Report",
            "🚚 Receiving Report",
            "📤 Shipping Report",
            "⚠️ Low Stock Alert Report",
            "💰 Inventory Valuation Report",
            "📋 ABC Analysis Report"
        ])
        
        # Date range
        date_range = st.date_input(
            "Report Date Range",
            value=[datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()],
            max_value=datetime.date.today()
        )
        
        # Additional filters
        warehouse_filter = st.multiselect("Warehouses", ["WH001", "WH002", "WH003", "WH004"], default=[st.session_state.selected_warehouse])
        zone_filter = st.multiselect("Zones", ["A01", "A02", "A03", "B01", "B02", "C01"])
        
    with col2:
        st.markdown("**Report Options:**")
        format_type = st.radio("Output Format", ["📊 View Online", "📥 Download PDF", "📄 Download Excel"])
        include_charts = st.checkbox("Include Charts", value=True)
        include_summary = st.checkbox("Include Summary", value=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_button = st.button("📊 Generate Report", use_container_width=True)
    
    if generate_button:
        # Generate the selected report
        st.success("📊 Generating report...")
        
        # Simulate report generation
        with st.spinner("Processing data..."):
            time.sleep(2)  # Simulate processing time
        
        # Display the report
        display_generated_report(report_type, date_range, warehouse_filter, zone_filter, include_charts, include_summary, format_type)

def display_formatted_receipt(receipt_data):
    """Display a formatted receipt"""
    st.markdown("---")
    st.subheader("📋 Receipt Document")
    
    # Header
    st.markdown(f"""
    <div style="border: 2px solid #007BFF; padding: 20px; border-radius: 10px; background: #f8f9fa;">
        <h2 style="color: #007BFF; margin: 0; text-align: center;">📥 GOODS RECEIPT</h2>
        <h3 style="color: #007BFF; margin: 10px 0; text-align: center;">Receipt ID: {receipt_data['Receipt ID']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Receipt details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Receipt Information:**")
        st.write(f"**Date:** {receipt_data['Date']}")
        st.write(f"**Time:** {receipt_data['Time']}")
        st.write(f"**Supplier:** {receipt_data['Supplier']}")
        st.write(f"**Purchase Order:** {receipt_data['Purchase Order']}")
        st.write(f"**Delivery Note:** {receipt_data['Delivery Note']}")
    
    with col2:
        st.markdown("**🏢 Warehouse Information:**")
        st.write(f"**Warehouse:** {receipt_data['Warehouse']}")
        st.write(f"**Zone Assignment:** {receipt_data['Zone Assignment']}")
        st.write(f"**Received By:** {receipt_data['Received By']}")
        st.write(f"**Carrier:** {receipt_data['Carrier']}")
        st.write(f"**Total Items:** {receipt_data['Total Items']}")
    
    # Items table
    st.markdown("**📦 Items Received:**")
    items_df = pd.DataFrame(receipt_data['Items'])
    st.dataframe(items_df, use_container_width=True)
    
    # Download options
    st.markdown("**📥 Download Options:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF"):
            st.success("PDF receipt downloaded!")
    
    with col2:
        if st.button("📊 Download Excel"):
            st.success("Excel receipt downloaded!")
    
    with col3:
        if st.button("🖨️ Print Receipt"):
            st.success("Receipt sent to printer!")

def display_formatted_shipment(shipment_data):
    """Display a formatted shipment document"""
    st.markdown("---")
    st.subheader("📦 Shipment Document")
    
    # Header
    st.markdown(f"""
    <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; background: #f8f9fa;">
        <h2 style="color: #28a745; margin: 0; text-align: center;">📦 SHIPMENT ORDER</h2>
        <h3 style="color: #28a745; margin: 10px 0; text-align: center;">Shipment ID: {shipment_data['Shipment ID']}</h3>
        <h4 style="color: #28a745; margin: 5px 0; text-align: center;">Tracking: {shipment_data['Tracking Number']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Shipment details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📋 Shipment Information:**")
        st.write(f"**Date:** {shipment_data['Date']}")
        st.write(f"**Time:** {shipment_data['Time']}")
        st.write(f"**Customer:** {shipment_data['Customer']}")
        st.write(f"**Order ID:** {shipment_data['Order ID']}")
        st.write(f"**Priority:** {shipment_data['Priority']}")
        st.write(f"**Prepared By:** {shipment_data['Prepared By']}")
    
    with col2:
        st.markdown("**🚚 Shipping Information:**")
        st.write(f"**Carrier:** {shipment_data['Carrier']}")
        st.write(f"**Service Type:** {shipment_data['Service Type']}")
        st.write(f"**Warehouse:** {shipment_data['Warehouse']}")
        st.write(f"**Total Items:** {shipment_data['Total Items']}")
        st.write(f"**Total Weight:** {shipment_data['Total Weight']}")
        st.write(f"**Tracking Number:** {shipment_data['Tracking Number']}")
    
    # Shipping address
    st.markdown("**📍 Shipping Address:**")
    st.text_area("Address", value=shipment_data['Shipping Address'], disabled=True, height=80)
    
    # Items table
    st.markdown("**📦 Items to Ship:**")
    items_df = pd.DataFrame(shipment_data['Items'])
    st.dataframe(items_df, use_container_width=True)
    
    # Download options
    st.markdown("**📥 Download Options:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Download PDF", key="ship_pdf"):
            st.success("PDF shipment downloaded!")
    
    with col2:
        if st.button("🏷️ Print Labels", key="ship_labels"):
            st.success("Shipping labels printed!")
    
    with col3:
        if st.button("📋 Packing List", key="ship_packing"):
            st.success("Packing list generated!")
    
    with col4:
        if st.button("📧 Email Customer", key="ship_email"):
            st.success("Tracking info emailed!")

def display_generated_report(report_type, date_range, warehouse_filter, zone_filter, include_charts, include_summary, format_type):
    """Display the generated report"""
    st.markdown("---")
    st.subheader(f"📊 {report_type}")
    
    # Report header
    st.markdown(f"""
    <div style="border: 2px solid #6f42c1; padding: 15px; border-radius: 8px; background: #f8f9fa; margin-bottom: 20px;">
        <h3 style="color: #6f42c1; margin: 0;">📊 {report_type}</h3>
        <p style="margin: 5px 0;"><strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p style="margin: 5px 0;"><strong>Period:</strong> {date_range[0]} to {date_range[1]}</p>
        <p style="margin: 5px 0;"><strong>Warehouses:</strong> {', '.join(warehouse_filter) if warehouse_filter else 'All'}</p>
        <p style="margin: 5px 0;"><strong>Generated By:</strong> {st.session_state.warehouse_user_role}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if include_summary:
        st.markdown("### 📋 Executive Summary")
        
        # Generate summary metrics based on report type
        if "Inventory" in report_type:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Items", "15,432", "↑ 234")
            with col2:
                st.metric("Total Value", "$2.4M", "↑ $45K")
            with col3:
                st.metric("Low Stock Items", "23", "↓ 5")
            with col4:
                st.metric("Zero Stock Items", "7", "↑ 2")
        
        elif "Movement" in report_type:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Items Received", "2,341", "↑ 12%")
            with col2:
                st.metric("Items Shipped", "2,189", "↑ 8%")
            with col3:
                st.metric("Net Movement", "+152", "↑ 4%")
            with col4:
                st.metric("Accuracy Rate", "99.2%", "↑ 0.3%")
        
        elif "Zone" in report_type:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Utilization", "78.5%", "↑ 2.1%")
            with col2:
                st.metric("Highest Zone", "A01 (95%)", "")
            with col3:
                st.metric("Lowest Zone", "D01 (45%)", "")
            with col4:
                st.metric("Efficiency Score", "87.3%", "↑ 1.5%")
    
    # Generate sample data based on report type
    if "Inventory Summary" in report_type:
        # Inventory data
        inventory_data = []
        categories = ["Electronics", "Clothing", "Grocery", "Home & Garden", "Sports"]
        
        for category in categories:
            inventory_data.append({
                "Category": category,
                "Total Items": random.randint(1000, 5000),
                "Total Value": f"${random.randint(100000, 800000):,}",
                "Avg Value per Item": f"${random.randint(50, 500)}",
                "Low Stock Items": random.randint(0, 50),
                "Turnover Rate": f"{random.uniform(2.0, 12.0):.1f}x"
            })
        
        df = pd.DataFrame(inventory_data)
        st.dataframe(df, use_container_width=True)
        
        if include_charts:
            # Create charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.pie(df, values=[int(x.replace('$', '').replace(',', '')) for x in df['Total Value']], 
                             names='Category', title='Inventory Value by Category')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.bar(df, x='Category', y='Total Items', title='Item Count by Category')
                st.plotly_chart(fig2, use_container_width=True)
    
    elif "Stock Movement" in report_type:
        # Movement data
        dates = pd.date_range(start=date_range[0], end=date_range[1], freq='D')
        movement_data = []
        
        for date in dates:
            movement_data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Items In": random.randint(50, 200),
                "Items Out": random.randint(40, 180),
                "Net Change": random.randint(-50, 50),
                "Transactions": random.randint(20, 100)
            })
        
        df = pd.DataFrame(movement_data)
        st.dataframe(df, use_container_width=True)
        
        if include_charts:
            fig = px.line(df, x='Date', y=['Items In', 'Items Out'], title='Daily Stock Movement')
            st.plotly_chart(fig, use_container_width=True)
    
    elif "Zone Utilization" in report_type:
        # Zone data
        zones = ["A01", "A02", "A03", "B01", "B02", "C01", "C02", "D01"]
        zone_data = []
        
        for zone in zones:
            utilization = random.randint(30, 95)
            zone_data.append({
                "Zone": zone,
                "Capacity": random.randint(500, 5000),
                "Current Stock": random.randint(200, 4500),
                "Utilization %": utilization,
                "Status": "High" if utilization > 80 else "Medium" if utilization > 50 else "Low",
                "Last Activity": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        
        df = pd.DataFrame(zone_data)
        st.dataframe(df, use_container_width=True)
        
        if include_charts:
            fig = px.bar(df, x='Zone', y='Utilization %', color='Status', 
                        title='Zone Utilization Overview')
            st.plotly_chart(fig, use_container_width=True)
    
    # Download options
    st.markdown("### 📥 Download Report")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF Report"):
            st.success("PDF report downloaded!")
    
    with col2:
        if st.button("📊 Download Excel Report"):
            st.success("Excel report downloaded!")
    
    with col3:
        if st.button("📧 Email Report"):
            st.success("Report emailed successfully!")
    
    # Close button
    if st.button("❌ Close Report"):
        st.session_state.show_report_generator = False
        st.rerun()
