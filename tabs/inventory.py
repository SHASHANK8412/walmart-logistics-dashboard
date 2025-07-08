import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
from utils.api import get_data, post_data, put_data, get_integrated_dashboard_data
from utils.helpers import display_kpi_metrics, plot_category_pie_chart, show_notification
from utils.products import get_product_info, get_all_products, get_all_categories, get_category_stats, update_stock_level, get_low_stock_products

def create_sample_inventory_data():
    """Create comprehensive sample inventory data"""
    all_products = get_all_products()
    categories = get_all_categories()
    
    inventory_data = []
    suppliers = ["Walmart Distribution", "Amazon Logistics", "Target Supply", "Best Buy Wholesale", "Costco Direct"]
    locations = ["Warehouse A1", "Warehouse B2", "Warehouse C3", "Storage D4", "Freezer E5"]
    
    item_id = 1000
    for product_name, product_info in all_products.items():
        # Extract price from price range
        price_range = product_info.get('price_range', '$0 - $0')
        import re
        prices = re.findall(r'\d+\.?\d*', price_range.replace(',', ''))
        cost_price = float(prices[0]) * 0.7 if prices else 10.0  # 30% markup
        selling_price = float(prices[0]) if prices else 15.0
        
        stock_qty = product_info.get('stock_level', 50)
        reorder_level = max(10, stock_qty // 3)
        
        # Determine stock status
        if stock_qty == 0:
            status = "Out of Stock"
        elif stock_qty <= reorder_level:
            status = "Low Stock"
        else:
            status = "In Stock"
        
        inventory_data.append({
            'item_id': f"WM{item_id}",
            'item_name': product_name,
            'sku': f"SKU{item_id}",
            'category': product_info.get('category', 'General'),
            'brand': product_info.get('brand', 'Generic'),
            'stock_quantity': stock_qty,
            'reorder_level': reorder_level,
            'supplier': suppliers[item_id % len(suppliers)],
            'location': locations[item_id % len(locations)],
            'cost_price': round(cost_price, 2),
            'selling_price': round(selling_price, 2),
            'last_updated': (datetime.now() - timedelta(days=item_id % 30)).strftime('%Y-%m-%d'),
            'status': status,
            'image_url': product_info.get('image_url', ''),
            'expiry_date': (datetime.now() + timedelta(days=90 + (item_id % 200))).strftime('%Y-%m-%d') if product_info.get('category') == 'Grocery' else None
        })
        item_id += 1
    
    return pd.DataFrame(inventory_data)
    st.header("📚 Inventory Management")
    
    # Integration Status Banner
    st.info("🔄 **Real-time Inventory**: Stock levels update automatically when orders are placed!")
    
    # Check for recent inventory updates (for order notifications)
    if 'last_inventory_update' in st.session_state:
        if st.session_state.last_inventory_update:
            update_info = st.session_state.last_inventory_update
            product_name = update_info.get('product_name', 'Unknown')
            
            # Display clean inventory update notification
            st.success("🎉 **Inventory Updated Due to Recent Order!**")
            
            # Clean notification display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.info(f"**Product:** {product_name}")
            with col2:
                st.warning(f"**Deducted:** {update_info.get('quantity_deducted', 0)} units")
            with col3:
                st.metric("Previous Stock", update_info.get('previous_stock', 0))
            with col4:
                st.metric("Current Stock", update_info.get('current_stock', 0))
            
            if update_info.get('low_stock_alert'):
                st.error("⚠️ **LOW STOCK ALERT!**")
            
            st.caption(f"Order processed at: {update_info.get('timestamp', 'Now')}")
            
            # Clear the notification after showing it
            if st.button("✅ Acknowledge Update"):
                st.session_state.last_inventory_update = None
                st.rerun()
    
    # Get inventory data
    inventory = get_data("inventory")
    
    # Display KPIs
    if inventory:
        low_stock_items = sum(1 for item in inventory if item.get('quantity', 0) < item.get('min_stock_level', 10))
        
        kpi_data = {
            'inventory_items': len(inventory),
            'low_stock': low_stock_items,
            'low_stock_delta': f"+{low_stock_items} alerts" if low_stock_items > 0 else "No alerts"
        }
        
        display_kpi_metrics(kpi_data)
    
    # Inventory Visualization
    if inventory:
        tab1, tab2 = st.tabs(["Inventory Table", "Category Distribution"])
        
        # Tab 1: Inventory Table
        with tab1:
            # Filters
            with st.expander("Filters", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    # SKU filter
                    sku_filter = st.text_input("Filter by SKU")
                
                with col2:
                    # Low stock filter
                    show_low_stock = st.checkbox("Show only low stock items")
            
            # Convert to DataFrame
            df = pd.DataFrame(inventory)
            
            # Apply filters
            if not df.empty:
                if sku_filter:
                    df = df[df['sku'].str.contains(sku_filter, case=False)]
                
                if show_low_stock:
                    df = df[df['quantity'] < df['min_stock_level']]
                
                if not df.empty:
                    # Enhanced inventory display with product images
                    st.subheader("📦 Inventory with Product Images")
                    
                    # Display inventory in visual cards
                    inventory_items = df.to_dict('records')
                    
                    # Show inventory using clean display
                    from utils.styles import create_simple_inventory_display
                    
                    # Option to toggle between clean and detailed view
                    view_mode = st.radio("Display Mode:", ["Clean View", "Detailed View"], horizontal=True)
                    
                    if view_mode == "Clean View":
                        # Simple text-based display
                        st.markdown("### 📋 Inventory Summary")
                        for i, item in enumerate(inventory_items[:9]):
                            product_name = item.get('product_name', item.get('name', 'Unknown Product'))
                            sku = item.get('sku', 'N/A')
                            quantity = item.get('stock_quantity', item.get('quantity', 0))
                            min_stock = item.get('min_stock_level', 10)
                            price = item.get('price', 0.0)
                            
                            # Simple status indicator
                            stock_status = "🔴 Low Stock" if quantity < min_stock else "🟢 In Stock"
                            
                            # Clean display without styling code
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.write(f"**{product_name}**")
                                st.caption(f"SKU: {sku}")
                            with col2:
                                st.metric("Stock", quantity)
                            with col3:
                                st.metric("Min Level", min_stock)
                            with col4:
                                if quantity < min_stock:
                                    st.error("Low Stock")
                                else:
                                    st.success("In Stock")
                            
                            st.divider()
                    
                    else:
                        # Detailed view with images (styling hidden in backend)
                        cols = st.columns(3)
                        for i, item in enumerate(inventory_items[:9]):
                            with cols[i % 3]:
                                product_name = item.get('product_name', item.get('name', 'Unknown Product'))
                                sku = item.get('sku', 'N/A')
                                quantity = item.get('stock_quantity', item.get('quantity', 0))
                                min_stock = item.get('min_stock_level', 10)
                                price = item.get('price', 0.0)
                                
                                # Get product info for image
                                product_info = get_product_info(product_name)
                                
                                # Use styling from backend (hidden from user)
                                from utils.styles import create_clean_inventory_card
                                inventory_card_html = create_clean_inventory_card(
                                    product_name, sku, quantity, min_stock, price, product_info
                                )
                                st.markdown(inventory_card_html, unsafe_allow_html=True)
                    
                    if len(inventory_items) > 9:
                        st.info(f"Showing 9 of {len(inventory_items)} items. Use filters to narrow down results.")
                    
                    # Traditional table view toggle
                    if st.checkbox("📊 Show Detailed Table View"):
                        st.dataframe(df, use_container_width=True)
                    
                    # Inventory actions
                    st.subheader("Inventory Actions")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        selected_sku = st.selectbox("Select SKU", df['sku'].tolist())
                    
                    with col2:
                        quantity_change = st.number_input("Quantity Change", value=0, step=1)
                    
                    if st.button("Update Stock"):
                        if quantity_change != 0:
                            # Get current quantity
                            current_item = next((item for item in inventory if item['sku'] == selected_sku), None)
                            
                            if current_item:
                                # Use stock_quantity for MongoDB compatibility
                                current_qty = current_item.get('stock_quantity', current_item.get('quantity', 0))
                                new_quantity = current_qty + quantity_change
                                
                                if new_quantity >= 0:
                                    success, _ = put_data("inventory", selected_sku, {"stock_quantity": new_quantity})
                                    
                                    if success:
                                        show_notification(f"Updated {selected_sku} stock to {new_quantity}", "success")
                                        st.rerun()
                                    else:
                                        show_notification("Failed to update inventory", "error")
                                else:
                                    show_notification("Quantity cannot be negative", "warning")
                else:
                    st.info("No inventory items match the selected filters.")
                    
        # Tab 2: Category Distribution
        with tab2:
            if not df.empty and 'category' in df.columns:
                fig = plot_category_pie_chart(df, "Inventory by Category")
                st.pyplot(fig)
            else:
                st.info("No category data available for visualization.")
    else:
        st.warning("Could not fetch inventory data. Please check API connection.")
    
    # Add New SKU Form
    with st.expander("Add New SKU"):
        with st.form("new_sku_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sku = st.text_input("SKU")
                name = st.text_input("Product Name")
                category = st.text_input("Category")
                
            with col2:
                quantity = st.number_input("Quantity", min_value=0, value=0)
                bin_location = st.text_input("Bin Location")
                min_stock = st.number_input("Minimum Stock Level", min_value=1, value=10)
            
            submit_button = st.form_submit_button("Add SKU")
            
            if submit_button:
                if sku and name and category and bin_location:
                    new_item = {
                        "sku": sku,
                        "name": name,
                        "category": category,
                        "quantity": quantity,
                        "bin_location": bin_location,
                        "min_stock_level": min_stock
                    }
                    
                    success, _ = post_data("inventory", new_item)
                    if success:
                        show_notification(f"Added new SKU: {sku}", "success")
                        st.rerun()
                    else:
                        show_notification("Failed to add new SKU", "error")
                else:
                    show_notification("Please fill all required fields", "warning")

def display_inventory_kpis(df):
    """Display comprehensive inventory KPIs"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_skus = len(df)
        st.metric(
            label="📦 Total SKUs",
            value=total_skus,
            delta=f"+{total_skus//10} this month"
        )
    
    with col2:
        total_stock = df['stock_quantity'].sum()
        st.metric(
            label="📊 Total Stock",
            value=f"{total_stock:,}",
            delta=f"+{total_stock//20} units"
        )
    
    with col3:
        low_stock = len(df[df['status'] == 'Low Stock'])
        st.metric(
            label="⚠️ Low Stock Items",
            value=low_stock,
            delta=f"-{max(0, low_stock-5)} from last week",
            delta_color="inverse"
        )
    
    with col4:
        out_of_stock = len(df[df['status'] == 'Out of Stock'])
        st.metric(
            label="🚫 Out of Stock",
            value=out_of_stock,
            delta=f"+{out_of_stock}" if out_of_stock > 0 else "No items",
            delta_color="inverse" if out_of_stock > 0 else "normal"
        )
    
    with col5:
        recent_updates = len(df[df['last_updated'] >= (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')])
        st.metric(
            label="🔄 Recent Updates",
            value=recent_updates,
            delta="Last 7 days"
        )

def display_inventory_filters(df):
    """Display comprehensive filter options"""
    st.subheader("🔍 Search & Filter Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Search functionality
        search_term = st.text_input("🔎 Search by Item Name or SKU", placeholder="Enter item name or SKU...")
        
        # Category filter
        categories = ['All'] + sorted(df['category'].unique().tolist())
        category_filter = st.selectbox("📂 Filter by Category", categories)
    
    with col2:
        # Status filter
        status_options = ['All'] + sorted(df['status'].unique().tolist())
        status_filter = st.selectbox("📊 Filter by Stock Status", status_options)
        
        # Supplier filter
        suppliers = ['All'] + sorted(df['supplier'].unique().tolist())
        supplier_filter = st.selectbox("🏢 Filter by Supplier", suppliers)
    
    with col3:
        # Location filter
        locations = ['All'] + sorted(df['location'].unique().tolist())
        location_filter = st.selectbox("📍 Filter by Location", locations)
        
        # Stock range filter
        stock_range = st.slider("📦 Stock Quantity Range", 
                               min_value=0, 
                               max_value=int(df['stock_quantity'].max()), 
                               value=(0, int(df['stock_quantity'].max())))
    
    return {
        'search_term': search_term,
        'category': category_filter,
        'status': status_filter,
        'supplier': supplier_filter,
        'location': location_filter,
        'stock_range': stock_range
    }

def apply_filters(df, filters):
    """Apply all filters to the dataframe"""
    filtered_df = df.copy()
    
    # Search filter
    if filters['search_term']:
        mask = (filtered_df['item_name'].str.contains(filters['search_term'], case=False, na=False) |
                filtered_df['sku'].str.contains(filters['search_term'], case=False, na=False))
        filtered_df = filtered_df[mask]
    
    # Category filter
    if filters['category'] != 'All':
        filtered_df = filtered_df[filtered_df['category'] == filters['category']]
    
    # Status filter
    if filters['status'] != 'All':
        filtered_df = filtered_df[filtered_df['status'] == filters['status']]
    
    # Supplier filter
    if filters['supplier'] != 'All':
        filtered_df = filtered_df[filtered_df['supplier'] == filters['supplier']]
    
    # Location filter
    if filters['location'] != 'All':
        filtered_df = filtered_df[filtered_df['location'] == filters['location']]
    
    # Stock range filter
    filtered_df = filtered_df[
        (filtered_df['stock_quantity'] >= filters['stock_range'][0]) &
        (filtered_df['stock_quantity'] <= filters['stock_range'][1])
    ]
    
    return filtered_df

def display_bulk_actions(df):
    """Display bulk action controls"""
    st.subheader("⚡ Bulk Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📤 Export to CSV", use_container_width=True):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="inventory_export.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("CSV export ready!")
    
    with col2:
        if st.button("📊 Export to Excel", use_container_width=True):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Inventory', index=False)
            
            b64 = base64.b64encode(buffer.getvalue()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="inventory_export.xlsx">Download Excel</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("Excel export ready!")
    
    with col3:
        if st.button("🔄 Bulk Update Stock", use_container_width=True):
            st.session_state.show_bulk_update = True
    
    with col4:
        if st.button("📦 Import Inventory", use_container_width=True):
            st.session_state.show_import = True

def display_stock_adjustment_panel():
    """Display stock adjustment controls"""
    st.subheader("📋 Stock Adjustment Panel")
    
    with st.expander("🔧 Adjust Stock Levels", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**➕ Add Stock (Incoming Goods)**")
            add_sku = st.text_input("SKU for Stock Addition")
            add_quantity = st.number_input("Quantity to Add", min_value=1, value=1)
            add_reason = st.selectbox("Reason", ["New Delivery", "Return", "Found Inventory", "Correction"])
            
            if st.button("Add Stock"):
                st.success(f"Added {add_quantity} units to {add_sku}")
        
        with col2:
            st.markdown("**➖ Reduce Stock**")
            reduce_sku = st.text_input("SKU for Stock Reduction")
            reduce_quantity = st.number_input("Quantity to Reduce", min_value=1, value=1)
            reduce_reason = st.selectbox("Reason ", ["Damaged", "Lost", "Expired", "Transfer Out", "Correction"])
            
            if st.button("Reduce Stock"):
                st.success(f"Reduced {reduce_quantity} units from {reduce_sku}")

def display_inventory_alerts(df):
    """Display inventory alerts and notifications"""
    st.subheader("🚨 Inventory Alerts")
    
    alerts = []
    
    # Low stock alerts
    low_stock_items = df[df['status'] == 'Low Stock']
    if not low_stock_items.empty:
        alerts.append({
            'type': 'warning',
            'title': f"⚠️ {len(low_stock_items)} Low Stock Items",
            'items': low_stock_items['item_name'].tolist()[:5]
        })
    
    # Out of stock alerts
    out_of_stock_items = df[df['status'] == 'Out of Stock']
    if not out_of_stock_items.empty:
        alerts.append({
            'type': 'error',
            'title': f"🚫 {len(out_of_stock_items)} Out of Stock Items",
            'items': out_of_stock_items['item_name'].tolist()[:5]
        })
    
    # Expiry warnings (for grocery items)
    if 'expiry_date' in df.columns:
        near_expiry = df[
            (df['expiry_date'].notna()) & 
            (pd.to_datetime(df['expiry_date']) <= datetime.now() + timedelta(days=30))
        ]
        if not near_expiry.empty:
            alerts.append({
                'type': 'info',
                'title': f"📅 {len(near_expiry)} Items Expiring Soon",
                'items': near_expiry['item_name'].tolist()[:5]
            })
    
    # Overstocked items
    overstocked = df[df['stock_quantity'] > df['reorder_level'] * 5]
    if not overstocked.empty:
        alerts.append({
            'type': 'info',
            'title': f"📈 {len(overstocked)} Overstocked Items",
            'items': overstocked['item_name'].tolist()[:5]
        })
    
    # Display alerts
    if alerts:
        for alert in alerts:
            if alert['type'] == 'warning':
                st.warning(f"**{alert['title']}**\n" + ", ".join(alert['items']) + 
                          (f" and {len(alert['items'])-5} more..." if len(alert['items']) > 5 else ""))
            elif alert['type'] == 'error':
                st.error(f"**{alert['title']}**\n" + ", ".join(alert['items']) + 
                        (f" and {len(alert['items'])-5} more..." if len(alert['items']) > 5 else ""))
            else:
                st.info(f"**{alert['title']}**\n" + ", ".join(alert['items']) + 
                       (f" and {len(alert['items'])-5} more..." if len(alert['items']) > 5 else ""))
    else:
        st.success("✅ No critical alerts at this time!")

def display_inventory_analytics(df):
    """Display inventory analytics and visualizations"""
    st.subheader("📈 Inventory Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Stock Distribution", "💰 Value Analysis", "📈 Trends", "🏆 Top Items"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Stock status distribution
            status_counts = df['status'].value_counts()
            fig_status = px.pie(values=status_counts.values, names=status_counts.index, 
                               title="Stock Status Distribution")
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Category distribution
            category_counts = df['category'].value_counts()
            fig_category = px.bar(x=category_counts.index, y=category_counts.values,
                                 title="Items by Category")
            st.plotly_chart(fig_category, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Total inventory value
            df['total_value'] = df['stock_quantity'] * df['cost_price']
            total_value = df['total_value'].sum()
            st.metric("💰 Total Inventory Value", f"${total_value:,.2f}")
            
            # Value by category
            value_by_category = df.groupby('category')['total_value'].sum().sort_values(ascending=False)
            fig_value = px.bar(x=value_by_category.index, y=value_by_category.values,
                              title="Inventory Value by Category")
            st.plotly_chart(fig_value, use_container_width=True)
        
        with col2:
            # Margin analysis
            df['margin'] = df['selling_price'] - df['cost_price']
            df['margin_percent'] = (df['margin'] / df['cost_price'] * 100).round(2)
            avg_margin = df['margin_percent'].mean()
            st.metric("📊 Average Margin", f"{avg_margin:.1f}%")
            
            # Top margin items
            top_margin = df.nlargest(10, 'margin_percent')[['item_name', 'margin_percent']]
            st.markdown("**🏆 Top Margin Items**")
            st.dataframe(top_margin, use_container_width=True)
    
    with tab3:
        # Stock trends (simulated)
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
        trend_data = []
        for date in dates:
            total_stock = df['stock_quantity'].sum() + (hash(str(date)) % 1000 - 500)
            trend_data.append({'date': date, 'total_stock': max(0, total_stock)})
        
        trend_df = pd.DataFrame(trend_data)
        fig_trend = px.line(trend_df, x='date', y='total_stock', title="Stock Levels Over Time")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Turnover ratio
        st.markdown("**📊 Inventory Turnover Analysis**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔄 Avg Turnover Ratio", "4.2x/year")
        with col2:
            st.metric("📦 Days on Hand", "87 days")
        with col3:
            st.metric("💨 Fast Moving Items", "23%")
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Top stock items
            top_stock = df.nlargest(10, 'stock_quantity')[['item_name', 'stock_quantity', 'category']]
            st.markdown("**📦 Highest Stock Items**")
            st.dataframe(top_stock, use_container_width=True)
        
        with col2:
            # Most valuable items
            top_value = df.nlargest(10, 'total_value')[['item_name', 'total_value', 'category']]
            st.markdown("**💰 Most Valuable Items**")
            st.dataframe(top_value, use_container_width=True)

def app():
    st.header("📚 Advanced Inventory Management Dashboard")
    
    # Integration Status Banner
    st.success("🔄 **Real-time Inventory Management**: Comprehensive warehouse management with advanced analytics!")
    
    # Display inventory update alerts from recent orders
    display_inventory_update_alerts()
    
    # Check for legacy inventory updates (backward compatibility)
    if 'last_inventory_update' in st.session_state and st.session_state.last_inventory_update:
        update_info = st.session_state.last_inventory_update
        st.success(f"🎉 **Inventory Updated**: {update_info.get('product_name', 'Item')} stock changed by {update_info.get('quantity_deducted', 0)} units")
        
        if st.button("✅ Clear Notification"):
            st.session_state.last_inventory_update = None
            st.rerun()
    
    # Create sample data (in real app, this would come from database)
    df = create_sample_inventory_data()
    
    # 1. INVENTORY SUMMARY SECTION
    display_inventory_kpis(df)
    
    st.markdown("---")
    
    # 2. SEARCH AND FILTER SECTION
    filters = display_inventory_filters(df)
    filtered_df = apply_filters(df, filters)
    
    st.markdown("---")
    
    # 3. BULK ACTIONS
    display_bulk_actions(filtered_df)
    
    # Handle bulk update modal
    if st.session_state.get('show_bulk_update', False):
        with st.expander("🔄 Bulk Stock Update", expanded=True):
            selected_skus = st.multiselect("Select SKUs", filtered_df['sku'].tolist())
            update_type = st.radio("Update Type", ["Add Stock", "Set Stock", "Reduce Stock"])
            quantity = st.number_input("Quantity", min_value=1, value=1)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Apply Bulk Update"):
                    st.success(f"Updated {len(selected_skus)} items with {update_type}")
                    st.session_state.show_bulk_update = False
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.show_bulk_update = False
                    st.rerun()
    
    # Handle import modal
    if st.session_state.get('show_import', False):
        with st.expander("📤 Import Inventory", expanded=True):
            uploaded_file = st.file_uploader("Choose CSV/Excel file", type=['csv', 'xlsx'])
            if uploaded_file:
                st.success("File uploaded successfully!")
                if st.button("Process Import"):
                    st.success("Inventory imported successfully!")
                    st.session_state.show_import = False
                    st.rerun()
            
            if st.button("Cancel Import"):
                st.session_state.show_import = False
                st.rerun()
    
    st.markdown("---")
    
    # 4. INVENTORY ALERTS
    display_inventory_alerts(filtered_df)
    
    st.markdown("---")
    
    # 5. STOCK ADJUSTMENT PANEL
    display_stock_adjustment_panel()
    
    st.markdown("---")
    
    # 6. INVENTORY TABLE VIEW
    st.subheader("📋 Inventory Table View")
    
    # Display results count
    st.info(f"📊 Showing **{len(filtered_df)}** of **{len(df)}** items")
    
    # Configure columns to display
    display_columns = st.multiselect(
        "Select columns to display:",
        ['item_name', 'sku', 'category', 'brand', 'stock_quantity', 'reorder_level', 
         'supplier', 'location', 'cost_price', 'selling_price', 'last_updated', 'status'],
        default=['item_name', 'sku', 'category', 'stock_quantity', 'reorder_level', 'status']
    )
    
    if display_columns:
        # Style the dataframe based on status
        def highlight_status(row):
            if row['status'] == 'Out of Stock':
                return ['background-color: #ffebee'] * len(row)
            elif row['status'] == 'Low Stock':
                return ['background-color: #fff3e0'] * len(row)
            else:
                return [''] * len(row)
        
        # Display the table
        display_df = filtered_df[display_columns].copy()
        st.dataframe(
            display_df.style.apply(highlight_status, axis=1),
            use_container_width=True,
            height=400
        )
        
        # Individual item actions
        if not filtered_df.empty:
            st.subheader("🔧 Individual Item Actions")
            selected_item = st.selectbox("Select Item for Action", filtered_df['item_name'].tolist())
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("✏️ Edit Item"):
                    st.info(f"Editing {selected_item}")
            with col2:
                if st.button("📦 Adjust Stock"):
                    st.info(f"Adjusting stock for {selected_item}")
            with col3:
                if st.button("📍 Move Location"):
                    st.info(f"Moving {selected_item}")
            with col4:
                if st.button("🗑️ Archive Item"):
                    st.warning(f"Archiving {selected_item}")
    
    st.markdown("---")
    
    # 7. INVENTORY ANALYTICS
    display_inventory_analytics(filtered_df)
    
    # Quick actions sidebar
    with st.sidebar:
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        if st.button("📊 Generate Report", use_container_width=True, key="inventory_main_report"):
            st.success("Report generated!")
        
        if st.button("⚙️ System Settings", use_container_width=True):
            st.info("Opening settings...")
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        st.metric("Total Value", f"${(filtered_df['stock_quantity'] * filtered_df['cost_price']).sum():,.2f}")
        st.metric("Categories", filtered_df['category'].nunique())
        st.metric("Suppliers", filtered_df['supplier'].nunique())
        st.metric("Locations", filtered_df['location'].nunique())

def display_inventory_update_alerts():
    """Display inventory update alerts from recent orders"""
    
    # Check for recent inventory updates
    if 'inventory_updates' in st.session_state and st.session_state.inventory_updates:
        st.markdown("### 🚨 **RECENT INVENTORY UPDATES**")
        
        for i, update in enumerate(st.session_state.inventory_updates[-5:]):  # Show last 5 updates
            # Create a prominent alert card
            alert_color = "#dc3545" if update.get('low_stock_alert') else "#28a745"
            
            alert_html = f"""
            <div style="
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                border: 3px solid {alert_color};
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
                animation: pulse 2s infinite;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #2c3e50;">
                            📦 Order Processed: {update['product_name']}
                        </h4>
                        <p style="margin: 5px 0; font-size: 14px;">
                            <strong>Quantity Deducted:</strong> {update['quantity_deducted']} units
                        </p>
                        <p style="margin: 5px 0; font-size: 14px;">
                            <strong>Stock Level:</strong> {update['previous_stock']} → {update['current_stock']} units
                        </p>
                        <p style="margin: 5px 0; font-size: 12px; color: #6c757d;">
                            Order: #{update.get('order_id', 'N/A')} | {update.get('timestamp', 'Now')}
                        </p>
                    </div>
                    <div style="text-align: center;">
                        {'<div style="background: #dc3545; color: white; padding: 8px 12px; border-radius: 8px; font-weight: bold;">⚠️ LOW STOCK!</div>' if update.get('low_stock_alert') else '<div style="background: #28a745; color: white; padding: 8px 12px; border-radius: 8px; font-weight: bold;">✅ UPDATED</div>'}
                    </div>
                </div>
            </div>
            
            <style>
            @keyframes pulse {{
                0% {{ box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); }}
                50% {{ box-shadow: 0 8px 25px rgba(255, 193, 7, 0.6); }}
                100% {{ box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); }}
            }}
            </style>
            """
            
            st.markdown(alert_html, unsafe_allow_html=True)
        
        # Clear alerts button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✅ Clear All Alerts", type="primary", use_container_width=True):
                st.session_state.inventory_updates = []
                st.rerun()
        
        st.markdown("---")
