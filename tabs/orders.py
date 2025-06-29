import streamlit as st
import pandas as pd
import datetime
from utils.api import get_data, post_data, put_data, delete_data, create_integrated_order, update_order_status_integrated, get_integrated_dashboard_data
from utils.helpers import display_kpi_metrics, format_date, show_notification

def app():
    st.header("📦 Orders Management")
    
    # Integration Status Banner
    st.info("🔄 **Integrated Order System**: Orders automatically update Inventory, Delivery, and Warehouse systems in real-time!")
    
    # Get orders data
    orders = get_data("orders")
    
    # Display KPIs
    if orders:
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        orders_today = sum(1 for order in orders if format_date(order.get('order_date', '')) == today)
        pending_orders = sum(1 for order in orders if order.get('status') == 'pending')
        
        kpi_data = {
            'orders_today': orders_today,
            'orders_delta': f"+{orders_today} today",
            'deliveries_pending': pending_orders
        }
        
        display_kpi_metrics(kpi_data)
    
    # Filters
    with st.expander("Filters", expanded=True):
        col1, col2 = st.columns(2)
        
        # Date filter
        with col1:
            min_date = datetime.datetime.today() - datetime.timedelta(days=30)
            max_date = datetime.datetime.today()
            date_range = st.date_input(
                "Order Date Range",
                (min_date, max_date),
                min_value=min_date - datetime.timedelta(days=365),
                max_value=max_date
            )
        
        # Status filter
        with col2:
            status_filter = st.multiselect(
                "Status", 
                ["pending", "shipped", "cancelled"], 
                default=["pending", "shipped"]
            )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh"):
            orders = get_data("orders")
            st.rerun()
    
    with col3:
        if st.button("➕ Add New Order"):
            st.session_state.show_add_order_form = True
    
    # Orders table
    if orders:
        df = pd.DataFrame(orders)
        
        # Apply filters if there's data
        if not df.empty:
            # Convert date string to datetime for filtering
            df['order_date'] = pd.to_datetime(df['order_date'])
            
            # Apply date filter if it exists
            if 'date_range' in locals() and len(date_range) == 2:
                start_date, end_date = date_range
                df = df[(df['order_date'].dt.date >= start_date) & 
                        (df['order_date'].dt.date <= end_date)]
            
            # Apply status filter
            if status_filter:
                df = df[df['status'].isin(status_filter)]
            
            if not df.empty:
                # Format date for display
                df['order_date'] = df['order_date'].dt.strftime('%Y-%m-%d')
                
                # Add action buttons column
                df['Actions'] = None
                
                # Display the table
                st.dataframe(df)
                
                # Order actions
                st.subheader("Order Actions")
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_order = st.selectbox("Select Order ID", df['order_id'].tolist())
                
                with col2:
                    action = st.selectbox("Action", ["Cancel Order", "Mark as Dispatched"])
                    
                if st.button("Apply Action"):
                    if action == "Cancel Order":
                        success, updated_order = update_order_status_integrated(selected_order, "cancelled")
                        if success:
                            show_notification(f"Order #{selected_order} has been cancelled and inventory restored.", "success")
                            st.rerun()
                        else:
                            show_notification("Failed to cancel order.", "error")
                    elif action == "Mark as Dispatched":
                        success, updated_order = update_order_status_integrated(selected_order, "shipped")
                        if success:
                            show_notification(f"Order #{selected_order} has been dispatched. Delivery and warehouse updated.", "success")
                            st.rerun()
                        else:
                            show_notification("Failed to dispatch order.", "error")
            else:
                st.info("No orders match the selected filters.")
        else:
            st.info("No orders found in the system.")
    else:
        st.warning("Could not fetch orders data. Please check API connection.")
    
    # Add new order form
    if st.session_state.get('show_add_order_form', False):
        st.subheader("Add New Order")
        
        with st.form("new_order_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer_name = st.text_input("Customer Name", placeholder="Enter customer full name")
                customer_email = st.text_input("Customer Email", placeholder="customer@example.com")
                product_name = st.text_input("Product Name", placeholder="Enter product name")
            
            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=1)
                price = st.number_input("Price ($)", min_value=0.01, value=10.00, step=0.01)
                payment_method = st.selectbox("Payment Method", ["Credit Card", "PayPal", "Cash on Delivery"])
            
            delivery_address = st.text_area("Delivery Address", placeholder="Enter full delivery address")
            
            submit_button = st.form_submit_button("Create Order")
            cancel_button = st.form_submit_button("Cancel")
            
            if cancel_button:
                st.session_state.show_add_order_form = False
                st.rerun()
            
            if submit_button:
                # Validate required fields
                if customer_name and customer_email and product_name and delivery_address and quantity > 0 and price > 0:
                    new_order = {
                        "customer_name": customer_name,
                        "customer_email": customer_email,
                        "product_name": product_name,
                        "quantity": quantity,
                        "price": price,
                        "delivery_address": delivery_address,
                        "payment_method": payment_method,
                        "status": "pending",
                        "order_date": datetime.datetime.now().isoformat()
                    }
                    
                    # Use integrated order creation
                    success, order_data, integration_status = create_integrated_order(new_order)
                    if success:
                        st.success("✅ Order created successfully!")
                        
                        # Show integration status
                        if isinstance(integration_status, dict):
                            st.success("🎉 **Complete System Integration Successful!**")
                            
                            # Show detailed status for each system
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.info(f"📦 **Order Created**\n{'✅ Success' if integration_status.get('order_created') else '❌ Failed'}")
                            with col2:
                                st.info(f"📊 **Inventory Updated**\n{'✅ Stock Deducted' if integration_status.get('inventory_updated') else '❌ Failed'}")
                            with col3:
                                st.info(f"🚚 **Delivery Scheduled**\n{'✅ Driver Assigned' if integration_status.get('delivery_created') else '❌ Failed'}")
                            with col4:
                                st.info(f"🏪 **Warehouse Dispatched**\n{'✅ Item Picked' if integration_status.get('warehouse_updated') else '❌ Failed'}")
                            
                            # Show detailed integration results if available
                            if hasattr(order_data, 'get') and order_data.get('details'):
                                details = order_data['details']
                                
                                st.markdown("---")
                                st.markdown("### 🔍 **Integration Details**")
                                
                                tab1, tab2, tab3 = st.tabs(["📊 Inventory Impact", "🚚 Delivery Info", "🏪 Warehouse Status"])
                                
                                with tab1:
                                    if details.get('inventory'):
                                        inv = details['inventory']
                                        st.write(f"**Product:** {inv.get('product_name')}")
                                        st.write(f"**Quantity Picked:** {inv.get('quantity_reduced')} units")
                                        st.write(f"**New Stock Level:** {inv.get('new_stock_level')} units")
                                        st.write(f"**Status:** {inv.get('status', 'Updated')}")
                                        if inv.get('low_stock_alert'):
                                            st.warning("⚠️ **Low Stock Alert!** - Restock recommended")
                                
                                with tab2:
                                    if details.get('delivery'):
                                        delv = details['delivery']
                                        st.write(f"**Delivery ID:** {delv.get('delivery_id')}")
                                        st.write(f"**Driver:** {delv.get('agent_assigned')}")
                                        st.write(f"**Delivery Address:** {delv.get('delivery_address')}")
                                        st.write(f"**Estimated Delivery:** {delv.get('estimated_delivery')}")
                                        st.write(f"**Status:** {delv.get('status', 'Scheduled')}")
                                        st.write(f"**Tracking Number:** {delv.get('tracking_number')}")
                                        
                                        # Google Maps integration details
                                        if delv.get('route_info'):
                                            route = delv['route_info']
                                            st.markdown("---")
                                            st.markdown("**🗺️ Google Maps Route Details:**")
                                            if route.get('distance'):
                                                st.write(f"📏 **Distance:** {route['distance'].get('miles', 'N/A')} miles")
                                            if route.get('duration'):
                                                st.write(f"⏱️ **Duration:** {route['duration'].get('text', 'N/A')}")
                                            if route.get('google_maps_link'):
                                                st.markdown(f"🔗 [**View Route on Google Maps**]({route['google_maps_link']})")
                                            if route.get('traffic_aware'):
                                                st.success("🚦 **Traffic-Aware Routing:** Enabled")
                                        
                                        if delv.get('google_maps_link'):
                                            st.markdown(f"🗺️ [**Track Delivery Live**]({delv.get('google_maps_link')})")
                                        
                                        if delv.get('delivery_fee'):
                                            st.info(f"💰 **Delivery Fee:** ${delv.get('delivery_fee')} (Distance-based pricing)")
                                        
                                        if delv.get('google_integration'):
                                            gi = delv['google_integration']
                                            st.success(f"✅ **Google Maps Integration Active** - API Version: {gi.get('api_version', 'v3')}")
                                            if gi.get('geocoded'):
                                                st.write("📍 Address successfully geocoded")
                                            if gi.get('route_calculated'):
                                                st.write("🛣️ Route calculated with real-time traffic")
                                            if gi.get('maps_link_generated'):
                                                st.write("🔗 Interactive maps link generated")
                                
                                with tab3:
                                    if details.get('warehouse'):
                                        wh = details['warehouse']
                                        st.write(f"**Warehouse ID:** {wh.get('warehouse_id')}")
                                        st.write(f"**Location:** {wh.get('location')}")
                                        st.write(f"**Assigned Worker:** {wh.get('assigned_worker')}")
                                        st.write(f"**Status:** {wh.get('status', 'Processed')}")
                                        st.write(f"**Zone:** {wh.get('zone', 'N/A')}")
                                        st.write(f"**Quality Check:** {wh.get('quality_status', 'Passed')}")
                                        if wh.get('dispatch_message'):
                                            st.success(f"📦 {wh.get('dispatch_message')}")
                        else:
                            # Fallback display for simple integration status
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.info(f"📦 Order: ✅")
                            with col2:
                                st.info(f"📊 Inventory: ✅")
                            with col3:
                                st.info(f"🚚 Delivery: ✅")
                            with col4:
                                st.info(f"🏪 Warehouse: ✅")
                        
                        show_notification("Order created and all systems updated!", "success")
                        st.session_state.show_add_order_form = False
                        st.rerun()
                    else:
                        show_notification(f"Failed to create order: {integration_status}", "error")
                else:
                    show_notification("❌ Missing required fields: Customer Name, Email, Product Name, Quantity, Price, and Delivery Address are required.", "error")
    
    # Quick Integration Demo
    with st.expander("🎯 Integration Demo", expanded=False):
        st.markdown("""
        **How Integration Works:**
        1. **Create Order** → Order system records the order
        2. **Auto-Update Inventory** → Stock levels decrease automatically  
        3. **Schedule Delivery** → Delivery agent assigned and route optimized
        4. **Warehouse Alert** → Picking task created for warehouse staff
        5. **Real-time Sync** → All changes visible across all dashboard tabs instantly
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Create Sample Integrated Order", use_container_width=True):
                import random
                
                sample_order = {
                    "customer_name": f"Integration Demo User {random.randint(1, 999)}",
                    "customer_email": f"demo{random.randint(1, 999)}@integration.test",
                    "product_name": random.choice(["Demo Laptop", "Demo Phone", "Demo Tablet"]),
                    "quantity": random.randint(1, 2),
                    "price": round(random.uniform(100, 500), 2),
                    "delivery_address": f"{random.randint(1, 999)} Integration Ave, Demo City",
                    "payment_method": "Demo Payment"
                }
                
                success, order_data, integration_status = create_integrated_order(sample_order)
                if success:
                    st.success("🎉 Integration Demo Complete! Check other tabs to see the updates.")
                    if isinstance(integration_status, dict):
                        for system, status in integration_status.items():
                            st.write(f"✅ {system.replace('_', ' ').title()}: {'Updated' if status else 'Failed'}")
                else:
                    st.error(f"Demo failed: {integration_status}")
        
        with col2:
            st.markdown("**Integration Benefits:**")
            st.write("⚡ Real-time updates")
            st.write("🎯 Zero manual sync")
            st.write("📊 Consistent data")
            st.write("🔄 Automatic workflows")
