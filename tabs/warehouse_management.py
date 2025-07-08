"""
Comprehensive Warehouse Management System (WMS)
Features: Real-time tracking, inventory control, space optimization, barcode integration,
multi-location support, FIFO/LIFO, employee access control, and reporting dashboards.
"""

import streamlit as st
import pandas as pd
import datetime
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import qrcode
from io import BytesIO
import base64
import time
import random
from utils.api import get_data, put_data, post_data
from utils.helpers import display_kpi_metrics, format_date, show_notification

# Warehouse Configuration
WAREHOUSE_ZONES = {
    "A01": {"name": "Electronics Zone", "capacity": 1000, "current_stock": 0, "type": "High Value"},
    "A02": {"name": "Grocery Zone", "capacity": 2000, "current_stock": 0, "type": "Fast Moving"},
    "A03": {"name": "Clothing Zone", "capacity": 1500, "current_stock": 0, "type": "Seasonal"},
    "B01": {"name": "Bulk Storage", "capacity": 5000, "current_stock": 0, "type": "Bulk Items"},
    "B02": {"name": "Fragile Items", "capacity": 500, "current_stock": 0, "type": "Special Care"},
    "C01": {"name": "Refrigerated", "capacity": 800, "current_stock": 0, "type": "Temperature Controlled"},
    "C02": {"name": "Hazardous Materials", "capacity": 200, "current_stock": 0, "type": "Restricted Access"},
    "D01": {"name": "Returns Processing", "capacity": 300, "current_stock": 0, "type": "Quality Control"}
}

RFID_ZONES = {
    "RFID_GATE_01": {"name": "Main Entrance", "status": "Active", "last_read": "2 min ago"},
    "RFID_GATE_02": {"name": "Shipping Dock", "status": "Active", "last_read": "30 sec ago"},
    "RFID_GATE_03": {"name": "Receiving Dock", "status": "Active", "last_read": "1 min ago"},
    "RFID_GATE_04": {"name": "Cold Storage", "status": "Maintenance", "last_read": "1 hour ago"}
}

WAREHOUSE_LOCATIONS = {
    "WH001": {"name": "Main Distribution Center", "address": "123 Warehouse Ave, Dallas, TX", "zones": ["A01", "A02", "A03", "B01"]},
    "WH002": {"name": "Regional Hub North", "address": "456 Industrial Blvd, Chicago, IL", "zones": ["A01", "A02", "C01"]},
    "WH003": {"name": "Regional Hub South", "address": "789 Commerce St, Atlanta, GA", "zones": ["A02", "A03", "B02"]},
    "WH004": {"name": "Specialty Warehouse", "address": "321 Tech Park Dr, Austin, TX", "zones": ["C01", "C02", "D01"]}
}

AUTOMATION_RULES = {
    "AUTO_REORDER": {
        "enabled": True,
        "threshold_percentage": 20,
        "lead_time_days": 7,
        "safety_stock_percentage": 15
    },
    "ZONE_OPTIMIZATION": {
        "enabled": True,
        "optimize_frequency": "Daily",
        "consider_seasons": True,
        "fast_moving_threshold": 50
    },
    "PICKING_OPTIMIZATION": {
        "enabled": True,
        "algorithm": "Wave Planning",
        "batch_size": 10,
        "priority_orders": ["Express", "Same Day"]
    }
}

USER_ROLES = {
    "Admin": {"access_level": 10, "permissions": ["view_all", "edit_all", "delete_all", "manage_users", "system_config"]},
    "Manager": {"access_level": 8, "permissions": ["view_all", "edit_inventory", "manage_staff", "reports"]},
    "Supervisor": {"access_level": 6, "permissions": ["view_inventory", "edit_stock", "staff_reports"]},
    "Operator": {"access_level": 4, "permissions": ["view_inventory", "update_stock", "scan_items"]},
    "Viewer": {"access_level": 2, "permissions": ["view_inventory", "basic_reports"]}
}

def initialize_warehouse_session():
    """Initialize warehouse session variables"""
    if 'warehouse_user_role' not in st.session_state:
        st.session_state.warehouse_user_role = 'Operator'
    if 'selected_warehouse' not in st.session_state:
        st.session_state.selected_warehouse = 'WH001'
    if 'warehouse_transactions' not in st.session_state:
        st.session_state.warehouse_transactions = []
    if 'stock_movements' not in st.session_state:
        st.session_state.stock_movements = []

def generate_barcode_qr(data, code_type="QR"):
    """Generate barcode or QR code for warehouse items"""
    if code_type == "QR":
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    return None

def check_user_permission(required_permission):
    """Check if current user has required permission"""
    user_role = st.session_state.warehouse_user_role
    permissions = USER_ROLES.get(user_role, {}).get("permissions", [])
    return required_permission in permissions

def display_warehouse_header():
    """Display warehouse management header with user info"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; text-align: center;">🏭 Warehouse Management System</h1>
        <p style="margin: 10px 0 0 0; text-align: center; font-size: 16px;">
            Real-time tracking • Inventory control • Space optimization • Multi-location support
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_user_access_control():
    """Display user access control panel"""
    st.sidebar.subheader("👤 User Access Control")
    
    # User role selection (in production, this would be handled by authentication)
    selected_role = st.sidebar.selectbox(
        "Current User Role",
        list(USER_ROLES.keys()),
        index=list(USER_ROLES.keys()).index(st.session_state.warehouse_user_role)
    )
    st.session_state.warehouse_user_role = selected_role
    
    # Display current permissions
    permissions = USER_ROLES[selected_role]["permissions"]
    access_level = USER_ROLES[selected_role]["access_level"]
    
    st.sidebar.markdown(f"""
    **Access Level:** {access_level}/10  
    **Permissions:**
    """)
    for perm in permissions:
        st.sidebar.markdown(f"• {perm.replace('_', ' ').title()}")
    
    # Warehouse selection
    st.sidebar.subheader("🏢 Warehouse Selection")
    selected_warehouse = st.sidebar.selectbox(
        "Select Warehouse",
        list(WAREHOUSE_LOCATIONS.keys()),
        format_func=lambda x: f"{x} - {WAREHOUSE_LOCATIONS[x]['name']}"
    )
    st.session_state.selected_warehouse = selected_warehouse
    
    return selected_role, selected_warehouse

def display_warehouse_kpis():
    """Display warehouse KPIs and metrics"""
    if not check_user_permission("view_inventory"):
        st.error("❌ Access denied: Insufficient permissions to view inventory")
        return
    
    # Simulate warehouse data
    total_capacity = sum(zone["capacity"] for zone in WAREHOUSE_ZONES.values())
    current_stock = sum(zone["current_stock"] for zone in WAREHOUSE_ZONES.values())
    utilization = (current_stock / total_capacity * 100) if total_capacity > 0 else 0
    
    # Generate random metrics for demo
    pending_receipts = random.randint(5, 25)
    pending_shipments = random.randint(10, 40)
    low_stock_alerts = random.randint(2, 8)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📦 Total Capacity", f"{total_capacity:,} units")
    
    with col2:
        st.metric("📊 Current Stock", f"{current_stock:,} units", 
                 delta=f"{random.randint(-100, 200)} since yesterday")
    
    with col3:
        st.metric("🎯 Utilization", f"{utilization:.1f}%", 
                 delta=f"{random.uniform(-2.5, 5.2):.1f}%")
    
    with col4:
        st.metric("📥 Pending Receipts", pending_receipts, 
                 delta=f"{random.randint(-5, 10)} vs yesterday")
    
    with col5:
        st.metric("🚚 Pending Shipments", pending_shipments, 
                 delta=f"{random.randint(-8, 15)} vs yesterday")

def display_warehouse_layout():
    """Display warehouse layout and zone management"""
    st.subheader("🗺️ Warehouse Layout & Zone Management")
    
    if not check_user_permission("view_inventory"):
        st.error("❌ Access denied: Insufficient permissions to view warehouse layout")
        return
    
    # Get zones for selected warehouse
    selected_warehouse = st.session_state.selected_warehouse
    warehouse_zones = WAREHOUSE_LOCATIONS[selected_warehouse]["zones"]
    
    # Display warehouse info
    warehouse_info = WAREHOUSE_LOCATIONS[selected_warehouse]
    st.info(f"📍 **{warehouse_info['name']}** - {warehouse_info['address']}")
    
    # Zone layout visualization
    cols = st.columns(4)
    for i, zone_id in enumerate(warehouse_zones):
        with cols[i % 4]:
            zone = WAREHOUSE_ZONES[zone_id]
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
            
            # Zone management buttons
            if check_user_permission("edit_inventory"):
                if st.button(f"⚙️ Manage {zone_id}", key=f"manage_{zone_id}"):
                    st.session_state.selected_zone = zone_id
                    st.session_state.show_zone_management = True

def display_inventory_tracking():
    """Display real-time inventory tracking"""
    st.subheader("📊 Real-time Inventory Tracking")
    
    if not check_user_permission("view_inventory"):
        st.error("❌ Access denied: Insufficient permissions to view inventory")
        return
    
    # Inventory tracking tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Stock Levels", "🔍 Item Lookup", "📱 Barcode Scanner", "📈 Stock Movements"])
    
    with tab1:
        st.markdown("### 📦 Current Stock Levels")
        
        # Generate sample inventory data
        inventory_data = []
        products = ["iPhone 15 Pro", "Samsung Galaxy S24", "Dell Laptop", "Nike Air Max", "Adidas Sneakers",
                   "Organic Apples", "Whole Milk", "Bread Loaf", "Chicken Breast", "Salmon Fillet"]
        
        for product in products:
            stock_level = random.randint(0, 500)
            reorder_point = random.randint(20, 100)
            max_stock = random.randint(300, 1000)
            zone = random.choice(list(WAREHOUSE_ZONES.keys()))
            
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
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            zone_filter = st.selectbox("Filter by Zone", ["All"] + list(WAREHOUSE_ZONES.keys()))
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All", "Normal", "Low Stock"])
        with col3:
            search_term = st.text_input("🔍 Search Products")
        
        # Apply filters
        filtered_df = df.copy()
        if zone_filter != "All":
            filtered_df = filtered_df[filtered_df["Zone"] == zone_filter]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        if search_term:
            filtered_df = filtered_df[filtered_df["Product"].str.contains(search_term, case=False)]
        
        # Display filtered data
        st.dataframe(filtered_df, use_container_width=True)
        
        # Stock alerts
        low_stock_items = filtered_df[filtered_df["Status"] == "Low Stock"]
        if not low_stock_items.empty:
            st.warning(f"⚠️ {len(low_stock_items)} items are below reorder point!")
            with st.expander("View Low Stock Items"):
                st.dataframe(low_stock_items[["SKU", "Product", "Current Stock", "Reorder Point"]])
    
    with tab2:
        st.markdown("### 🔍 Item Lookup")
        
        lookup_method = st.radio("Lookup Method", ["SKU", "Product Name", "Barcode"])
        
        if lookup_method == "SKU":
            sku_input = st.text_input("Enter SKU")
            if sku_input and st.button("🔍 Search"):
                # Simulate SKU lookup
                st.success(f"Found item: {random.choice(products)}")
        
        elif lookup_method == "Product Name":
            product_input = st.text_input("Enter Product Name")
            if product_input and st.button("🔍 Search"):
                st.success(f"Found {random.randint(1, 5)} matching items")
        
        elif lookup_method == "Barcode":
            barcode_input = st.text_input("Enter Barcode")
            if barcode_input and st.button("🔍 Search"):
                st.success(f"Item found: {random.choice(products)}")
    
    with tab3:
        st.markdown("### 📱 Barcode/QR Code Scanner")
        
        if check_user_permission("scan_items"):
            # Simulate barcode scanner interface
            st.info("📱 **Mobile Scanner Interface** - Use your mobile device to scan barcodes")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📷 Scan Item")
                uploaded_image = st.file_uploader("Upload barcode image", type=['png', 'jpg', 'jpeg'])
                
                if uploaded_image:
                    st.image(uploaded_image, caption="Scanned Image", width=200)
                    if st.button("🔍 Process Scan"):
                        # Simulate barcode processing
                        st.success("✅ Barcode processed successfully!")
            
            with col2:
                st.markdown("#### 🏷️ Generate QR Code")
                item_data = st.text_input("Enter item data for QR code")
                if item_data:
                    qr_code = generate_barcode_qr(item_data)
                    if qr_code:
                        st.markdown(f'<img src="{qr_code}" width="200">', unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Download QR Code",
                            data=qr_code,
                            file_name=f"qr_code_{item_data}.png",
                            mime="image/png"
                        )
        else:
            st.error("❌ Access denied: Insufficient permissions to use scanner")
    
    with tab4:
        st.markdown("### 📈 Stock Movement History")
        
        # Generate sample stock movement data
        movement_data = []
        for i in range(20):
            movement_data.append({
                "Date": datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30)),
                "SKU": f"SKU{random.randint(1000, 9999)}",
                "Product": random.choice(products),
                "Type": random.choice(["IN", "OUT", "TRANSFER", "ADJUSTMENT"]),
                "Quantity": random.randint(1, 100),
                "Zone": random.choice(list(WAREHOUSE_ZONES.keys())),
                "User": random.choice(["John Doe", "Jane Smith", "Mike Johnson", "Sarah Wilson"]),
                "Reference": f"REF{random.randint(1000, 9999)}"
            })
        
        movements_df = pd.DataFrame(movement_data)
        movements_df["Date"] = movements_df["Date"].dt.strftime("%Y-%m-%d %H:%M")
        
        # Display movements
        st.dataframe(movements_df, use_container_width=True)
        
        # Movement analytics
        col1, col2 = st.columns(2)
        with col1:
            # Stock in vs out chart
            fig = px.pie(
                movements_df, 
                names="Type", 
                title="Stock Movement Types",
                color_discrete_map={
                    "IN": "#28a745",
                    "OUT": "#dc3545", 
                    "TRANSFER": "#ffc107",
                    "ADJUSTMENT": "#6c757d"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Daily movement trend
            daily_movements = movements_df.groupby("Date").size().reset_index(name="Count")
            fig2 = px.line(daily_movements, x="Date", y="Count", title="Daily Movement Trend")
            st.plotly_chart(fig2, use_container_width=True)

def display_receiving_shipping():
    """Display receiving and shipping management"""
    st.subheader("📦 Receiving & Shipping Management")
    
    if not check_user_permission("view_inventory"):
        st.error("❌ Access denied: Insufficient permissions to view receiving/shipping")
        return
    
    tab1, tab2, tab3 = st.tabs(["📥 Incoming Goods", "📤 Outgoing Shipments", "🚚 Delivery Tracking"])
    
    with tab1:
        st.markdown("### 📥 Goods Receiving")
        
        if check_user_permission("update_stock"):
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
                    zone_assignment = st.selectbox("Assign to Zone", list(WAREHOUSE_ZONES.keys()))
                
                # Items received
                st.markdown("#### 📦 Items Received")
                num_items = st.number_input("Number of Items", min_value=1, max_value=10, value=1)
                
                items_received = []
                for i in range(num_items):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        sku = st.text_input(f"SKU {i+1}", key=f"sku_{i}")
                    with col2:
                        product = st.text_input(f"Product {i+1}", key=f"product_{i}")
                    with col3:
                        quantity = st.number_input(f"Qty {i+1}", min_value=1, key=f"qty_{i}")
                    with col4:
                        condition = st.selectbox(f"Condition {i+1}", ["Good", "Damaged", "Partial"], key=f"condition_{i}")
                    
                    items_received.append({
                        "SKU": sku,
                        "Product": product,
                        "Quantity": quantity,
                        "Condition": condition
                    })
                
                if st.form_submit_button("📥 Process Receipt"):
                    # Process receipt
                    st.success("✅ Receipt processed successfully!")
                    
                    # Display receipt summary
                    st.markdown("#### 📋 Receipt Summary")
                    receipt_summary = {
                        "Receipt ID": f"REC{random.randint(10000, 99999)}",
                        "Supplier": supplier,
                        "PO Number": purchase_order,
                        "Date": receipt_date.strftime("%Y-%m-%d"),
                        "Items Count": len(items_received),
                        "Total Quantity": sum(item["Quantity"] for item in items_received),
                        "Zone": zone_assignment
                    }
                    # st.json(receipt_summary)  # HIDDEN: Do not show raw code or debug output
        else:
            st.error("❌ Access denied: Insufficient permissions to process receipts")
    
    with tab2:
        st.markdown("### 📤 Outgoing Shipments")
        
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
                "Carrier": random.choice(["FedEx", "UPS", "DHL", "USPS"]),
                "Tracking #": f"TRK{random.randint(100000, 999999)}"
            })
        
        shipments_df = pd.DataFrame(shipment_data)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All"] + list(shipments_df["Status"].unique()))
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All"] + list(shipments_df["Priority"].unique()))
        with col3:
            carrier_filter = st.selectbox("Filter by Carrier", ["All"] + list(shipments_df["Carrier"].unique()))
        
        # Apply filters
        filtered_shipments = shipments_df.copy()
        if status_filter != "All":
            filtered_shipments = filtered_shipments[filtered_shipments["Status"] == status_filter]
        if priority_filter != "All":
            filtered_shipments = filtered_shipments[filtered_shipments["Priority"] == priority_filter]
        if carrier_filter != "All":
            filtered_shipments = filtered_shipments[filtered_shipments["Carrier"] == carrier_filter]
        
        st.dataframe(filtered_shipments, use_container_width=True)
        
        # Shipment actions
        if check_user_permission("edit_inventory"):
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
        st.markdown("### 🚚 Live Delivery Tracking")
        
        # Integration with delivery tracking
        st.info("🔄 **Integrated with Delivery Management System**")
        
        # Display active deliveries
        active_deliveries = [
            {"Tracking": "TRK123456", "Status": "In Transit", "ETA": "2 hours", "Location": "Dallas, TX"},
            {"Tracking": "TRK789012", "Status": "Out for Delivery", "ETA": "45 minutes", "Location": "Local Hub"},
            {"Tracking": "TRK345678", "Status": "Delivered", "ETA": "Completed", "Location": "Customer"},
        ]
        
        for delivery in active_deliveries:
            status_color = {"In Transit": "blue", "Out for Delivery": "orange", "Delivered": "green"}
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; 
                        border-left: 4px solid {status_color.get(delivery['Status'], 'gray')};">
                <strong>{delivery['Tracking']}</strong> - {delivery['Status']}<br>
                📍 {delivery['Location']} | ⏱️ ETA: {delivery['ETA']}
            </div>
            """, unsafe_allow_html=True)

def display_advanced_features():
    """Display advanced WMS features"""
    st.subheader("🚀 Advanced WMS Features")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📡 RFID Tracking", "🤖 Automation", "🔮 Predictive Analytics", "🌡️ IoT Sensors"])
    
    with tab1:
        st.markdown("### 📡 RFID Real-time Tracking")
        
        # RFID gate status
        st.markdown("#### 🚪 RFID Gate Status")
        for gate_id, gate_data in RFID_ZONES.items():
            status_color = {"Active": "green", "Maintenance": "red", "Offline": "gray"}
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{gate_data['name']}** ({gate_id})")
            with col2:
                st.markdown(f"<span style='color: {status_color[gate_data['status']]}'>{gate_data['status']}</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"📡 {gate_data['last_read']}")
        
        # Live RFID readings
        st.markdown("#### 📊 Live RFID Readings")
        
        # Simulate live RFID data
        import random
        import time
        
        if st.button("🔄 Refresh Live Data"):
            rfid_readings = []
            for i in range(5):
                rfid_readings.append({
                    "Timestamp": datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 30)),
                    "RFID_Tag": f"RFID{random.randint(100000, 999999)}",
                    "Gate": random.choice(list(RFID_ZONES.keys())),
                    "Direction": random.choice(["IN", "OUT"]),
                    "Product": random.choice(["iPhone 15", "Samsung TV", "Nike Shoes", "Organic Milk", "Laptop"]),
                    "Employee": random.choice(["John Doe", "Jane Smith", "Mike Johnson"])
                })
            
            rfid_df = pd.DataFrame(rfid_readings)
            rfid_df["Timestamp"] = rfid_df["Timestamp"].dt.strftime("%H:%M:%S")
            st.dataframe(rfid_df, use_container_width=True)
    
    with tab2:
        st.markdown("### 🤖 Warehouse Automation")
        
        # Automation rules
        st.markdown("#### ⚙️ Automation Rules")
        
        for rule_name, rule_config in AUTOMATION_RULES.items():
            with st.expander(f"{rule_name.replace('_', ' ').title()}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    enabled = st.checkbox(f"Enable {rule_name}", value=rule_config.get("enabled", False))
                
                with col2:
                    if rule_name == "AUTO_REORDER":
                        threshold = st.slider("Reorder Threshold %", 10, 50, rule_config.get("threshold_percentage", 20))
                        lead_time = st.number_input("Lead Time (Days)", 1, 30, rule_config.get("lead_time_days", 7))
                    elif rule_name == "ZONE_OPTIMIZATION":
                        frequency = st.selectbox("Optimization Frequency", ["Daily", "Weekly", "Monthly"], 
                                                index=["Daily", "Weekly", "Monthly"].index(rule_config.get("optimize_frequency", "Daily")))
                        seasonal = st.checkbox("Consider Seasonal Patterns", value=rule_config.get("consider_seasons", True))
                    elif rule_name == "PICKING_OPTIMIZATION":
                        algorithm = st.selectbox("Algorithm", ["Wave Planning", "Batch Picking", "Zone Picking"],
                                                index=["Wave Planning", "Batch Picking", "Zone Picking"].index(rule_config.get("algorithm", "Wave Planning")))
                        batch_size = st.number_input("Batch Size", 1, 50, rule_config.get("batch_size", 10))
                
                if st.button(f"Save {rule_name} Settings"):
                    st.success(f"✅ {rule_name} settings saved!")
        
        # Automated tasks status
        st.markdown("#### 🔄 Automated Tasks Status")
        
        automated_tasks = [
            {"Task": "Auto Reorder SKU123", "Status": "Completed", "Next Run": "Tomorrow 6:00 AM"},
            {"Task": "Zone Optimization", "Status": "Running", "Next Run": "Tonight 11:00 PM"},
            {"Task": "Picking Wave Generation", "Status": "Scheduled", "Next Run": "In 2 hours"},
            {"Task": "Inventory Cycle Count", "Status": "Pending", "Next Run": "This Weekend"}
        ]
        
        for task in automated_tasks:
            status_color = {"Completed": "green", "Running": "blue", "Scheduled": "orange", "Pending": "gray"}
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; 
                        border-left: 4px solid {status_color[task['Status']]};">
                <strong>{task['Task']}</strong> - {task['Status']}<br>
                ⏰ Next Run: {task['Next Run']}
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🔮 Predictive Analytics")
        
        # Demand forecasting
        st.markdown("#### 📈 Demand Forecasting")
        
        # Generate sample forecast data
        forecast_products = ["iPhone 15", "Samsung TV", "Nike Shoes", "Organic Milk", "Laptop"]
        forecast_data = []
        
        for product in forecast_products:
            forecast_data.append({
                "Product": product,
                "Current Stock": random.randint(50, 500),
                "Forecasted Demand (7 days)": random.randint(20, 200),
                "Recommended Action": random.choice(["Reorder", "Increase Stock", "Maintain", "Reduce"]),
                "Confidence": f"{random.randint(75, 95)}%"
            })
        
        forecast_df = pd.DataFrame(forecast_data)
        st.dataframe(forecast_df, use_container_width=True)
        
        # Seasonal analysis
        st.markdown("#### 🌍 Seasonal Analysis")
        
        # Create seasonal trend chart
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
        st.markdown("### 🌡️ IoT Sensor Network")
        
        # Environmental monitoring
        st.markdown("#### 🌡️ Environmental Monitoring")
        
        # Temperature and humidity sensors
        sensor_data = [
            {"Zone": "Cold Storage A", "Temperature": "2.5°C", "Humidity": "65%", "Status": "Normal"},
            {"Zone": "Cold Storage B", "Temperature": "3.1°C", "Humidity": "68%", "Status": "Warning"},
            {"Zone": "Main Warehouse", "Temperature": "22°C", "Humidity": "45%", "Status": "Normal"},
            {"Zone": "Electronics Zone", "Temperature": "20°C", "Humidity": "40%", "Status": "Normal"},
            {"Zone": "Hazmat Storage", "Temperature": "18°C", "Humidity": "35%", "Status": "Normal"}
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
        
        # Motion and occupancy sensors
        st.markdown("#### 🚶 Motion & Occupancy Sensors")
        
        motion_data = [
            {"Zone": "Receiving Dock", "Occupancy": "3 people", "Last Motion": "30 sec ago", "Status": "Active"},
            {"Zone": "Picking Area", "Occupancy": "7 people", "Last Motion": "5 sec ago", "Status": "Active"},
            {"Zone": "Shipping Dock", "Occupancy": "2 people", "Last Motion": "1 min ago", "Status": "Active"},
            {"Zone": "Storage Area B", "Occupancy": "0 people", "Last Motion": "2 hours ago", "Status": "Inactive"}
        ]
        
        for motion in motion_data:
            st.markdown(f"**{motion['Zone']}:** {motion['Occupancy']} | Last Motion: {motion['Last Motion']}")
        
        # Sensor alerts
        st.markdown("#### 🚨 Sensor Alerts")
        
        alerts = [
            {"Time": "5 min ago", "Sensor": "Temperature Sensor B", "Alert": "Temperature above threshold", "Severity": "Warning"},
            {"Time": "1 hour ago", "Sensor": "Motion Sensor C", "Alert": "No motion detected for 2 hours", "Severity": "Info"},
            {"Time": "2 hours ago", "Sensor": "Humidity Sensor A", "Alert": "Humidity levels normal", "Severity": "Normal"}
        ]
        
        for alert in alerts:
            severity_color = {"Warning": "orange", "Info": "blue", "Normal": "green", "Critical": "red"}
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px; 
                        border-left: 4px solid {severity_color[alert['Severity']]};">
                <strong>{alert['Time']}</strong> - {alert['Sensor']}: {alert['Alert']}
            </div>
            """, unsafe_allow_html=True)

def display_smart_notifications():
    """Display smart notification system"""
    st.subheader("🔔 Smart Notification System")
    
    # Notification categories
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Alerts", "📊 Reports", "🔄 System", "📱 Mobile"])
    
    with tab1:
        st.markdown("### 🚨 Critical Alerts")
        
        alerts = [
            {"Time": "2 min ago", "Type": "Low Stock", "Message": "SKU123 below reorder point", "Priority": "High"},
            {"Time": "15 min ago", "Type": "Temperature", "Message": "Cold storage temperature rising", "Priority": "Critical"},
            {"Time": "1 hour ago", "Type": "System", "Message": "ERP sync completed successfully", "Priority": "Info"},
            {"Time": "2 hours ago", "Type": "Security", "Message": "Unauthorized access attempt", "Priority": "High"}
        ]
        
        for alert in alerts:
            priority_color = {"Critical": "red", "High": "orange", "Medium": "yellow", "Low": "blue", "Info": "green"}
            
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; 
                        border-left: 4px solid {priority_color[alert['Priority']]};">
                <strong>{alert['Time']}</strong> - {alert['Type']}<br>
                {alert['Message']} <span style="float: right; color: {priority_color[alert['Priority']]};">{alert['Priority']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Automated Reports")
        
        reports = [
            {"Report": "Daily Inventory Summary", "Schedule": "Daily 6:00 AM", "Last Sent": "Today 6:00 AM", "Status": "Sent"},
            {"Report": "Weekly Performance Report", "Schedule": "Monday 8:00 AM", "Last Sent": "Jan 15 8:00 AM", "Status": "Sent"},
            {"Report": "Monthly Analytics", "Schedule": "1st of month", "Last Sent": "Jan 1 9:00 AM", "Status": "Sent"},
            {"Report": "Exception Report", "Schedule": "As needed", "Last Sent": "Jan 16 2:30 PM", "Status": "Sent"}
        ]
        
        for report in reports:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px;">
                <strong>{report['Report']}</strong><br>
                📅 Schedule: {report['Schedule']} | 📤 Last Sent: {report['Last Sent']} | Status: {report['Status']}
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🔄 System Notifications")
        
        system_notifications = [
            {"Time": "Now", "Message": "System operating normally", "Type": "Status"},
            {"Time": "5 min ago", "Message": "Backup completed successfully", "Type": "Backup"},
            {"Time": "1 hour ago", "Message": "Database optimization completed", "Type": "Maintenance"},
            {"Time": "3 hours ago", "Message": "Security scan completed - no issues", "Type": "Security"}
        ]
        
        for notification in system_notifications:
            st.info(f"**{notification['Time']}** - {notification['Message']} ({notification['Type']})")
    
    with tab4:
        st.markdown("### 📱 Mobile Push Notifications")
        
        # Mobile notification settings
        st.checkbox("Enable Push Notifications", value=True)
        st.checkbox("Low Stock Alerts", value=True)
        st.checkbox("Order Completion", value=True)
        st.checkbox("System Alerts", value=False)
        st.checkbox("Daily Summary", value=True)
        
        # Test notification
        if st.button("📱 Send Test Notification"):
            st.success("✅ Test notification sent to mobile devices!")

def display_audit_trail():
    """Display audit trail and activity logs"""
    st.subheader("📋 Audit Trail & Activity Logs")
    
    # Audit trail tabs
    tab1, tab2, tab3 = st.tabs(["👤 User Actions", "📦 Inventory Changes", "🔧 System Changes"])
    
    with tab1:
        st.markdown("### 👤 User Activity Log")
        
        # Generate sample user activities
        user_activities = []
        actions = ["Login", "Logout", "Update Stock", "Create Order", "Scan Item", "Generate Report", "Export Data"]
        users = ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Wilson", "Tom Brown"]
        
        for i in range(15):
            user_activities.append({
                "Timestamp": datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 480)),
                "User": random.choice(users),
                "Action": random.choice(actions),
                "Details": f"Action performed on {random.choice(['SKU123', 'ORDER456', 'REPORT789'])}",
                "IP Address": f"192.168.1.{random.randint(100, 200)}",
                "Status": random.choice(["Success", "Failed", "Pending"])
            })
        
        activities_df = pd.DataFrame(user_activities)
        activities_df["Timestamp"] = activities_df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            user_filter = st.selectbox("Filter by User", ["All"] + users)
        with col2:
            action_filter = st.selectbox("Filter by Action", ["All"] + actions)
        with col3:
            date_filter = st.date_input("Filter by Date", datetime.date.today())
        
        # Display filtered activities
        filtered_activities = activities_df.copy()
        if user_filter != "All":
            filtered_activities = filtered_activities[filtered_activities["User"] == user_filter]
        if action_filter != "All":
            filtered_activities = filtered_activities[filtered_activities["Action"] == action_filter]
        
        st.dataframe(filtered_activities, use_container_width=True)
    
    with tab2:
        st.markdown("### 📦 Inventory Change Log")
        
        # Generate sample inventory changes
        inventory_changes = []
        change_types = ["Stock In", "Stock Out", "Adjustment", "Transfer", "Damaged", "Return"]
        
        for i in range(12):
            inventory_changes.append({
                "Timestamp": datetime.datetime.now() - datetime.timedelta(hours=random.randint(0, 72)),
                "SKU": f"SKU{random.randint(1000, 9999)}",
                "Change Type": random.choice(change_types),
                "Quantity": random.randint(-50, 100),
                "Previous Stock": random.randint(0, 500),
                "New Stock": random.randint(0, 500),
                "User": random.choice(users),
                "Reference": f"REF{random.randint(10000, 99999)}"
            })
        
        changes_df = pd.DataFrame(inventory_changes)
        changes_df["Timestamp"] = changes_df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        
        st.dataframe(changes_df, use_container_width=True)
    
    with tab3:
        st.markdown("### 🔧 System Configuration Changes")
        
        # System changes
        system_changes = [
            {"Time": "2024-01-15 10:30", "Change": "Added new user role", "User": "Admin", "Details": "Created 'Supervisor' role"},
            {"Time": "2024-01-15 09:15", "Change": "Updated warehouse zone", "User": "Manager", "Details": "Changed Zone A capacity"},
            {"Time": "2024-01-14 16:45", "Change": "Modified alert settings", "User": "Admin", "Details": "Updated low stock threshold"},
            {"Time": "2024-01-14 14:20", "Change": "Added new integration", "User": "IT Admin", "Details": "Connected new ERP system"}
        ]
        
        for change in system_changes:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px;">
                <strong>{change['Time']}</strong> - {change['Change']}<br>
                👤 User: {change['User']} | 📝 Details: {change['Details']}
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main warehouse management application"""
    st.set_page_config(page_title="Warehouse Management System", layout="wide")
    
    # Initialize session
    initialize_warehouse_session()
    
    # Display header
    display_warehouse_header()
    
    # User access control
    user_role, selected_warehouse = display_user_access_control()
    
    # Main navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 WMS Modules")
    
    page = st.sidebar.selectbox(
        "Select Module",
        [
            "📊 Dashboard",
            "🗺️ Warehouse Layout",
            "📦 Inventory Tracking",
            "📥 Receiving & Shipping",
            "📱 Mobile Operations",
            "� Advanced Features",
            "�📈 Analytics & Reports",
            "🔗 System Integration",
            "⚙️ Settings"
        ]
    )
    
    # Page routing
    if page == "📊 Dashboard":
        display_warehouse_kpis()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📥 New Receipt", use_container_width=True):
                st.info("Redirecting to receiving module...")
        
        with col2:
            if st.button("📤 New Shipment", use_container_width=True):
                st.info("Redirecting to shipping module...")
        
        with col3:
            if st.button("🔍 Item Lookup", use_container_width=True):
                st.info("Opening item lookup...")
        
        with col4:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Opening report generator...")
    
    elif page == "🗺️ Warehouse Layout":
        display_warehouse_layout()
    
    elif page == "📦 Inventory Tracking":
        display_inventory_tracking()
    
    elif page == "📥 Receiving & Shipping":
        display_receiving_shipping()
    
    elif page == "📱 Mobile Operations":
        st.subheader("📱 Mobile Operations")
        st.info("📱 **Mobile-Optimized Interface** - Optimized for smartphones and tablets")
        
        # Mobile-specific features
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📷 Quick Scan")
            st.button("📱 Launch Camera Scanner", use_container_width=True)
            st.button("📋 View Tasks", use_container_width=True)
            st.button("📊 Stock Check", use_container_width=True)
        
        with col2:
            st.markdown("### ⚡ Quick Actions")
            st.button("📥 Quick Receipt", use_container_width=True)
            st.button("📤 Quick Ship", use_container_width=True)
            st.button("🔄 Cycle Count", use_container_width=True)
    
    elif page == "� Advanced Features":
        display_advanced_features()
    
    elif page == "�📈 Analytics & Reports":
        st.subheader("📈 Analytics & Reports")
        st.info("📊 **Analytics Dashboard** - Comprehensive reporting and analytics")
        
        # Basic analytics placeholder
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📈 Performance Score", "94.2%", "↑ 2.1%")
        with col2:
            st.metric("📊 Efficiency", "89.5%", "↑ 1.8%")
        with col3:
            st.metric("🎯 Accuracy", "99.1%", "↑ 0.3%")
    
    elif page == "🔗 System Integration":
        st.subheader("🔗 System Integration")
        st.info("🔌 **API Integration** - Connect with external systems")
        
        # Basic integration status
        integrations = [
            {"System": "ERP", "Status": "Connected", "Last Sync": "2 min ago"},
            {"System": "E-commerce", "Status": "Connected", "Last Sync": "5 min ago"},
            {"System": "Shipping", "Status": "Connected", "Last Sync": "1 min ago"}
        ]
        
        for integration in integrations:
            st.success(f"✅ {integration['System']}: {integration['Status']} (Last sync: {integration['Last Sync']})")
    
    elif page == "⚙️ Settings":
        st.subheader("⚙️ System Settings")
        
        if check_user_permission("system_config"):
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏢 Warehouse Config", "👥 User Management", "🔔 Notifications", "📋 Audit Trail", "🚀 Advanced"])
            
            with tab1:
                st.markdown("### 🏢 Warehouse Configuration")
                
                # Warehouse settings
                st.markdown("#### 🏭 Warehouse Details")
                warehouse_name = st.text_input("Warehouse Name", value=WAREHOUSE_LOCATIONS[selected_warehouse]["name"])
                warehouse_address = st.text_area("Address", value=WAREHOUSE_LOCATIONS[selected_warehouse]["address"])
                
                # Zone configuration
                st.markdown("#### 🗺️ Zone Configuration")
                for zone_id in WAREHOUSE_LOCATIONS[selected_warehouse]["zones"]:
                    zone_data = WAREHOUSE_ZONES[zone_id]
                    with st.expander(f"Zone {zone_id} - {zone_data['name']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.number_input(f"Capacity", value=zone_data["capacity"], key=f"capacity_{zone_id}")
                        with col2:
                            st.selectbox(f"Type", ["High Value", "Fast Moving", "Seasonal", "Bulk Items"], 
                                        index=["High Value", "Fast Moving", "Seasonal", "Bulk Items"].index(zone_data["type"]) if zone_data["type"] in ["High Value", "Fast Moving", "Seasonal", "Bulk Items"] else 0,
                                        key=f"type_{zone_id}")
            
            with tab2:
                st.markdown("### 👥 User Management")
                
                # User roles configuration
                st.markdown("#### 🛡️ Role Permissions")
                for role, permissions in USER_ROLES.items():
                    with st.expander(f"{role} (Access Level: {permissions['access_level']})"):
                        st.multiselect(
                            f"Permissions for {role}",
                            ["view_all", "edit_all", "delete_all", "manage_users", "system_config", "view_inventory", "edit_inventory", "update_stock", "scan_items", "reports"],
                            default=permissions["permissions"],
                            key=f"permissions_{role}"
                        )
            
            with tab3:
                display_smart_notifications()
            
            with tab4:
                display_audit_trail()
            
            with tab5:
                st.markdown("### � Advanced Settings")
                
                # Advanced features toggle
                st.markdown("#### 🔧 Feature Toggles")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.checkbox("Enable RFID Tracking", value=True)
                    st.checkbox("Enable Predictive Analytics", value=True)
                    st.checkbox("Enable IoT Sensors", value=True)
                    st.checkbox("Enable Automation Rules", value=True)
                
                with col2:
                    st.checkbox("Enable Mobile Push Notifications", value=True)
                    st.checkbox("Enable Real-time Sync", value=True)
                    st.checkbox("Enable Audit Logging", value=True)
                    st.checkbox("Enable Smart Alerts", value=True)
                
                # Performance settings
                st.markdown("#### ⚡ Performance Settings")
                
                sync_interval = st.selectbox("Data Sync Interval", ["Real-time", "30 seconds", "1 minute", "5 minutes"])
                cache_duration = st.slider("Cache Duration (minutes)", 1, 60, 15)
                max_concurrent_users = st.number_input("Max Concurrent Users", 1, 100, 50)
                
                # Backup settings
                st.markdown("#### 💾 Backup Settings")
                
                backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
                backup_retention = st.number_input("Backup Retention (days)", 7, 365, 30)
                
                if st.button("💾 Create Backup Now"):
                    st.success("✅ Backup created successfully!")
        else:
            st.error("❌ Access denied: Insufficient permissions to view system settings")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #6c757d; padding: 20px;">
        🏭 <strong>Warehouse Management System</strong> | 
        👤 User: {user_role} | 
        🏢 Warehouse: {selected_warehouse} | 
        🕒 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
