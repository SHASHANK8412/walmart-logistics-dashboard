import streamlit as st
import pandas as pd
import datetime
import time
from utils.api import get_data, post_data, put_data, delete_data, create_integrated_order, update_order_status_integrated, get_integrated_dashboard_data, create_order_with_inventory_update, update_inventory_on_order
from utils.helpers import display_kpi_metrics, format_date, show_notification
from utils.products import get_product_info, get_all_products, display_product_card, display_product_grid, get_all_categories, get_products_by_category
from utils.styles import create_glassmorphism_card, create_hero_section, create_status_badge, create_modern_progress_bar

def app():
    """World-class orders management application"""
    
    # Hero Section
    hero_html = create_hero_section(
        title="📦 Smart Order Management",
        subtitle="AI-Powered Order Processing • Real-time Inventory Sync • Advanced Analytics • Seamless Customer Experience",
        gradient_type="primary"
    )
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # Add toggle for clean/detailed view
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 🎛️ Order Control Center")
    with col2:
        view_mode = st.selectbox("View Mode", ["Clean", "Detailed"], key="orders_view_mode")
    
    if view_mode == "Clean":
        # Use simplified interface without styling
        display_clean_orders_interface()
    else:
        # Use detailed interface with full styling
        display_detailed_orders_interface_full()

def display_clean_orders_interface():
    """World-class clean orders interface"""
    
    # Integration Status Banner
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 16px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        text-align: center;
    ">
        <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 8px;">
            🔄 <strong>Integrated Order Ecosystem</strong>
        </div>
        <div style="font-size: 0.95rem; opacity: 0.95;">
            Orders automatically sync with Inventory, Delivery, and Warehouse systems in real-time!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get orders data
    orders = get_data("orders")
    
    # Display Enhanced KPIs
    if orders:
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        orders_today = sum(1 for order in orders if format_date(order.get('order_date', '')) == today)
        pending_orders = sum(1 for order in orders if order.get('status') == 'pending')
        completed_orders = sum(1 for order in orders if order.get('status') == 'completed')
        total_revenue = sum(order.get('total_amount', 0) for order in orders if format_date(order.get('order_date', '')) == today)
        
        # Modern KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Orders Today", str(orders_today), f"+{orders_today}")
        
        with col2:
            st.metric("⏳ Pending Orders", str(pending_orders), f"{pending_orders} active")
        
        with col3:
            st.metric("✅ Completed", str(completed_orders), f"+{completed_orders}")
        
        with col4:
            st.metric("💰 Revenue Today", f"${total_revenue:,.0f}", "+8.3%")
    
    # Check if payment page should be displayed
    if st.session_state.get('show_payment_page', False):
        display_payment_page()
        return
    
    # Modern Shopping Cart Interface
    st.markdown("---")
    
    cart_header_html = """
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px 30px;
        border-radius: 16px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    ">
        <h2 style="margin: 0; font-family: 'Poppins', sans-serif; font-weight: 600;">
            🛒 Smart Shopping Cart
        </h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 1rem;">
            Advanced cart management with real-time pricing and inventory sync
        </p>
    </div>
    """
    st.markdown(cart_header_html, unsafe_allow_html=True)
    
    # Initialize cart
    if 'shopping_cart' not in st.session_state:
        st.session_state.shopping_cart = []
    
    if st.session_state.shopping_cart:
        # Modern Cart Items Display
        cart_container_html = """
        <div style="
            background: white;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
        ">
        """
        st.markdown(cart_container_html, unsafe_allow_html=True)
        
        # Display cart items with modern styling
        for i, item in enumerate(st.session_state.shopping_cart):
            item_html = f"""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 20px;
                margin: 15px 0;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease;
            " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="flex: 1;">
                        <h4 style="margin: 0 0 8px 0; color: #1f2937; font-weight: 600;">
                            {item['name']}
                        </h4>
                        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                            <span style="background: rgba(102, 126, 234, 0.1); color: #4f46e5; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">
                                {item['category']}
                            </span>
                            <span style="color: #6b7280; font-size: 0.9rem;">
                                Brand: {item.get('brand', 'N/A')}
                            </span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #059669; margin-bottom: 5px;">
                            ${item['price']:.2f}
                        </div>
                        <div style="color: #6b7280; font-size: 0.9rem;">
                            Qty: {item['quantity']} • Total: ${item['price'] * item['quantity']:.2f}
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(item_html, unsafe_allow_html=True)
            
            # Interactive controls in columns
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col2:
                new_qty = st.number_input("Qty", min_value=1, value=item['quantity'], key=f"qty_{i}")
                if new_qty != item['quantity']:
                    st.session_state.shopping_cart[i]['quantity'] = new_qty
                    st.rerun()
            
            with col3:
                new_price = st.number_input("Price", min_value=0.01, value=item['price'], key=f"price_{i}")
                if abs(new_price - item['price']) > 0.01:
                        st.session_state.shopping_cart[i]['price'] = new_price
                        st.rerun()
                
                with col4:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.shopping_cart.pop(i)
                        st.rerun()
        
        # Cart total
        cart_total = sum(item['quantity'] * item['price'] for item in st.session_state.shopping_cart)
        st.metric("Cart Total", f"${cart_total:.2f}")
        
        # Checkout button
        if st.button("🛒 Proceed to Checkout", type="primary"):
            st.session_state.show_payment_page = True
            st.session_state.show_checkout = False
            st.rerun()
        
        # Clear cart
        if st.button("🗑️ Clear Cart"):
            st.session_state.shopping_cart = []
            st.rerun()
    else:
        st.info("Your cart is empty. Add products from the catalog below!")

    # Product Catalog
    st.markdown("---")
    st.markdown("## 🏪 Product Catalog")
    
    # Get categories
    categories = get_all_categories()
    
    # Create tabs for categories
    category_tabs = st.tabs([f"{info['icon']} {category}" for category, info in categories.items()])
    
    for i, (category, category_info) in enumerate(categories.items()):
        with category_tabs[i]:
            st.markdown(f"### {category_info['icon']} {category}")
            st.info(category_info['description'])
            
            # Get products in this category
            category_products = get_products_by_category(category)
            
            if category_products:
                # Display products in grid
                cols = st.columns(3)
                for j, (product_name, product_info) in enumerate(category_products.items()):
                    with cols[j % 3]:
                        # Simple product display
                        with st.container():
                            st.image(product_info['image_url'], use_container_width=True)
                            st.subheader(product_name)
                            st.caption(f"{category_info['icon']} {category}")
                            st.write(f"**Brand:** {product_info['brand']}")
                            st.write(f"**Price:** {product_info['price_range']}")
                            st.write(f"**Stock:** {product_info['stock_level']} units")
                            
                            # Add to cart button
                            if st.button(f"🛒 Add to Cart", key=f"add_{product_name}_{category}"):
                                # Check if already in cart
                                existing_item = next(
                                    (item for item in st.session_state.shopping_cart if item['name'] == product_name), 
                                    None
                                )
                                
                                if existing_item:
                                    # Increase quantity
                                    existing_item['quantity'] += 1
                                    st.success(f"Updated {product_name} quantity in cart!")
                                else:
                                    # Add new item with actual price
                                    from utils.products import get_product_actual_price
                                    actual_price = get_product_actual_price(product_name)
                                    
                                    cart_item = {
                                        'name': product_name,
                                        'category': category,
                                        'brand': product_info['brand'],
                                        'image_url': product_info['image_url'],
                                        'quantity': 1,
                                        'price': actual_price,  # Use actual price from product catalog
                                        'stock_level': product_info['stock_level']
                                    }
                                    st.session_state.shopping_cart.append(cart_item)
                                    st.success(f"Added {product_name} to cart!")
                                
                                st.rerun()
            else:
                st.info(f"No products available in {category} category.")
    
    # Recent Orders
    if orders:
        st.markdown("---")
        st.markdown("## 📋 Recent Orders")
        
        # Display recent orders in a simple table
        df = pd.DataFrame(orders)
        st.dataframe(df[['order_id', 'customer_name', 'product_name', 'quantity', 'price', 'status']].head(10))


def display_payment_page():
    """Display payment page for checkout"""
    st.markdown("---")
    st.header("💳 Secure Payment Processing")
    
    if st.session_state.shopping_cart:
        # Import payment processor
        from utils.payment_methods import PaymentProcessor, display_payment_form, display_payment_confirmation, get_payment_summary
        
        # Initialize payment processor
        payment_processor = PaymentProcessor()
        
        # Calculate cart total
        cart_total = sum(item['quantity'] * item['price'] for item in st.session_state.shopping_cart)
        
        # Display cart summary
        st.markdown("### 🛍️ Order Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Items", len(st.session_state.shopping_cart))
        with col2:
            st.metric("Total Quantity", sum(item['quantity'] for item in st.session_state.shopping_cart))
        with col3:
            st.metric("Subtotal", f"${cart_total:.2f}")
        
        # Display items in cart
        st.markdown("### 📦 Items in Your Cart")
        for item in st.session_state.shopping_cart:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{item['name']}**")
                st.caption(f"{item['category']} - {item.get('brand', 'N/A')}")
            with col2:
                st.write(f"Qty: {item['quantity']}")
            with col3:
                st.write(f"${item['price']:.2f}")
            with col4:
                st.write(f"${item['quantity'] * item['price']:.2f}")
        
        # Display payment form
        selected_method, payment_details = display_payment_form(cart_total, payment_processor, "orders_detailed")
        
        # Payment buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💳 Process Payment", type="primary", use_container_width=True):
                if selected_method and payment_details:
                    # Process payment
                    with st.spinner("Processing payment..."):
                        success, message, transaction_details = payment_processor.process_payment(
                            cart_total, selected_method, payment_details
                        )
                    
                    if success:
                        # Show spectacular success animation
                        st.balloons()
                        st.success("🎉 **PAYMENT SUCCESSFUL!** 🎉")
                        st.success("✅ **Your order has been confirmed and is being processed!**")
                        
                        # Display payment confirmation
                        display_payment_confirmation(transaction_details)
                        
                        # Clear cart and reset session state
                        st.session_state.shopping_cart = []
                        st.session_state.show_payment_page = False
                        st.rerun()
                    else:
                        st.error(f"❌ Payment failed: {message}")
                else:
                    st.error("❌ Please select a payment method and fill in all required details.")
        
        with col2:
            if st.button("← Back to Cart", use_container_width=True):
                st.session_state.show_payment_page = False
                st.rerun()
        
        with col3:
            if st.button("❌ Cancel Order", use_container_width=True):
                st.session_state.show_payment_page = False
                st.session_state.shopping_cart = []
                st.rerun()
    else:
        st.warning("Your cart is empty. Please add items to proceed with checkout.")
        if st.button("← Back to Shopping"):
            st.session_state.show_payment_page = False
            st.rerun()


def display_detailed_orders_interface_full():
    """Detailed orders interface with full styling (existing implementation)"""
    
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
    
    # Orders table with enhanced visual display
    if orders:
        # Show recent orders with product images
        st.subheader("📦 Recent Orders with Product Images")
        
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
                
                # Display orders with product images in cards
                st.markdown("### 🛍️ Order Gallery")
                
                # Convert dataframe back to list of dictionaries for easier handling
                filtered_orders = df.to_dict('records')
                
                # Show orders in a visual grid (first 6 orders)
                for i, order in enumerate(filtered_orders[:6]):
                    product_name = order.get('product_name', 'Unknown Product')
                    quantity = order.get('quantity', 1)
                    price = order.get('price', 0.0)
                    customer_name = order.get('customer_name', 'Unknown Customer')
                    status = order.get('status', 'pending')
                    order_date = order.get('order_date', '')
                    
                    # Create enhanced order card with product image
                    product_card_html = display_product_card(product_name, quantity, price, show_details=True)
                    
                    # Add order information to the card
                    order_info_html = f"""
                    <div style="
                        background: #f8f9fa; 
                        border-radius: 8px; 
                        padding: 12px; 
                        margin-top: 10px;
                        border-left: 4px solid {'#28a745' if status == 'delivered' else '#ffc107' if status == 'pending' else '#dc3545'};
                    ">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px;">
                            <div><strong>👤 Customer:</strong> {customer_name}</div>
                            <div><strong>📅 Date:</strong> {order_date}</div>
                            <div><strong>📧 Order ID:</strong> {order.get('order_id', 'N/A')}</div>
                            <div><strong>🏷️ Status:</strong> 
                                <span style="
                                    background: {'#28a745' if status == 'delivered' else '#ffc107' if status == 'pending' else '#dc3545'};
                                    color: white;
                                    padding: 2px 8px;
                                    border-radius: 12px;
                                    font-size: 11px;
                                ">{status.upper()}</span>
                            </div>
                        </div>
                    </div>
                    """
                    
                    # Display the complete order card
                    st.markdown(product_card_html + order_info_html, unsafe_allow_html=True)
                    
                    # Add some spacing between orders
                    if i < len(filtered_orders[:6]) - 1:
                        st.markdown("<br>", unsafe_allow_html=True)
                
                if len(filtered_orders) > 6:
                    st.info(f"Showing 6 of {len(filtered_orders)} orders. Use filters to narrow down results.")
                
                # Traditional table view toggle
                if st.checkbox("📊 Show Detailed Table View"):
                    # Add total price column
                    df['total_price'] = df['quantity'] * df['price']
                    st.dataframe(df, use_container_width=True)
                
                # Order actions
                st.subheader("⚙️ Order Management")
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
    
    # Add new order form with shopping cart and categorized product catalog
    if st.session_state.get('show_add_order_form', False):
        st.subheader("🛒 Shopping Cart & Product Catalog")
        
        # Initialize shopping cart in session state
        if 'shopping_cart' not in st.session_state:
            st.session_state.shopping_cart = []
        
        # Import additional functions for categories
        from utils.products import get_all_categories, get_products_by_category, display_category_selector
        
        # Shopping Cart Display
        if st.session_state.shopping_cart:
            st.markdown("### 🛍️ Your Shopping Cart")
            
            cart_total = 0
            cart_items_html = ""
            
            for i, item in enumerate(st.session_state.shopping_cart):
                product_name = item['name']
                quantity = item['quantity']
                price = item['price']
                category = item['category']
                image_url = item['image_url']
                
                item_total = quantity * price
                cart_total += item_total
                
                # Get category color
                category_info = get_all_categories().get(category, {'color': '#95a5a6', 'icon': '📦'})
                
                cart_items_html += f"""
                <div style="
                    border: 2px solid {category_info['color']};
                    border-radius: 12px;
                    padding: 15px;
                    margin: 10px 0;
                    background: white;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                ">
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <img src="{image_url}" 
                             alt="{product_name}" 
                             style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; border: 2px solid {category_info['color']};">
                        
                        <div style="flex: 1;">
                            <h5 style="margin: 0 0 5px 0; color: #2c3e50;">{product_name}</h5>
                            <p style="margin: 2px 0; color: {category_info['color']}; font-size: 12px; font-weight: bold;">
                                {category_info['icon']} {category}
                            </p>
                            <div style="display: flex; gap: 10px; margin-top: 8px; align-items: center;">
                                <span style="background: #3498db; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                                    Qty: {quantity}
                                </span>
                                <span style="background: #27ae60; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                                    ${price:.2f}/unit
                                </span>
                                <span style="background: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                                    Total: ${item_total:.2f}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                """
            
            st.markdown(cart_items_html, unsafe_allow_html=True)
            
            # Cart Summary
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            ">
                <h3 style="margin: 0;">🛍️ Cart Total: ${cart_total:.2f}</h3>
                <p style="margin: 5px 0;">Items in cart: {len(st.session_state.shopping_cart)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Cart Actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🗑️ Clear Cart", use_container_width=True):
                    st.session_state.shopping_cart = []
                    st.rerun()
            
            with col2:
                if st.button("✏️ Edit Quantities", use_container_width=True):
                    st.session_state.show_cart_editor = True
                    st.rerun()
            
            with col3:
                if st.button("🛒 Proceed to Checkout", use_container_width=True, type="primary"):
                    st.session_state.show_payment_page = True
                    st.session_state.show_checkout = False
                    st.rerun()
        
        # Category selection and product display
        st.markdown("### 🏷️ Shop by Category")
        
        # Get all categories
        categories = get_all_categories()
        
        # Display category selector as tabs
        category_tabs = st.tabs([f"{info['icon']} {category}" for category, info in categories.items()])
        
        for i, (category, category_info) in enumerate(categories.items()):
            with category_tabs[i]:
                st.markdown(f"""
                <div style="background: {category_info['color']}; color: white; padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h4 style="margin: 0; color: white;">{category_info['icon']} {category}</h4>
                    <p style="margin: 5px 0; color: #f0f0f0;">{category_info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Get products in this category
                category_products = get_products_by_category(category)
                
                if category_products:
                    # Display products in this category
                    cols = st.columns(3)
                    for j, (product_name, product_info) in enumerate(category_products.items()):
                        with cols[j % 3]:
                            # Create enhanced product card with add to cart functionality
                            stock_level = product_info.get('stock_level', 0)
                            in_stock = stock_level > 0
                            
                            product_card_html = f"""
                            <div style="
                                border: 2px solid {category_info['color']};
                                border-radius: 12px;
                                padding: 15px;
                                margin: 10px 0;
                                background: white;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                                text-align: center;
                                transition: all 0.3s ease;
                                opacity: {'1' if in_stock else '0.7'};
                            ">
                                <img src="{product_info['image_url']}" 
                                     alt="{product_name}" 
                                     style="width: 100%; height: 150px; object-fit: cover; border-radius: 8px; margin-bottom: 10px;">
                                
                                <h5 style="margin: 5px 0; color: #2c3e50; font-size: 14px;">{product_name}</h5>
                                <p style="margin: 2px 0; color: {category_info['color']}; font-size: 11px; font-weight: bold;">
                                    {category_info['icon']} {category}
                                </p>
                                <p style="margin: 2px 0; color: #7f8c8d; font-size: 11px;">Brand: {product_info['brand']}</p>
                                <p style="margin: 5px 0; color: #34495e; font-size: 10px; line-height: 1.3;">
                                    {product_info['description'][:60]}...
                                </p>
                                <p style="margin: 5px 0; color: #27ae60; font-weight: bold; font-size: 12px;">
                                    {product_info['price_range']}
                                </p>
                                
                                <div style="background: #f8f9fa; padding: 5px; border-radius: 5px; margin: 10px 0;">
                                    <span style="font-size: 10px; color: {'#27ae60' if in_stock else '#dc3545'};">
                                        {'✅ In Stock' if in_stock else '❌ Out of Stock'} ({stock_level} units)
                                    </span>
                                </div>
                            </div>
                            """
                            st.markdown(product_card_html, unsafe_allow_html=True)
                            
                            # Add to cart controls
                            if in_stock:
                                col1, col2 = st.columns(2)
                                with col1:
                                    quantity = st.number_input(
                                        "Qty", 
                                        min_value=1, 
                                        max_value=min(stock_level, 10), 
                                        value=1, 
                                        key=f"qty_{product_name}_{category}"
                                    )
                                
                                with col2:
                                    # Extract average price from price range
                                    price_range = product_info['price_range'].replace('$', '').replace(',', '')
                                    try:
                                        if ' - ' in price_range:
                                            min_price, max_price = price_range.split(' - ')
                                            avg_price = (float(min_price) + float(max_price)) / 2
                                        else:
                                            avg_price = float(price_range.split('/')[0])
                                    except:
                                        avg_price = 10.0
                                    
                                    price = st.number_input(
                                        "Price", 
                                        min_value=0.01, 
                                        value=avg_price, 
                                        step=0.01,
                                        key=f"price_{product_name}_{category}"
                                    )
                                
                                # Add to Cart button
                                if st.button(
                                    f"🛒 Add to Cart", 
                                    key=f"add_{product_name}_{category}",
                                    use_container_width=True,
                                    type="primary"
                                ):
                                    # Check if item already in cart
                                    existing_item = next(
                                        (item for item in st.session_state.shopping_cart if item['name'] == product_name), 
                                        None
                                    )
                                    
                                    if existing_item:
                                        # Update quantity if item exists
                                        existing_item['quantity'] += quantity
                                        st.success(f"Updated {product_name} quantity in cart!")
                                    else:
                                        # Add new item to cart
                                        cart_item = {
                                            'name': product_name,
                                            'category': category,
                                            'quantity': quantity,
                                            'price': price,
                                            'image_url': product_info['image_url'],
                                            'brand': product_info['brand']
                                        }
                                        st.session_state.shopping_cart.append(cart_item)
                                        st.success(f"Added {product_name} to cart!")
                                    
                                    st.rerun()
                            else:
                                st.button(
                                    "❌ Out of Stock", 
                                    key=f"oos_{product_name}_{category}",
                                    use_container_width=True,
                                    disabled=True
                                )
                else:
                    st.info(f"No products available in {category} category.")
        
        # Cart Editor Modal
        if st.session_state.get('show_cart_editor', False):
            st.markdown("---")
            st.subheader("✏️ Edit Cart Items")
            
            for i, item in enumerate(st.session_state.shopping_cart):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{item['name']}** ({item['category']})")
                
                with col2:
                    new_qty = st.number_input(
                        "Quantity", 
                        min_value=1, 
                        value=item['quantity'], 
                        key=f"edit_qty_{i}"
                    )
                    st.session_state.shopping_cart[i]['quantity'] = new_qty
                
                with col3:
                    new_price = st.number_input(
                        "Price", 
                        min_value=0.01, 
                        value=item['price'], 
                        step=0.01,
                        key=f"edit_price_{i}"
                    )
                    st.session_state.shopping_cart[i]['price'] = new_price
                
                with col4:
                    if st.button("🗑️", key=f"remove_{i}", help="Remove item"):
                        st.session_state.shopping_cart.pop(i)
                        st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Save Changes", use_container_width=True):
                    st.session_state.show_cart_editor = False
                    st.success("Cart updated successfully!")
                    st.rerun()
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_cart_editor = False
                    st.rerun()
        
        # Payment Page
        if st.session_state.get('show_payment_page', False):
            if st.session_state.shopping_cart:
                st.markdown("---")
                st.subheader("💳 Secure Payment Processing")
                
                # Import payment processor
                from utils.payment_methods import PaymentProcessor, display_payment_form, display_payment_confirmation, get_payment_summary
                
                # Initialize payment processor
                payment_processor = PaymentProcessor()
                
                # Calculate cart total
                cart_total = sum(item['quantity'] * item['price'] for item in st.session_state.shopping_cart)
                
                # Display cart summary
                st.markdown("### 🛍️ Order Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Items", len(st.session_state.shopping_cart))
                with col2:
                    st.metric("Total Quantity", sum(item['quantity'] for item in st.session_state.shopping_cart))
                with col3:
                    st.metric("Subtotal", f"${cart_total:.2f}")
                
                # Display payment form
                selected_method, payment_details = display_payment_form(cart_total, payment_processor, "orders_full")
                
                # Payment buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("💳 Process Payment", type="primary", use_container_width=True):
                        if selected_method and payment_details:
                            # Process payment
                            with st.spinner("Processing payment..."):
                                success, message, transaction_details = payment_processor.process_payment(
                                    cart_total, selected_method, payment_details
                                )
                            
                            if success:
                                # Show spectacular success animation
                                st.balloons()
                                st.success("🎉 **PAYMENT SUCCESSFUL!** 🎉")
                                st.success("✅ **Your order has been confirmed and is being processed!**")
                                
                                # Display payment confirmation
                                display_payment_confirmation(transaction_details)
                                
                                # AUTO-GENERATE ORDER BILL/RECEIPT
                                st.markdown("---")
                                st.markdown("### 🧾 **AUTOMATIC BILL GENERATION**")
                                
                                # Import receipt generator
                                from utils.receipts import auto_generate_order_receipt, display_auto_receipt
                                
                                # Prepare order data for receipt with customer details from payment
                                order_receipt_data = {
                                    "order_id": transaction_details.get('transaction_id', f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"),
                                    "customer_name": payment_details.get('customer_name', 'Valued Customer'),
                                    "customer_email": payment_details.get('email', 'customer@example.com'),
                                    "delivery_address": payment_details.get('billing_address', 'Address not provided'),
                                    "payment_method": selected_method.replace('_', ' ').title(),
                                    "special_instructions": "Paid via secure online payment",
                                    "quantity": sum(item['quantity'] for item in st.session_state.shopping_cart),
                                    "price": cart_total / sum(item['quantity'] for item in st.session_state.shopping_cart)
                                }
                                
                                # Generate and display the customer bill
                                receipt_result = auto_generate_order_receipt(order_receipt_data, st.session_state.shopping_cart)
                                display_auto_receipt(receipt_result)
                                
                                # Update inventory for each item
                                st.markdown("---")
                                st.markdown("### 📦 **Inventory Updates**")
                                inventory_updates = []
                                for cart_item in st.session_state.shopping_cart:
                                    product_name = cart_item['name']
                                    quantity = cart_item['quantity']
                                    inv_success, inv_result = update_inventory_on_order(product_name, quantity)
                                    if inv_success:
                                        inventory_updates.append(inv_result)
                                        st.success(f"✅ {inv_result['product_name']}: Stock reduced by {inv_result['quantity_deducted']} units (New stock: {inv_result['current_stock']})")
                                        if inv_result['low_stock_alert']:
                                            st.warning(f"⚠️ LOW STOCK ALERT: {inv_result['product_name']} is running low!")
                                
                                # Clear cart and reset state
                                cart_backup = st.session_state.shopping_cart.copy()  # Backup for receipt
                                st.session_state.shopping_cart = []
                                st.session_state.show_payment_page = False
                                st.session_state.show_checkout = False
                                
                                # Store transaction for future reference
                                if 'completed_transactions' not in st.session_state:
                                    st.session_state.completed_transactions = []
                                
                                transaction_summary = {
                                    **transaction_details,
                                    'cart_items': cart_backup,
                                    'receipt_data': receipt_result.get('receipt_data', {}),
                                    'timestamp': datetime.datetime.now().isoformat()
                                }
                                st.session_state.completed_transactions.append(transaction_summary)
                                
                                # Success message with next steps
                                st.markdown("---")
                                st.success("🚀 **Order Processing Complete!**")
                                st.info("📧 A confirmation email will be sent to your email address.")
                                st.info("🚚 You will receive tracking information once your order ships.")
                                st.info("📞 For any questions, contact customer service at (479) 273-4000")
                                
                                # Show automatic redirect countdown
                                countdown_placeholder = st.empty()
                                for i in range(5, 0, -1):
                                    countdown_placeholder.info(f"🔄 Returning to shopping in {i} seconds...")
                                    time.sleep(1)
                                countdown_placeholder.empty()
                                st.rerun()
                            else:
                                st.error(f"❌ Payment Failed: {message}")
                        else:
                            st.error("Please fill in all required payment details.")
                
                with col2:
                    if st.button("⬅️ Back to Cart", use_container_width=True):
                        st.session_state.show_payment_page = False
                        st.rerun()
                
                with col3:
                    if st.button("❌ Cancel Order", use_container_width=True):
                        st.session_state.show_payment_page = False
                        st.session_state.shopping_cart = []
                        st.warning("Order cancelled and cart cleared.")
                        st.rerun()
            else:
                # Show message when cart is empty
                st.markdown("---")
                st.subheader("💳 Payment Page")
                st.warning("🛒 Your cart is empty! Please add items to your cart before proceeding to checkout.")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🛍️ Continue Shopping", use_container_width=True, type="primary"):
                        st.session_state.show_payment_page = False
                        st.rerun()
                with col2:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.show_payment_page = False
                        st.rerun()

        # Checkout Process
        if st.session_state.get('show_checkout', False) and st.session_state.shopping_cart:
            st.markdown("---")
            st.subheader("🛒 Checkout - Order Details")
            
            with st.form("checkout_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    customer_name = st.text_input("Customer Name", placeholder="Enter customer full name")
                    customer_email = st.text_input("Customer Email", placeholder="customer@example.com")
                    payment_method = st.selectbox("Payment Method", ["Credit Card", "PayPal", "Cash on Delivery"])
                
                with col2:
                    delivery_address = st.text_area("Delivery Address", placeholder="Enter full delivery address")
                    special_instructions = st.text_area("Special Instructions", placeholder="Any special delivery instructions")
                
                # Order Summary
                cart_total = sum(item['quantity'] * item['price'] for item in st.session_state.shopping_cart)
                total_items = sum(item['quantity'] for item in st.session_state.shopping_cart)
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%);
                    padding: 20px;
                    border-radius: 12px;
                    margin: 15px 0;
                    border-left: 6px solid #4CAF50;
                ">
                    <h4 style="margin: 0 0 10px 0; color: #2e7d32;">📋 Order Summary</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><strong>Total Items:</strong> {total_items} units</div>
                        <div><strong>Unique Products:</strong> {len(st.session_state.shopping_cart)}</div>
                        <div><strong>Subtotal:</strong> ${cart_total:.2f}</div>
                        <div><strong>Tax (8.5%):</strong> ${cart_total * 0.085:.2f}</div>
                    </div>
                    <div style="text-align: center; margin-top: 15px; background: #4CAF50; color: white; padding: 10px; border-radius: 8px;">
                        <strong style="font-size: 18px;">Total: ${cart_total * 1.085:.2f}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Submit buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    submit_button = st.form_submit_button("🛒 Place Order", use_container_width=True, type="primary")
                with col2:
                    cancel_button = st.form_submit_button("❌ Cancel Checkout", use_container_width=True)
                with col3:
                    back_button = st.form_submit_button("⬅️ Back to Cart", use_container_width=True)
                
                if cancel_button:
                    st.session_state.show_checkout = False
                    st.session_state.show_add_order_form = False
                    st.rerun()
                
                if back_button:
                    st.session_state.show_checkout = False
                    st.rerun()
                
                if submit_button:
                    # Validate required fields
                    if customer_name and customer_email and delivery_address:
                        # Show order processing animation
                        processing_placeholder = st.empty()
                        with processing_placeholder.container():
                            st.info("🔄 Processing your order...")
                            progress_bar = st.progress(0)
                            for i in range(100):
                                progress_bar.progress(i + 1)
                                time.sleep(0.01)
                        
                        # Process inventory updates for each item
                        inventory_updates = []
                        processing_errors = []
                        
                        for cart_item in st.session_state.shopping_cart:
                            product_name = cart_item['name']
                            quantity = cart_item['quantity']
                            
                            # Update inventory for this item
                            inv_success, inv_result = update_inventory_on_order(product_name, quantity)
                            if inv_success:
                                inventory_updates.append(inv_result)
                            else:
                                processing_errors.append(f"Inventory update failed for {product_name}: {inv_result}")
                        
                        # Clear processing animation
                        processing_placeholder.empty()
                        
                        # Create combined order
                        combined_order = {
                            "customer_name": customer_name,
                            "customer_email": customer_email,
                            "delivery_address": delivery_address,
                            "payment_method": payment_method,
                            "special_instructions": special_instructions,
                            "status": "pending",
                            "order_date": datetime.datetime.now().isoformat(),
                            "cart_items": st.session_state.shopping_cart,
                            "total_amount": cart_total * 1.085,
                            "tax_amount": cart_total * 0.085
                        }
                        
                        # Create main order with first item details
                        main_item = st.session_state.shopping_cart[0]
                        new_order = {
                            "customer_name": customer_name,
                            "customer_email": customer_email,
                            "product_name": f"Multi-item Order ({len(st.session_state.shopping_cart)} products)",
                            "quantity": total_items,
                            "price": cart_total / total_items,  # Average price per item
                            "delivery_address": delivery_address,
                            "payment_method": payment_method,
                            "status": "pending",
                            "order_date": datetime.datetime.now().isoformat(),
                            "cart_details": st.session_state.shopping_cart
                        }
                        
                        # Use integrated order creation
                        success, order_data, integration_status = create_integrated_order(new_order)
                        
                        if success:
                            # Display spectacular order confirmation with effects
                            st.balloons()
                            st.success("🎉 **MULTI-ITEM ORDER CONFIRMED SUCCESSFULLY!** 🎉")
                            
                            # AUTO-GENERATE ORDER RECEIPT
                            st.markdown("---")
                            st.markdown("### 🧾 **AUTOMATIC RECEIPT GENERATION**")
                            
                            # Import receipt generator
                            from utils.receipts import auto_generate_order_receipt, display_auto_receipt
                            
                            # Prepare order data for receipt
                            order_receipt_data = {
                                "order_id": order_data.get('order_id', f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"),
                                "customer_name": customer_name,
                                "customer_email": customer_email,
                                "delivery_address": delivery_address,
                                "payment_method": payment_method,
                                "special_instructions": special_instructions,
                                "quantity": total_items,
                                "price": cart_total / total_items if total_items > 0 else 0
                            }
                            
                            # Generate receipt with cart items
                            receipt_result = auto_generate_order_receipt(order_receipt_data, st.session_state.shopping_cart)
                            
                            # Display the receipt
                            display_auto_receipt(receipt_result)
                            
                            # Show inventory updates
                            if inventory_updates:
                                st.success("📦 **INVENTORY AUTOMATICALLY UPDATED!**")
                                for update in inventory_updates:
                                    st.info(f"✅ {update['product_name']}: Stock reduced by {update['quantity_deducted']} units (New stock: {update['current_stock']})")
                                    if update['low_stock_alert']:
                                        st.warning(f"⚠️ LOW STOCK ALERT: {update['product_name']} is running low!")
                            
                            # Show any inventory errors
                            if processing_errors:
                                for error in processing_errors:
                                    st.warning(error)
                            
                            # Enhanced Order Summary with all cart items
                            order_summary_html = f"""
                            <div style="
                                background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%);
                                padding: 25px;
                                border-radius: 15px;
                                border-left: 6px solid #4CAF50;
                                margin: 20px 0;
                                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                            ">
                                <h2 style="color: #2e7d32; margin: 0 0 20px 0; text-align: center;">🎉 ORDER CONFIRMATION 🎉</h2>
                                
                                <div style="background: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
                                    <h3 style="margin: 0 0 15px 0; color: #2c3e50;">🛍️ Ordered Items ({len(st.session_state.shopping_cart)} products)</h3>
                            """
                            
                            # Add each cart item to the summary
                            for item in st.session_state.shopping_cart:
                                product_info = get_product_info(item['name'])
                                category_info = get_all_categories().get(item['category'], {'color': '#95a5a6', 'icon': '📦'})
                                item_total = item['quantity'] * item['price']
                                
                                order_summary_html += f"""
                                <div style="display: flex; gap: 15px; align-items: center; padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin: 5px 0;">
                                    <img src="{item['image_url']}" 
                                         alt="{item['name']}" 
                                         style="width: 60px; height: 60px; object-fit: cover; border-radius: 6px; border: 2px solid {category_info['color']};">
                                    <div style="flex: 1;">
                                        <h5 style="margin: 0; color: #2c3e50;">{item['name']}</h5>
                                        <p style="margin: 2px 0; color: {category_info['color']}; font-size: 11px;">{category_info['icon']} {item['category']}</p>
                                        <p style="margin: 2px 0; color: #7f8c8d; font-size: 11px;">Brand: {item['brand']}</p>
                                    </div>
                                    <div style="text-align: right;">
                                        <div style="color: #3498db; font-weight: bold;">Qty: {item['quantity']}</div>
                                        <div style="color: #27ae60; font-weight: bold;">${item['price']:.2f}/unit</div>
                                        <div style="color: #e74c3c; font-weight: bold; font-size: 14px;">${item_total:.2f}</div>
                                    </div>
                                </div>
                                """
                            
                            order_summary_html += f"""
                                </div>
                                
                                <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">� Order Details</h4>
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
                                        <div><strong>👤 Customer:</strong> {customer_name}</div>
                                        <div><strong>📧 Email:</strong> {customer_email}</div>
                                        <div><strong>💳 Payment:</strong> {payment_method}</div>
                                        <div><strong>📅 Date:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                                    </div>
                                    <div style="margin-top: 10px;">
                                        <strong>📍 Delivery Address:</strong><br>
                                        <span style="color: #7f8c8d;">{delivery_address}</span>
                                    </div>
                                    {"<div style='margin-top: 10px;'><strong>�📝 Instructions:</strong><br><span style='color: #7f8c8d;'>" + special_instructions + "</span></div>" if special_instructions else ""}
                                </div>
                                
                                <div style="background: #2e7d32; color: white; padding: 15px; border-radius: 8px; text-align: center;">
                                    <h3 style="margin: 0;">💰 Total: ${cart_total * 1.085:.2f}</h3>
                                    <p style="margin: 5px 0; font-size: 12px;">Includes ${cart_total * 0.085:.2f} tax</p>
                                </div>
                            </div>
                            """
                            
                            st.markdown(order_summary_html, unsafe_allow_html=True)
                            
                            # Show integration status (same as before)
                            if isinstance(integration_status, dict):
                                st.success("🎉 **Complete System Integration Successful!**")
                                
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.info(f"📦 **Order Created**\n{'✅ Success' if integration_status.get('order_created') else '❌ Failed'}")
                                with col2:
                                    st.info(f"📊 **Inventory Updated**\n{'✅ Stock Deducted' if integration_status.get('inventory_updated') else '❌ Failed'}")
                                with col3:
                                    st.info(f"🚚 **Delivery Scheduled**\n{'✅ Driver Assigned' if integration_status.get('delivery_created') else '❌ Failed'}")
                                with col4:
                                    st.info(f"🏪 **Warehouse Dispatched**\n{'✅ Item Picked' if integration_status.get('warehouse_updated') else '❌ Failed'}")
                            
                            # Clear cart and reset forms
                            st.session_state.shopping_cart = []
                            st.session_state.show_checkout = False
                            st.session_state.show_add_order_form = False
                            
                            show_notification("Multi-item order created and all systems updated!", "success")
                            st.rerun()
                        else:
                            show_notification(f"Failed to create order: {integration_status}", "error")
                    else:
                        show_notification("❌ Missing required fields: Customer Name, Email, and Delivery Address are required.", "error")

        # Order form (for manual single-item orders - keeping for compatibility)
        if not st.session_state.get('show_checkout', False):
            st.markdown("---")
            st.markdown("### 📝 Single Item Order (Quick Order)")
            
            with st.form("single_order_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    customer_name = st.text_input("Customer Name", placeholder="Enter customer full name")
                    customer_email = st.text_input("Customer Email", placeholder="customer@example.com")
                    
                    # Enhanced product selection with categories
                    all_products = get_all_products()
                    product_names = list(all_products.keys())
                    
                    # Show selected product if any
                    if hasattr(st.session_state, 'selected_product'):
                        default_index = product_names.index(st.session_state.selected_product) + 1 if st.session_state.selected_product in product_names else 0
                    else:
                        default_index = 0
                
                product_name = st.selectbox(
                    "Select Product", 
                    [""] + product_names, 
                    index=default_index,
                    help="Choose from our categorized product catalog above"
                )
                
                # Show selected product preview with category
                if product_name:
                    selected_product_info = get_product_info(product_name)
                    category_info = categories.get(selected_product_info['category'], {'color': '#95a5a6', 'icon': '📦'})
                    
                    preview_html = f"""
                    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid {category_info['color']};">
                        <div style="display: flex; gap: 15px; align-items: center;">
                            <img src="{selected_product_info['image_url']}" 
                                 alt="{product_name}" 
                                 style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; border: 2px solid {category_info['color']};">
                            <div style="flex: 1;">
                                <h4 style="margin: 0; color: #2c3e50;">{product_name}</h4>
                                <p style="margin: 5px 0; color: {category_info['color']}; font-weight: bold;">
                                    {category_info['icon']} {selected_product_info['category']}
                                </p>
                                <p style="margin: 5px 0; color: #6c757d; font-size: 12px;">{selected_product_info['description']}</p>
                                <p style="margin: 5px 0; color: #27ae60; font-weight: bold;">Brand: {selected_product_info['brand']}</p>
                                <p style="margin: 5px 0; color: #fd7e14; font-weight: bold;">Price Range: {selected_product_info['price_range']}</p>
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(preview_html, unsafe_allow_html=True)
                
                with col2:
                    quantity = st.number_input("Quantity", min_value=1, value=1)
                    
                    # Use actual product price as default
                    from utils.products import get_product_actual_price
                    default_price = get_product_actual_price(product_name) if product_name else 10.00
                    price = st.number_input("Price ($)", min_value=0.01, value=default_price, step=0.01, help="Set the actual selling price")
                    payment_method = st.selectbox("Payment Method", ["Credit Card", "PayPal", "Cash on Delivery"])
                    
                    # Show order summary
                    if product_name and quantity > 0 and price > 0:
                        total_price = quantity * price
                        st.markdown(f"""
                        <div style="background: #e8f5e8; padding: 10px; border-radius: 8px; margin: 10px 0;">
                            <h5 style="margin: 0; color: #2e7d32;">💰 Order Summary</h5>
                            <p style="margin: 5px 0;"><strong>Product:</strong> {product_name}</p>
                            <p style="margin: 5px 0;"><strong>Quantity:</strong> {quantity} units</p>
                            <p style="margin: 5px 0;"><strong>Unit Price:</strong> ${price:.2f}</p>
                            <p style="margin: 5px 0; color: #2e7d32; font-weight: bold; font-size: 16px;"><strong>Total: ${total_price:.2f}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                
                delivery_address = st.text_area("Delivery Address", placeholder="Enter full delivery address")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit_button = st.form_submit_button("🛒 Create Order", use_container_width=True, type="primary")
                with col2:
                    cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if cancel_button:
                    st.session_state.show_add_order_form = False
                    st.rerun()
                
                if submit_button:
                    # Validate required fields
                    if customer_name and customer_email and product_name and delivery_address and quantity > 0 and price > 0:
                        # Show order processing animation
                        processing_placeholder = st.empty()
                        with processing_placeholder.container():
                            st.info("🔄 Processing your order...")
                            progress_bar = st.progress(0)
                            for i in range(100):
                                progress_bar.progress(i + 1)
                                time.sleep(0.01)
                        
                        # Update inventory first
                        inv_success, inv_result = update_inventory_on_order(product_name, quantity)
                        
                        # Clear processing animation
                        processing_placeholder.empty()
                        
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
                            # Calculate total price
                            total_price = quantity * price
                            
                            # Display spectacular order confirmation with effects
                            st.balloons()
                            st.success("🎉 **ORDER CONFIRMED SUCCESSFULLY!** 🎉")
                            
                            # Show inventory update result
                            if inv_success:
                                st.success("📦 **INVENTORY AUTOMATICALLY UPDATED!**")
                                st.info(f"✅ {inv_result['product_name']}: Stock reduced by {inv_result['quantity_deducted']} units")
                                st.info(f"📊 Previous Stock: {inv_result['previous_stock']} → Current Stock: {inv_result['current_stock']}")
                                if inv_result['low_stock_alert']:
                                    st.warning(f"⚠️ LOW STOCK ALERT: {product_name} is running low!")
                            else:
                                st.warning(f"⚠️ Inventory update failed: {inv_result}")
                            
                            # Enhanced Order Summary Card with Product Image
                            product_info = get_product_info(product_name)
                        
                        order_summary_html = f"""
                        <div style="
                            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c8 100%);
                            padding: 25px;
                            border-radius: 15px;
                            border-left: 6px solid #4CAF50;
                            margin: 20px 0;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                        ">
                            <h2 style="color: #2e7d32; margin: 0 0 20px 0; text-align: center;">🎉 ORDER CONFIRMATION 🎉</h2>
                            
                            <div style="display: flex; gap: 20px; align-items: center; background: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
                                <img src="{product_info['image_url']}" 
                                     alt="{product_name}" 
                                     style="width: 150px; height: 150px; object-fit: cover; border-radius: 12px; border: 3px solid #4CAF50;">
                                
                                <div style="flex: 1;">
                                    <h3 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 24px;">{product_name}</h3>
                                    <p style="margin: 5px 0; color: #7f8c8d; font-size: 14px;"><strong>Brand:</strong> {product_info['brand']}</p>
                                    <p style="margin: 5px 0; color: #34495e; font-size: 14px;">{product_info['description']}</p>
                                    
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                                        <div style="background: #3498db; color: white; padding: 8px 12px; border-radius: 8px; text-align: center;">
                                            <strong>Quantity: {quantity} units</strong>
                                        </div>
                                        <div style="background: #27ae60; color: white; padding: 8px 12px; border-radius: 8px; text-align: center;">
                                            <strong>Unit Price: ${price:.2f}</strong>
                                        </div>
                                    </div>
                                    
                                    <div style="background: #e74c3c; color: white; padding: 12px; border-radius: 8px; text-align: center; margin-top: 10px;">
                                        <strong style="font-size: 18px;">TOTAL: ${total_price:.2f}</strong>
                                    </div>
                                </div>
                            </div>
                            
                            <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                <h4 style="margin: 0 0 10px 0; color: #2c3e50;">📋 Order Details</h4>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
                                    <div><strong>👤 Customer:</strong> {customer_name}</div>
                                    <div><strong>📧 Email:</strong> {customer_email}</div>
                                    <div><strong>💳 Payment:</strong> {payment_method}</div>
                                    <div><strong>📅 Date:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                                </div>
                                <div style="margin-top: 10px;">
                                    <strong>📍 Delivery Address:</strong><br>
                                    <span style="color: #7f8c8d;">{delivery_address}</span>
                                </div>
                            </div>
                        </div>
                        """
                        
                        st.markdown(order_summary_html, unsafe_allow_html=True)
                        
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
                        
                        # Clear cart and reset forms
                        st.session_state.shopping_cart = []
                        st.session_state.show_checkout = False
                        st.session_state.show_add_order_form = False
                        
                        show_notification("Order created and all systems updated!", "success")
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
