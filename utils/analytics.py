"""
Advanced Analytics Module for Walmart Logistics Dashboard
Provides comprehensive data insights, trend analysis, and predictive analytics
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import timedelta
import streamlit as st

def generate_sample_analytics_data():
    """Generate comprehensive sample data for analytics"""
    
    # Generate 30 days of data
    dates = pd.date_range(start=datetime.date.today() - timedelta(days=30), 
                         end=datetime.date.today(), freq='D')
    
    # Orders data
    orders_data = []
    for date in dates:
        daily_orders = np.random.randint(20, 80)
        for i in range(daily_orders):
            orders_data.append({
                'date': date,
                'order_id': f"ORD{len(orders_data) + 1000}",
                'customer_type': np.random.choice(['Regular', 'Premium', 'VIP'], p=[0.7, 0.2, 0.1]),
                'category': np.random.choice(['Electronics', 'Grocery', 'Clothing', 'Home & Garden'], p=[0.3, 0.4, 0.2, 0.1]),
                'order_value': np.random.normal(150, 50),
                'quantity': np.random.randint(1, 5),
                'delivery_time': np.random.normal(24, 8),  # hours
                'satisfaction_score': np.random.normal(4.2, 0.8),
                'region': np.random.choice(['North', 'South', 'East', 'West', 'Central']),
                'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Cash on Delivery'], p=[0.5, 0.3, 0.2])
            })
    
    orders_df = pd.DataFrame(orders_data)
    orders_df['order_value'] = np.clip(orders_df['order_value'], 10, 500)
    orders_df['delivery_time'] = np.clip(orders_df['delivery_time'], 4, 72)
    orders_df['satisfaction_score'] = np.clip(orders_df['satisfaction_score'], 1, 5)
    
    # Inventory data
    inventory_data = []
    products = ['iPhone 15 Pro', 'MacBook Pro', 'Samsung Galaxy', 'iPad Pro', 'Dell XPS', 
               'Organic Bananas', 'Milk', 'Bread', 'Coffee', 'Eggs',
               'Winter Jacket', 'Sneakers', 'Jeans', 'T-Shirt', 'Dress']
    
    for product in products:
        for date in dates[-7:]:  # Last 7 days
            inventory_data.append({
                'date': date,
                'product': product,
                'stock_level': np.random.randint(10, 200),
                'turnover_rate': np.random.uniform(0.1, 0.8),
                'reorder_frequency': np.random.randint(1, 30),
                'storage_cost': np.random.uniform(0.5, 5.0),
                'category': 'Electronics' if 'iPhone' in product or 'MacBook' in product or 'Samsung' in product or 'iPad' in product or 'Dell' in product
                           else 'Grocery' if product in ['Organic Bananas', 'Milk', 'Bread', 'Coffee', 'Eggs']
                           else 'Clothing' if product in ['Winter Jacket', 'Sneakers', 'Jeans', 'T-Shirt', 'Dress']
                           else 'Other'
            })
    
    inventory_df = pd.DataFrame(inventory_data)
    
    # Delivery data
    delivery_data = []
    for date in dates:
        daily_deliveries = np.random.randint(15, 60)
        for i in range(daily_deliveries):
            delivery_data.append({
                'date': date,
                'delivery_id': f"DEL{len(delivery_data) + 1000}",
                'status': np.random.choice(['Delivered', 'In Transit', 'Delayed', 'Failed'], p=[0.8, 0.1, 0.08, 0.02]),
                'delivery_time_actual': np.random.normal(24, 6),
                'delivery_time_promised': 24,
                'distance': np.random.uniform(1, 50),
                'fuel_cost': np.random.uniform(2, 20),
                'driver': np.random.choice(['Driver A', 'Driver B', 'Driver C', 'Driver D', 'Driver E']),
                'vehicle_type': np.random.choice(['Van', 'Truck', 'Bike'], p=[0.6, 0.3, 0.1]),
                'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'])
            })
    
    delivery_df = pd.DataFrame(delivery_data)
    delivery_df['delivery_time_actual'] = np.clip(delivery_df['delivery_time_actual'], 2, 72)
    delivery_df['on_time'] = delivery_df['delivery_time_actual'] <= delivery_df['delivery_time_promised']
    
    return orders_df, inventory_df, delivery_df

def create_revenue_analysis(orders_df):
    """Create comprehensive revenue analysis"""
    
    # Daily revenue trend
    daily_revenue = orders_df.groupby('date')['order_value'].sum().reset_index()
    daily_revenue['moving_avg'] = daily_revenue['order_value'].rolling(window=7).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_revenue['date'], y=daily_revenue['order_value'],
                            mode='lines+markers', name='Daily Revenue',
                            line=dict(color='#1f77b4')))
    fig.add_trace(go.Scatter(x=daily_revenue['date'], y=daily_revenue['moving_avg'],
                            mode='lines', name='7-Day Moving Average',
                            line=dict(color='#ff7f0e', dash='dash')))
    
    fig.update_layout(title='Revenue Trend Analysis',
                     xaxis_title='Date',
                     yaxis_title='Revenue ($)',
                     height=400)
    
    return fig, daily_revenue

def create_customer_segmentation(orders_df):
    """Create customer segmentation analysis"""
    
    # Customer value segmentation
    customer_stats = orders_df.groupby('customer_type').agg({
        'order_value': ['mean', 'sum', 'count'],
        'satisfaction_score': 'mean'
    }).round(2)
    
    # Flatten column names
    customer_stats.columns = ['Avg_Order_Value', 'Total_Revenue', 'Order_Count', 'Avg_Satisfaction']
    customer_stats = customer_stats.reset_index()
    
    # Create pie chart for revenue distribution
    fig = px.pie(customer_stats, values='Total_Revenue', names='customer_type',
                title='Revenue Distribution by Customer Type',
                color_discrete_sequence=['#ff9999', '#66b3ff', '#99ff99'])
    
    return fig, customer_stats

def create_inventory_insights(inventory_df):
    """Create inventory performance insights"""
    
    # Inventory turnover analysis
    turnover_analysis = inventory_df.groupby('category').agg({
        'turnover_rate': 'mean',
        'stock_level': 'mean',
        'storage_cost': 'sum'
    }).round(2)
    
    # Stock level trends
    stock_trends = inventory_df.groupby(['date', 'category'])['stock_level'].mean().reset_index()
    
    fig = px.line(stock_trends, x='date', y='stock_level', color='category',
                 title='Stock Level Trends by Category')
    
    return fig, turnover_analysis

def create_delivery_performance(delivery_df):
    """Create delivery performance analytics"""
    
    # On-time delivery rate by region
    delivery_performance = delivery_df.groupby('region').agg({
        'on_time': 'mean',
        'delivery_time_actual': 'mean',
        'fuel_cost': 'mean'
    }).round(2)
    
    delivery_performance['on_time_percentage'] = delivery_performance['on_time'] * 100
    
    # Create performance chart
    fig = px.bar(delivery_performance.reset_index(), x='region', y='on_time_percentage',
                title='On-Time Delivery Performance by Region',
                color='on_time_percentage',
                color_continuous_scale='RdYlGn')
    
    return fig, delivery_performance

def create_predictive_insights(orders_df, inventory_df, delivery_df):
    """Create predictive insights and forecasts"""
    
    insights = []
    
    # Revenue forecast
    recent_revenue = orders_df.groupby('date')['order_value'].sum().tail(7).mean()
    prev_revenue = orders_df.groupby('date')['order_value'].sum().head(7).mean()
    revenue_growth = ((recent_revenue - prev_revenue) / prev_revenue) * 100
    
    if revenue_growth > 5:
        insights.append({
            'type': 'positive',
            'title': '📈 Revenue Growth Trend',
            'message': f'Revenue has grown by {revenue_growth:.1f}% compared to last week. Projected monthly increase: ${recent_revenue * 30:.0f}'
        })
    elif revenue_growth < -5:
        insights.append({
            'type': 'warning',
            'title': '⚠️ Revenue Decline Alert',
            'message': f'Revenue has declined by {abs(revenue_growth):.1f}%. Consider promotional campaigns to boost sales.'
        })
    
    # Inventory insights
    low_stock_products = inventory_df[inventory_df['stock_level'] < 50]['product'].unique()
    if len(low_stock_products) > 0:
        insights.append({
            'type': 'warning',
            'title': '📦 Low Stock Alert',
            'message': f'{len(low_stock_products)} products are running low on stock. Immediate reorder recommended for: {", ".join(low_stock_products[:3])}'
        })
    
    # High turnover products
    high_turnover = inventory_df[inventory_df['turnover_rate'] > 0.6]['product'].unique()
    if len(high_turnover) > 0:
        insights.append({
            'type': 'positive',
            'title': '🚀 High Demand Products',
            'message': f'Products with high turnover rates: {", ".join(high_turnover[:3])}. Consider increasing stock levels.'
        })
    
    # Delivery performance
    on_time_rate = delivery_df['on_time'].mean()
    if on_time_rate > 0.9:
        insights.append({
            'type': 'positive',
            'title': '✅ Excellent Delivery Performance',
            'message': f'On-time delivery rate is {on_time_rate*100:.1f}%. Customer satisfaction is likely high.'
        })
    elif on_time_rate < 0.8:
        insights.append({
            'type': 'warning',
            'title': '🚚 Delivery Performance Issue',
            'message': f'On-time delivery rate is {on_time_rate*100:.1f}%. Route optimization recommended.'
        })
    
    # Seasonal predictions
    current_month = datetime.datetime.now().month
    if current_month in [11, 12]:  # Holiday season
        insights.append({
            'type': 'info',
            'title': '🎄 Holiday Season Forecast',
            'message': 'Expect 30-40% increase in orders during holiday season. Stock up on popular categories.'
        })
    
    return insights

def create_kpi_dashboard(orders_df, inventory_df, delivery_df):
    """Create comprehensive KPI dashboard"""
    
    # Calculate KPIs
    total_revenue = orders_df['order_value'].sum()
    avg_order_value = orders_df['order_value'].mean()
    total_orders = len(orders_df)
    customer_satisfaction = orders_df['satisfaction_score'].mean()
    
    inventory_value = (inventory_df['stock_level'] * 50).sum()  # Assuming avg price $50
    low_stock_items = len(inventory_df[inventory_df['stock_level'] < 30])
    
    on_time_delivery = delivery_df['on_time'].mean() * 100
    avg_delivery_time = delivery_df['delivery_time_actual'].mean()
    
    return {
        'revenue': {
            'total': total_revenue,
            'avg_order': avg_order_value,
            'total_orders': total_orders,
            'satisfaction': customer_satisfaction
        },
        'inventory': {
            'total_value': inventory_value,
            'low_stock_count': low_stock_items,
            'total_products': len(inventory_df['product'].unique())
        },
        'delivery': {
            'on_time_rate': on_time_delivery,
            'avg_time': avg_delivery_time,
            'total_deliveries': len(delivery_df)
        }
    }

def create_advanced_analytics_dashboard():
    """Create the main analytics dashboard"""
    
    st.header("📊 Advanced Analytics & Business Insights")
    st.success("🧠 **AI-Powered Analytics**: Real-time insights, predictive forecasting, and performance optimization recommendations")
    
    # Generate sample data
    orders_df, inventory_df, delivery_df = generate_sample_analytics_data()
    
    # Calculate KPIs
    kpis = create_kpi_dashboard(orders_df, inventory_df, delivery_df)
    
    # KPI Overview
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Revenue", f"${kpis['revenue']['total']:,.0f}", 
                 delta=f"${kpis['revenue']['avg_order']:.0f} avg order")
    with col2:
        st.metric("📦 Inventory Value", f"${kpis['inventory']['total_value']:,.0f}",
                 delta=f"{kpis['inventory']['low_stock_count']} low stock")
    with col3:
        st.metric("🚚 On-Time Delivery", f"{kpis['delivery']['on_time_rate']:.1f}%",
                 delta=f"{kpis['delivery']['avg_time']:.1f}h avg time")
    with col4:
        st.metric("⭐ Customer Satisfaction", f"{kpis['revenue']['satisfaction']:.1f}/5",
                 delta=f"{kpis['revenue']['total_orders']} total orders")
    
    # Analytics Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Revenue Analytics", 
        "👥 Customer Insights", 
        "📦 Inventory Intelligence", 
        "🚚 Delivery Performance", 
        "🔮 Predictive Insights"
    ])
    
    with tab1:
        st.subheader("💰 Revenue Analytics Dashboard")
        
        # Revenue trend
        rev_fig, daily_revenue = create_revenue_analysis(orders_df)
        st.plotly_chart(rev_fig, use_container_width=True)
        
        # Revenue insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Revenue by Category")
            category_revenue = orders_df.groupby('category')['order_value'].sum().reset_index()
            fig = px.bar(category_revenue, x='category', y='order_value',
                        title='Revenue by Product Category',
                        color='order_value',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💳 Payment Method Analysis")
            payment_stats = orders_df.groupby('payment_method')['order_value'].sum().reset_index()
            fig = px.pie(payment_stats, values='order_value', names='payment_method',
                        title='Revenue by Payment Method')
            st.plotly_chart(fig, use_container_width=True)
        
        # Revenue insights box
        st.subheader("💡 Revenue Insights")
        total_revenue = orders_df['order_value'].sum()
        best_category = orders_df.groupby('category')['order_value'].sum().idxmax()
        best_day = daily_revenue.loc[daily_revenue['order_value'].idxmax(), 'date'].strftime('%B %d')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"🏆 **Best Category**: {best_category}")
        with col2:
            st.info(f"📅 **Best Sales Day**: {best_day}")
        with col3:
            growth_rate = ((daily_revenue['order_value'].tail(7).mean() / daily_revenue['order_value'].head(7).mean()) - 1) * 100
            st.info(f"📈 **Weekly Growth**: {growth_rate:.1f}%")
    
    with tab2:
        st.subheader("👥 Customer Insights & Segmentation")
        
        # Customer segmentation
        seg_fig, customer_stats = create_customer_segmentation(orders_df)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(seg_fig, use_container_width=True)
        
        with col2:
            st.subheader("📋 Customer Statistics")
            st.dataframe(customer_stats, use_container_width=True)
        
        # Regional analysis
        st.subheader("🗺️ Regional Performance")
        regional_stats = orders_df.groupby('region').agg({
            'order_value': ['sum', 'mean', 'count'],
            'satisfaction_score': 'mean'
        }).round(2)
        regional_stats.columns = ['Total_Revenue', 'Avg_Order_Value', 'Order_Count', 'Satisfaction']
        
        fig = px.scatter(regional_stats.reset_index(), x='Avg_Order_Value', y='Satisfaction',
                        size='Total_Revenue', color='region',
                        title='Regional Performance Matrix',
                        hover_data=['Order_Count'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer insights
        st.subheader("💡 Customer Insights")
        vip_revenue = orders_df[orders_df['customer_type'] == 'VIP']['order_value'].sum()
        vip_percentage = (vip_revenue / orders_df['order_value'].sum()) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"💎 **VIP Revenue**: {vip_percentage:.1f}% of total")
        with col2:
            best_region = regional_stats['Satisfaction'].idxmax()
            st.info(f"🏆 **Best Region**: {best_region}")
        with col3:
            avg_satisfaction = orders_df['satisfaction_score'].mean()
            st.info(f"⭐ **Avg Satisfaction**: {avg_satisfaction:.1f}/5")
    
    with tab3:
        st.subheader("📦 Inventory Intelligence")
        
        # Inventory trends
        inv_fig, turnover_analysis = create_inventory_insights(inventory_df)
        st.plotly_chart(inv_fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔄 Turnover Analysis")
            st.dataframe(turnover_analysis, use_container_width=True)
        
        with col2:
            st.subheader("💰 Storage Cost by Category")
            fig = px.bar(turnover_analysis.reset_index(), x='category', y='storage_cost',
                        title='Storage Costs by Category',
                        color='storage_cost',
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        # Inventory recommendations
        st.subheader("🎯 Inventory Recommendations")
        
        # Find products that need attention
        latest_inventory = inventory_df[inventory_df['date'] == inventory_df['date'].max()]
        low_stock = latest_inventory[latest_inventory['stock_level'] < 50]
        high_turnover = latest_inventory[latest_inventory['turnover_rate'] > 0.6]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if len(low_stock) > 0:
                st.warning(f"⚠️ **{len(low_stock)} products** need restocking")
                for product in low_stock['product'].head(3):
                    st.write(f"• {product}")
        
        with col2:
            if len(high_turnover) > 0:
                st.success(f"🚀 **{len(high_turnover)} high-demand** products")
                for product in high_turnover['product'].head(3):
                    st.write(f"• {product}")
        
        with col3:
            avg_turnover = latest_inventory['turnover_rate'].mean()
            if avg_turnover > 0.5:
                st.info("📈 **Overall turnover**: Healthy")
            else:
                st.warning("📉 **Overall turnover**: Needs improvement")
    
    with tab4:
        st.subheader("🚚 Delivery Performance Analytics")
        
        # Delivery performance
        del_fig, delivery_performance = create_delivery_performance(delivery_df)
        st.plotly_chart(del_fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Performance by Region")
            st.dataframe(delivery_performance, use_container_width=True)
        
        with col2:
            st.subheader("🚛 Driver Performance")
            driver_stats = delivery_df.groupby('driver').agg({
                'on_time': 'mean',
                'delivery_time_actual': 'mean',
                'fuel_cost': 'mean'
            }).round(2)
            driver_stats['on_time_percentage'] = driver_stats['on_time'] * 100
            st.dataframe(driver_stats, use_container_width=True)
        
        # Delivery trends
        st.subheader("📈 Delivery Time Trends")
        delivery_trends = delivery_df.groupby('date')['delivery_time_actual'].mean().reset_index()
        fig = px.line(delivery_trends, x='date', y='delivery_time_actual',
                     title='Average Delivery Time Over Time')
        fig.add_hline(y=24, line_dash="dash", line_color="red", 
                     annotation_text="Target: 24 hours")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader("🔮 Predictive Insights & Recommendations")
        
        # Generate insights
        insights = create_predictive_insights(orders_df, inventory_df, delivery_df)
        
        # Display insights
        for insight in insights:
            if insight['type'] == 'positive':
                st.success(f"**{insight['title']}**\n\n{insight['message']}")
            elif insight['type'] == 'warning':
                st.warning(f"**{insight['title']}**\n\n{insight['message']}")
            else:
                st.info(f"**{insight['title']}**\n\n{insight['message']}")
        
        # Future predictions
        st.subheader("📅 30-Day Forecast")
        
        # Simple forecasting based on trends
        recent_avg_daily_revenue = orders_df.groupby('date')['order_value'].sum().tail(7).mean()
        predicted_monthly_revenue = recent_avg_daily_revenue * 30
        
        recent_avg_orders = orders_df.groupby('date').size().tail(7).mean()
        predicted_monthly_orders = recent_avg_orders * 30
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📈 Predicted Revenue", f"${predicted_monthly_revenue:,.0f}",
                     delta="Based on recent trends")
        with col2:
            st.metric("📦 Predicted Orders", f"{predicted_monthly_orders:.0f}",
                     delta="30-day forecast")
        with col3:
            growth_rate = ((recent_avg_daily_revenue / orders_df.groupby('date')['order_value'].sum().head(7).mean()) - 1) * 100
            st.metric("📊 Growth Rate", f"{growth_rate:.1f}%",
                     delta="Week-over-week")
        
        # Action recommendations
        st.subheader("🎯 Recommended Actions")
        
        recommendations = [
            "🔄 **Inventory**: Restock high-turnover products before they run out",
            "🚚 **Delivery**: Optimize routes in regions with lower on-time rates",
            "💰 **Revenue**: Focus marketing on best-performing product categories",
            "👥 **Customers**: Implement loyalty programs for Premium customers",
            "📊 **Analytics**: Set up automated alerts for KPI thresholds"
        ]
        
        for rec in recommendations:
            st.write(rec)
    
    # Executive Summary
    st.markdown("---")
    st.subheader("📋 Executive Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🎯 Key Strengths:**")
        st.write("• Strong revenue growth trend")
        st.write("• High customer satisfaction scores") 
        st.write("• Efficient inventory turnover")
        st.write("• Reliable delivery performance")
    
    with col2:
        st.write("**⚠️ Areas for Improvement:**")
        st.write("• Reduce delivery delays in certain regions")
        st.write("• Optimize inventory levels for slow-moving items")
        st.write("• Increase VIP customer acquisition")
        st.write("• Improve payment method diversity")

def display_analytics_insights():
    """Display the analytics dashboard"""
    create_advanced_analytics_dashboard()
