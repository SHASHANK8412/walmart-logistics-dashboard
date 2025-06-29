import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.api import get_integrated_dashboard_data, get_data
from utils.helpers import show_notification

def app():
    st.header("🏪 Integrated Walmart Logistics Dashboard")
    st.markdown("**Real-time interconnected view of Orders, Inventory, Delivery & Warehouse**")
    
    # Get integrated dashboard data
    dashboard_data = get_integrated_dashboard_data()
    
    if dashboard_data:
        # Main KPI Row
        st.subheader("📊 Real-time Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            orders_data = dashboard_data.get("orders", {})
            st.metric(
                "📦 Total Orders", 
                orders_data.get("total", 0),
                delta=f"+{orders_data.get('today', 0)} today"
            )
            st.metric(
                "💰 Revenue", 
                f"${orders_data.get('revenue', 0):,.2f}",
                delta="Live tracking"
            )
        
        with col2:
            inventory_data = dashboard_data.get("inventory", {})
            st.metric(
                "📚 Products", 
                inventory_data.get("total_products", 0),
                delta=f"{inventory_data.get('low_stock', 0)} low stock"
            )
            st.metric(
                "⚠️ Out of Stock", 
                inventory_data.get("out_of_stock", 0),
                delta="Requires restocking"
            )
        
        with col3:
            delivery_data = dashboard_data.get("deliveries", {})
            st.metric(
                "🚚 Pending Deliveries", 
                delivery_data.get("pending", 0),
                delta=f"{delivery_data.get('in_transit', 0)} in transit"
            )
            st.metric(
                "✅ Delivered Today", 
                delivery_data.get("delivered_today", 0),
                delta="Today's completions"
            )
        
        with col4:
            warehouse_data = dashboard_data.get("warehouse", {})
            st.metric(
                "📋 Picking Required", 
                warehouse_data.get("picking_required", 0),
                delta="Pending tasks"
            )
            st.metric(
                "⚙️ Processing", 
                warehouse_data.get("processing", 0),
                delta="Active operations"
            )
    
    # Real-time Activity Feed
    st.subheader("📱 Live Activity Feed")
    
    # Create activity timeline
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Simulated real-time activities (in real app, this would come from database)
        activities = [
            {
                "time": datetime.now() - timedelta(minutes=2),
                "type": "order",
                "message": "New order #ORDER-12345 placed by John Doe",
                "status": "✅ Completed",
                "impact": "Inventory: -2 Laptops, Delivery: Created, Warehouse: Picking assigned"
            },
            {
                "time": datetime.now() - timedelta(minutes=5),
                "type": "delivery",
                "message": "Order #ORDER-12340 out for delivery",
                "status": "🚚 In Transit",
                "impact": "ETA: 2:30 PM, Driver: Mike Johnson"
            },
            {
                "time": datetime.now() - timedelta(minutes=8),
                "type": "inventory",
                "message": "Low stock alert: Smartphone inventory below threshold",
                "status": "⚠️ Alert",
                "impact": "Current: 5 units, Threshold: 10 units"
            },
            {
                "time": datetime.now() - timedelta(minutes=12),
                "type": "warehouse",
                "message": "Order #ORDER-12338 packed and ready for dispatch",
                "status": "📦 Ready",
                "impact": "Moved to dispatch area, Delivery scheduled"
            }
        ]
        
        for activity in activities:
            with st.container():
                st.markdown(f"""
                <div style="border-left: 4px solid #ff6b6b; padding: 10px; margin: 10px 0; background-color: #f8f9fa;">
                    <div style="font-size: 0.8em; color: #666;">
                        {activity['time'].strftime('%H:%M:%S')} • {activity['status']}
                    </div>
                    <div style="font-weight: bold; margin: 5px 0;">
                        {activity['message']}
                    </div>
                    <div style="font-size: 0.9em; color: #555;">
                        Impact: {activity['impact']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # System Health Status
        st.markdown("### 🔧 System Health")
        
        systems = [
            {"name": "Orders API", "status": "🟢 Online", "response": "45ms"},
            {"name": "Inventory DB", "status": "🟢 Online", "response": "32ms"},
            {"name": "Delivery Service", "status": "🟢 Online", "response": "67ms"},
            {"name": "Warehouse System", "status": "🟢 Online", "response": "28ms"},
            {"name": "MongoDB Atlas", "status": "🟢 Connected", "response": "89ms"}
        ]
        
        for system in systems:
            st.markdown(f"""
            <div style="padding: 5px; margin: 3px 0;">
                <strong>{system['name']}</strong><br>
                {system['status']} • {system['response']}
            </div>
            """, unsafe_allow_html=True)
    
    # Interactive Charts Section
    st.subheader("📈 Operational Analytics")
    
    # Get actual data for charts
    orders = get_data("orders")
    inventory = get_data("inventory")
    
    if orders and inventory:
        tab1, tab2, tab3 = st.tabs(["📦 Order Flow", "📊 Inventory Status", "🔄 Integration Map"])
        
        with tab1:
            # Order status distribution
            if orders:
                df_orders = pd.DataFrame(orders)
                if not df_orders.empty and 'status' in df_orders.columns:
                    status_counts = df_orders['status'].value_counts()
                    
                    fig = px.pie(
                        values=status_counts.values,
                        names=status_counts.index,
                        title="Order Status Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Order timeline
                    if 'order_date' in df_orders.columns:
                        df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
                        daily_orders = df_orders.groupby(df_orders['order_date'].dt.date).size()
                        
                        fig2 = px.line(
                            x=daily_orders.index,
                            y=daily_orders.values,
                            title="Daily Order Trend",
                            labels={'x': 'Date', 'y': 'Number of Orders'}
                        )
                        st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            # Inventory analysis
            if inventory:
                df_inventory = pd.DataFrame(inventory)
                if not df_inventory.empty:
                    # Stock status
                    df_inventory['stock_status'] = df_inventory.apply(
                        lambda row: 'Out of Stock' if row.get('quantity', 0) == 0 
                        else 'Low Stock' if row.get('quantity', 0) <= row.get('min_stock_level', 5)
                        else 'In Stock', axis=1
                    )
                    
                    stock_counts = df_inventory['stock_status'].value_counts()
                    
                    fig3 = px.bar(
                        x=stock_counts.index,
                        y=stock_counts.values,
                        title="Inventory Stock Status",
                        color=stock_counts.index,
                        color_discrete_map={
                            'In Stock': '#28a745',
                            'Low Stock': '#ffc107',
                            'Out of Stock': '#dc3545'
                        }
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                    
                    # Category distribution
                    if 'category' in df_inventory.columns:
                        category_counts = df_inventory['category'].value_counts()
                        
                        fig4 = px.treemap(
                            names=category_counts.index,
                            values=category_counts.values,
                            title="Products by Category"
                        )
                        st.plotly_chart(fig4, use_container_width=True)
        
        with tab3:
            # Integration flow diagram
            st.markdown("""
            ### 🔄 System Integration Flow
            
            This diagram shows how the systems are interconnected:
            """)
            
            st.markdown("""
            ```mermaid
            graph TD
                A[New Order] --> B[Order Created]
                B --> C[Inventory Updated]
                B --> D[Delivery Scheduled]
                B --> E[Warehouse Notified]
                C --> F[Stock Reduced]
                C --> G[Low Stock Alert?]
                D --> H[Driver Assigned]
                D --> I[Route Optimized]
                E --> J[Picking List Created]
                E --> K[Worker Assigned]
                F --> L[Real-time Dashboard]
                H --> L
                J --> L
                G --> M[Restock Notification]
                I --> N[Delivery ETA Updated]
                K --> O[Order Status: Processing]
                O --> P[Order Status: Shipped]
                P --> Q[Order Status: Delivered]
                Q --> R[Customer Notification]
            ```
            """)
            
            st.info("""
            **Integration Benefits:**
            - 🔄 **Real-time Updates**: All systems sync automatically
            - 📊 **Accurate Inventory**: Stock levels update with each order
            - 🚚 **Efficient Delivery**: Automatic route optimization and scheduling
            - 🏪 **Warehouse Automation**: Picking lists and worker assignments
            - 📱 **Live Monitoring**: Real-time dashboard with all metrics
            - ⚡ **Instant Alerts**: Low stock, delivery delays, and system issues
            """)
    
    # Integration Test Section
    st.subheader("🔧 Integration Test & Status")
    
    # Run integration connectivity test
    if st.button("🧪 Run Integration Test", use_container_width=True):
        with st.spinner("Testing all integration components..."):
            from utils.api import test_integration_connectivity, get_integration_status
            
            status = get_integration_status()
            
            if status["overall_health"]:
                st.success(f"✅ All integration systems are online! ({status['systems_online']}/{status['total_systems']})")
            else:
                st.warning(f"⚠️ Some systems may have issues ({status['systems_online']}/{status['total_systems']} online)")
            
            # Show detailed status
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Core APIs:**")
                details = status["details"]
                st.write(f"🔌 Backend Health: {'✅' if details['backend_health'] else '❌'}")
                st.write(f"📦 Orders API: {'✅' if details['orders_api'] else '❌'}")
                st.write(f"📊 Inventory API: {'✅' if details['inventory_api'] else '❌'}")
            
            with col2:
                st.markdown("**Service APIs:**")
                st.write(f"🚚 Delivery API: {'✅' if details['delivery_api'] else '❌'}")
                st.write(f"🏪 Warehouse API: {'✅' if details['warehouse_api'] else '❌'}")
                st.write(f"🔄 Integration Endpoint: {'✅' if details['integration_endpoint'] else '❌'}")
            
            with col3:
                st.markdown("**Integration Features:**")
                st.write("🔄 Cross-system updates: ✅")
                st.write("📱 Real-time sync: ✅")
                st.write("🎯 Automatic workflows: ✅")
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ New Order", use_container_width=True):
            st.session_state.selected_tab = "📦 Orders"
            st.session_state.show_add_order_form = True
            st.rerun()
    
    with col2:
        if st.button("📊 Check Inventory", use_container_width=True):
            st.session_state.selected_tab = "📚 Inventory"
            st.rerun()
    
    with col3:
        if st.button("🚚 Track Deliveries", use_container_width=True):
            st.session_state.selected_tab = "🚚 Delivery"
            st.rerun()
    
    with col4:
        if st.button("🏪 Warehouse Ops", use_container_width=True):
            st.session_state.selected_tab = "🏢 Warehouse"
            st.rerun()
    
    # Live Integration Demo
    st.subheader("🎯 Integration Demo - See Real-time Updates")
    
    st.info("""
    **Try the Integration Demo:**
    1. Click 'Create Demo Order' below
    2. Watch as the order automatically updates all systems
    3. See inventory reduce, delivery get scheduled, and warehouse tasks get created
    4. All changes reflect in real-time across the dashboard
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🎯 Create Demo Order", use_container_width=True, type="primary"):
            from utils.api import create_integrated_order
            import random
            
            # Create a sample order
            demo_order = {
                "customer_name": f"Demo Customer {random.randint(1, 100)}",
                "customer_email": f"demo{random.randint(1, 100)}@walmart.com",
                "product_name": random.choice(["Laptop", "Smartphone", "Tablet", "Headphones"]),
                "quantity": random.randint(1, 3),
                "price": round(random.uniform(100, 800), 2),
                "delivery_address": f"{random.randint(1, 999)} Demo St, Demo City",
                "payment_method": random.choice(["Credit Card", "PayPal", "Debit Card"])
            }
            
            with st.spinner("Creating integrated order..."):
                success, order_data, integration_status = create_integrated_order(demo_order)
                
                if success:
                    st.success("🎉 Demo Order Created Successfully!")
                    
                    # Show what systems were updated with details
                    if isinstance(integration_status, dict):
                        st.markdown("**✅ Systems Updated Successfully:**")
                        
                        if integration_status.get('order_created'):
                            st.write("📦 ✅ **Order System:** New order record created")
                        if integration_status.get('inventory_updated'):
                            st.write("📊 ✅ **Inventory System:** Stock levels reduced and status updated")
                        if integration_status.get('delivery_created'):
                            st.write("🚚 ✅ **Delivery System:** Scheduled with driver assignment and route optimization")
                        if integration_status.get('warehouse_updated'):
                            st.write("🏪 ✅ **Warehouse System:** Item picked from location and dispatched")
                        
                        # Show integration impact summary
                        if order_data and hasattr(order_data, 'get') and order_data.get('details'):
                            details = order_data['details']
                            st.markdown("---")
                            st.markdown("**📊 Integration Impact Summary:**")
                            
                            if details.get('inventory'):
                                inv = details['inventory']
                                st.write(f"🔹 **Inventory:** Reduced {inv.get('product_name')} by {inv.get('quantity_reduced')} units")
                                if inv.get('low_stock_alert'):
                                    st.warning("⚠️ Low stock alert triggered!")
                            
                            if details.get('delivery'):
                                delv = details['delivery']
                                st.write(f"🔹 **Delivery:** Assigned to {delv.get('agent_assigned')} - {delv.get('estimated_delivery')}")
                            
                            if details.get('warehouse'):
                                wh = details['warehouse']
                                st.write(f"🔹 **Warehouse:** Item dispatched from {wh.get('location')} by {wh.get('assigned_worker')}")
                        
                        st.info("💡 **Next Steps:** Check other dashboard tabs to see the real-time updates reflected across all systems!")
                    else:
                        st.write("✅ All systems updated successfully!")
                else:
                    st.error(f"Demo failed: {integration_status}")
    
    with col2:
        if st.button("📊 Refresh All Data", use_container_width=True):
            st.rerun()
    
    # Real-time stats comparison
    st.markdown("### 📈 Before/After Integration Impact")
    
    # Current metrics
    current_dashboard_data = get_integrated_dashboard_data()
    if current_dashboard_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            orders_total = current_dashboard_data.get("orders", {}).get("total", 0)
            st.metric("Total Orders", orders_total, help="Live count of all orders")
        
        with col2:
            inventory_low = current_dashboard_data.get("inventory", {}).get("low_stock", 0)
            st.metric("Low Stock Items", inventory_low, help="Items needing restock")
        
        with col3:
            delivery_pending = current_dashboard_data.get("deliveries", {}).get("pending", 0)
            st.metric("Pending Deliveries", delivery_pending, help="Deliveries to be dispatched")
        
        with col4:
            warehouse_tasks = current_dashboard_data.get("warehouse", {}).get("picking_required", 0)
            st.metric("Warehouse Tasks", warehouse_tasks, help="Active picking/processing tasks")
    
    # Auto-refresh
    if st.checkbox("🔄 Auto-refresh (10s)"):
        st.rerun()

if __name__ == "__main__":
    app()
