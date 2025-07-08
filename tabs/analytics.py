import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
from utils.api import get_data
from utils.helpers import show_notification

def app():
    st.header("📊 Advanced Analytics Dashboard")
    st.markdown("**Deep insights and predictive analytics for business optimization**")
    
    # Main tabs for different analytics categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Predictive Analytics", 
        "📈 Performance Metrics", 
        "🎯 AI Insights", 
        "📊 Custom Reports",
        "🔄 Real-time Monitoring"
    ])
    
    with tab1:
        display_predictive_analytics()
    
    with tab2:
        display_performance_metrics()
    
    with tab3:
        display_ai_insights()
    
    with tab4:
        display_custom_reports()
    
    with tab5:
        display_realtime_monitoring()

def display_predictive_analytics():
    st.subheader("🔮 Predictive Analytics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Demand Forecasting
        st.markdown("### 📈 Demand Forecasting")
        
        # Generate mock forecasting data
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        products = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
        
        forecast_data = []
        for product in products:
            base_demand = np.random.randint(100, 500)
            trend = np.random.uniform(-0.02, 0.05)
            seasonal = np.sin(np.arange(30) * 2 * np.pi / 7) * 20
            noise = np.random.normal(0, 10, 30)
            
            for i, date in enumerate(dates):
                demand = base_demand * (1 + trend * i) + seasonal[i] + noise[i]
                forecast_data.append({
                    'Date': date,
                    'Product': product,
                    'Forecasted_Demand': max(0, int(demand)),
                    'Confidence_Lower': max(0, int(demand * 0.85)),
                    'Confidence_Upper': int(demand * 1.15)
                })
        
        forecast_df = pd.DataFrame(forecast_data)
        
        # Interactive forecast chart
        selected_product = st.selectbox("Select Product Category", products)
        product_data = forecast_df[forecast_df['Product'] == selected_product]
        
        fig = go.Figure()
        
        # Add forecast line
        fig.add_trace(go.Scatter(
            x=product_data['Date'],
            y=product_data['Forecasted_Demand'],
            mode='lines+markers',
            name='Forecasted Demand',
            line=dict(color='blue', width=2)
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=product_data['Date'],
            y=product_data['Confidence_Upper'],
            fill=None,
            mode='lines',
            line_color='rgba(0,0,0,0)',
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=product_data['Date'],
            y=product_data['Confidence_Lower'],
            fill='tonexty',
            mode='lines',
            line_color='rgba(0,0,0,0)',
            name='Confidence Interval',
            fillcolor='rgba(0,100,80,0.2)'
        ))
        
        fig.update_layout(
            title=f"30-Day Demand Forecast for {selected_product}",
            xaxis_title="Date",
            yaxis_title="Demand Units",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Inventory Optimization Predictions
        st.markdown("### 📦 Inventory Optimization")
        
        # Stock level predictions
        stock_data = pd.DataFrame({
            'Product': products,
            'Current_Stock': np.random.randint(50, 500, 5),
            'Predicted_Demand_7d': np.random.randint(100, 300, 5),
            'Reorder_Point': np.random.randint(30, 100, 5),
            'Optimal_Order_Qty': np.random.randint(200, 600, 5),
            'Stockout_Risk': np.random.uniform(0.05, 0.25, 5)
        })
        
        stock_data['Days_Until_Stockout'] = stock_data['Current_Stock'] / (stock_data['Predicted_Demand_7d'] / 7)
        stock_data['Reorder_Needed'] = stock_data['Current_Stock'] <= stock_data['Reorder_Point']
        
        # Color code based on urgency
        def get_urgency_color(days):
            if days <= 3:
                return "🔴 Critical"
            elif days <= 7:
                return "🟡 Warning"
            else:
                return "🟢 Good"
        
        stock_data['Urgency'] = stock_data['Days_Until_Stockout'].apply(get_urgency_color)
        
        st.dataframe(stock_data, use_container_width=True)
        
    with col2:
        # Key Predictions Summary
        st.markdown("### 🎯 Key Predictions")
        
        # Revenue forecast
        revenue_forecast = np.random.uniform(250000, 350000)
        st.metric(
            "7-Day Revenue Forecast",
            f"${revenue_forecast:,.0f}",
            delta=f"{np.random.uniform(5, 15):.1f}%"
        )
        
        # Order volume forecast
        order_forecast = np.random.randint(800, 1200)
        st.metric(
            "Expected Orders",
            f"{order_forecast:,}",
            delta=f"{np.random.uniform(3, 12):.1f}%"
        )
        
        # Capacity utilization
        capacity_forecast = np.random.uniform(75, 95)
        st.metric(
            "Warehouse Capacity",
            f"{capacity_forecast:.1f}%",
            delta=f"{np.random.uniform(-2, 8):.1f}%"
        )
        
        # Risk alerts
        st.markdown("### ⚠️ Risk Alerts")
        
        risk_alerts = [
            {"level": "High", "message": "Electronics demand spike expected", "color": "red"},
            {"level": "Medium", "message": "Delivery delays possible due to weather", "color": "orange"},
            {"level": "Low", "message": "Seasonal inventory adjustment needed", "color": "yellow"}
        ]
        
        for alert in risk_alerts:
            st.markdown(f"""
            <div style="padding: 10px; border-left: 4px solid {alert['color']}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{alert['level']} Risk:</strong><br>
                {alert['message']}
            </div>
            """, unsafe_allow_html=True)
        
        # ML Model Performance
        st.markdown("### 🤖 Model Performance")
        
        accuracy_metrics = {
            "Demand Forecast": 87.3,
            "Inventory Optimization": 92.1,
            "Delivery Time": 85.7,
            "Cost Prediction": 89.4
        }
        
        for model, accuracy in accuracy_metrics.items():
            st.metric(model, f"{accuracy}%", delta=f"{np.random.uniform(0.5, 2.5):.1f}%")

def display_performance_metrics():
    st.subheader("📊 Performance Metrics")
    
    # KPI Dashboard
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Order Fulfillment Rate", "98.7%", delta="1.2%")
        st.metric("Customer Satisfaction", "4.6/5.0", delta="0.3")
        
    with col2:
        st.metric("On-Time Delivery", "94.2%", delta="2.1%")
        st.metric("Inventory Turnover", "12.3x", delta="0.8x")
        
    with col3:
        st.metric("Cost per Order", "$18.45", delta="-$1.23")
        st.metric("Warehouse Efficiency", "87.9%", delta="3.4%")
        
    with col4:
        st.metric("Return Rate", "2.1%", delta="-0.3%")
        st.metric("Staff Productivity", "91.5%", delta="2.8%")
    
    # Performance Trends
    st.markdown("### 📈 Performance Trends")
    
    # Generate performance data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
    performance_data = pd.DataFrame({
        'Date': dates,
        'Orders_Processed': np.random.randint(80, 120, 30),
        'Fulfillment_Rate': np.random.uniform(95, 99, 30),
        'Customer_Satisfaction': np.random.uniform(4.2, 4.8, 30),
        'Delivery_Time': np.random.uniform(18, 26, 30),
        'Cost_Efficiency': np.random.uniform(85, 95, 30)
    })
    
    # Create performance dashboard
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Orders Processed', 'Fulfillment Rate', 'Customer Satisfaction', 'Delivery Time'),
        specs=[[{'secondary_y': False}, {'secondary_y': False}],
               [{'secondary_y': False}, {'secondary_y': False}]]
    )
    
    # Orders processed
    fig.add_trace(
        go.Scatter(x=performance_data['Date'], y=performance_data['Orders_Processed'], 
                  name='Orders', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Fulfillment rate
    fig.add_trace(
        go.Scatter(x=performance_data['Date'], y=performance_data['Fulfillment_Rate'], 
                  name='Fulfillment %', line=dict(color='green')),
        row=1, col=2
    )
    
    # Customer satisfaction
    fig.add_trace(
        go.Scatter(x=performance_data['Date'], y=performance_data['Customer_Satisfaction'], 
                  name='Satisfaction', line=dict(color='orange')),
        row=2, col=1
    )
    
    # Delivery time
    fig.add_trace(
        go.Scatter(x=performance_data['Date'], y=performance_data['Delivery_Time'], 
                  name='Delivery Time', line=dict(color='red')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Benchmarking
    st.markdown("### 🎯 Industry Benchmarking")
    
    benchmark_data = pd.DataFrame({
        'Metric': ['Order Fulfillment', 'Delivery Time', 'Customer Satisfaction', 'Cost Efficiency'],
        'Our_Performance': [98.7, 22.3, 4.6, 87.9],
        'Industry_Average': [95.2, 26.1, 4.2, 82.4],
        'Best_in_Class': [99.5, 18.7, 4.8, 94.2]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Our Performance',
        x=benchmark_data['Metric'],
        y=benchmark_data['Our_Performance'],
        marker_color='steelblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Industry Average',
        x=benchmark_data['Metric'],
        y=benchmark_data['Industry_Average'],
        marker_color='lightcoral'
    ))
    
    fig.add_trace(go.Bar(
        name='Best in Class',
        x=benchmark_data['Metric'],
        y=benchmark_data['Best_in_Class'],
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        title="Performance vs Industry Benchmarks",
        xaxis_title="Metrics",
        yaxis_title="Performance Score",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_ai_insights():
    st.subheader("🤖 AI-Powered Insights")
    
    # AI Recommendations
    st.markdown("### 💡 AI Recommendations")
    
    recommendations = [
        {
            "category": "Inventory Optimization",
            "insight": "Increase Electronics inventory by 15% for holiday season",
            "impact": "Potential 8% revenue increase",
            "confidence": 92,
            "action": "Adjust procurement for Q4"
        },
        {
            "category": "Delivery Optimization",
            "insight": "Consolidate shipments to Zone 5 for 12% cost reduction",
            "impact": "Save $2,400/month in shipping costs",
            "confidence": 87,
            "action": "Implement route consolidation"
        },
        {
            "category": "Staff Scheduling",
            "insight": "Peak orders occur 2-4 PM, optimize staff allocation",
            "impact": "Reduce overtime by 23%",
            "confidence": 94,
            "action": "Adjust shift schedules"
        },
        {
            "category": "Customer Behavior",
            "insight": "Customers in suburbs prefer weekend deliveries",
            "impact": "Improve satisfaction by 0.3 points",
            "confidence": 89,
            "action": "Offer weekend delivery options"
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"💡 {rec['category']} - Confidence: {rec['confidence']}%"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Insight:** {rec['insight']}")
                st.markdown(f"**Impact:** {rec['impact']}")
                st.markdown(f"**Recommended Action:** {rec['action']}")
            
            with col2:
                # Confidence gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = rec['confidence'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Confidence"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig.update_layout(height=200)
                st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly Detection
    st.markdown("### 🔍 Anomaly Detection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate anomaly data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        normal_data = np.random.normal(100, 15, 30)
        # Add some anomalies
        anomaly_indices = [7, 15, 23]
        for idx in anomaly_indices:
            normal_data[idx] = np.random.choice([150, 50])  # Spike or drop
        
        anomaly_data = pd.DataFrame({
            'Date': dates,
            'Order_Volume': normal_data,
            'Is_Anomaly': [i in anomaly_indices for i in range(30)]
        })
        
        fig = go.Figure()
        
        # Normal data
        normal_points = anomaly_data[~anomaly_data['Is_Anomaly']]
        fig.add_trace(go.Scatter(
            x=normal_points['Date'],
            y=normal_points['Order_Volume'],
            mode='lines+markers',
            name='Normal Orders',
            line=dict(color='blue'),
            marker=dict(size=6)
        ))
        
        # Anomalies
        anomaly_points = anomaly_data[anomaly_data['Is_Anomaly']]
        fig.add_trace(go.Scatter(
            x=anomaly_points['Date'],
            y=anomaly_points['Order_Volume'],
            mode='markers',
            name='Anomalies',
            marker=dict(color='red', size=12, symbol='diamond')
        ))
        
        fig.update_layout(
            title="Order Volume Anomaly Detection",
            xaxis_title="Date",
            yaxis_title="Order Volume"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Detected Anomalies:**")
        
        anomaly_descriptions = [
            "📈 Order spike on Nov 15 - Black Friday prep",
            "📉 Order drop on Nov 23 - Holiday closure",
            "⚠️ Unusual pattern on Dec 1 - System issue"
        ]
        
        for desc in anomaly_descriptions:
            st.markdown(f"• {desc}")
        
        st.markdown("**Auto-Actions Taken:**")
        st.markdown("• ✅ Scaled up warehouse staff")
        st.markdown("• ✅ Notified management team")
        st.markdown("• ✅ Adjusted inventory levels")
    
    # Predictive Models Performance
    st.markdown("### 📊 Model Performance Dashboard")
    
    model_metrics = pd.DataFrame({
        'Model': ['Demand Forecasting', 'Price Optimization', 'Inventory Management', 'Delivery Routing'],
        'Accuracy': [87.3, 92.1, 89.7, 94.2],
        'Precision': [86.1, 91.5, 88.9, 93.8],
        'Recall': [88.7, 92.8, 90.2, 94.5],
        'F1_Score': [87.4, 92.1, 89.5, 94.1]
    })
    
    fig = go.Figure()
    
    for metric in ['Accuracy', 'Precision', 'Recall', 'F1_Score']:
        fig.add_trace(go.Bar(
            name=metric,
            x=model_metrics['Model'],
            y=model_metrics[metric],
            text=model_metrics[metric],
            textposition='auto',
        ))
    
    fig.update_layout(
        title="ML Model Performance Metrics",
        xaxis_title="Models",
        yaxis_title="Score (%)",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_custom_reports():
    st.subheader("📋 Custom Reports")
    
    # Report Builder
    st.markdown("### 🛠️ Report Builder")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Report Configuration**")
        
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Operational Report", "Financial Analysis", "Performance Review"]
        )
        
        date_range = st.date_input(
            "Date Range",
            value=[datetime.now() - timedelta(days=30), datetime.now()],
            max_value=datetime.now()
        )
        
        metrics = st.multiselect(
            "Select Metrics",
            ["Orders", "Revenue", "Delivery Performance", "Inventory Levels", "Cost Analysis", "Customer Satisfaction"],
            default=["Orders", "Revenue", "Delivery Performance"]
        )
        
        export_format = st.selectbox(
            "Export Format",
            ["PDF", "Excel", "CSV", "PowerPoint"]
        )
        
        if st.button("Generate Report", type="primary"):
            with st.spinner("Generating report..."):
                # Simulate report generation
                import time
                time.sleep(2)
                
                st.success("Report generated successfully!")
                
                # Create download buttons
                st.download_button(
                    label=f"Download {report_type} ({export_format})",
                    data=f"Mock {report_type} data in {export_format} format",
                    file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{export_format.lower()}",
                    mime="text/plain"
                )
    
    with col2:
        # Report Preview
        st.markdown("**Report Preview**")
        
        if report_type == "Executive Summary":
            st.markdown("### 📊 Executive Summary")
            
            summary_data = {
                "Total Orders": "1,247",
                "Revenue": "$184,320",
                "Growth Rate": "+12.5%",
                "Customer Satisfaction": "4.6/5.0",
                "Key Insights": [
                    "Electronics category showing 18% growth",
                    "Delivery performance improved by 3.2%",
                    "Inventory turnover increased to 12.3x"
                ]
            }
            
            for key, value in summary_data.items():
                if key == "Key Insights":
                    st.markdown(f"**{key}:**")
                    for insight in value:
                        st.markdown(f"• {insight}")
                else:
                    st.markdown(f"**{key}:** {value}")
        
        elif report_type == "Operational Report":
            st.markdown("### ⚙️ Operational Report")
            
            # Sample operational metrics
            operational_data = pd.DataFrame({
                'Department': ['Warehouse', 'Delivery', 'Customer Service', 'IT'],
                'Efficiency': [87.3, 92.1, 89.7, 94.2],
                'Issues': [2, 1, 0, 1],
                'Status': ['Good', 'Excellent', 'Excellent', 'Good']
            })
            
            st.dataframe(operational_data, use_container_width=True)
        
        elif report_type == "Financial Analysis":
            st.markdown("### 💰 Financial Analysis")
            
            # Sample financial data
            financial_data = {
                "Revenue": "$184,320",
                "Costs": "$127,840",
                "Profit": "$56,480",
                "Margin": "30.7%",
                "ROI": "23.4%"
            }
            
            for key, value in financial_data.items():
                st.markdown(f"**{key}:** {value}")
        
        else:  # Performance Review
            st.markdown("### 📈 Performance Review")
            
            # Sample performance data
            performance_data = pd.DataFrame({
                'KPI': ['Order Fulfillment', 'Customer Satisfaction', 'Delivery Time', 'Cost Efficiency'],
                'Current': [98.7, 4.6, 22.3, 87.9],
                'Target': [99.0, 4.8, 20.0, 90.0],
                'Status': ['On Track', 'On Track', 'Needs Improvement', 'On Track']
            })
            
            st.dataframe(performance_data, use_container_width=True)
    
    # Scheduled Reports
    st.markdown("### 📅 Scheduled Reports")
    
    scheduled_reports = pd.DataFrame({
        'Report Name': ['Daily Operations', 'Weekly Performance', 'Monthly Financial', 'Quarterly Review'],
        'Frequency': ['Daily', 'Weekly', 'Monthly', 'Quarterly'],
        'Recipients': ['Operations Team', 'Management', 'Finance Team', 'Executive Team'],
        'Next Run': ['Today 9:00 AM', 'Monday 8:00 AM', 'Dec 1st 6:00 AM', 'Jan 1st 6:00 AM'],
        'Status': ['Active', 'Active', 'Active', 'Active']
    })
    
    st.dataframe(scheduled_reports, use_container_width=True)
    
    # Quick Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate Dashboard Report"):
            st.info("Dashboard report generation started...")
    
    with col2:
        if st.button("📈 Export Analytics Data"):
            st.info("Analytics data export started...")
    
    with col3:
        if st.button("📧 Email Report"):
            st.info("Report emailed to stakeholders...")

def display_realtime_monitoring():
    st.subheader("🔄 Real-time Monitoring")
    
    # System Status
    st.markdown("### 🖥️ System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**API Services**")
        api_status = ["🟢 Orders API", "🟢 Inventory API", "🟢 Delivery API", "🟡 Analytics API"]
        for status in api_status:
            st.markdown(status)
    
    with col2:
        st.markdown("**Database Status**")
        db_status = ["🟢 Primary DB", "🟢 Replica DB", "🟢 Cache Layer", "🟢 Search Index"]
        for status in db_status:
            st.markdown(status)
    
    with col3:
        st.markdown("**External Services**")
        ext_status = ["🟢 Payment Gateway", "🟢 Shipping APIs", "🟡 Maps Service", "🟢 Email Service"]
        for status in ext_status:
            st.markdown(status)
    
    with col4:
        st.markdown("**Performance Metrics**")
        st.metric("Response Time", "145ms", delta="-12ms")
        st.metric("Uptime", "99.97%", delta="0.02%")
        st.metric("Error Rate", "0.03%", delta="-0.01%")
    
    # Live Activity Feed
    st.markdown("### 📱 Live Activity Feed")
    
    # Simulate real-time activities
    activities = [
        {"time": "2 min ago", "event": "New order placed", "details": "Order #12345 - $89.99", "status": "✅"},
        {"time": "3 min ago", "event": "Delivery completed", "details": "Order #12340 delivered to customer", "status": "🚚"},
        {"time": "5 min ago", "event": "Inventory alert", "details": "Low stock: iPhone 13 Pro", "status": "⚠️"},
        {"time": "7 min ago", "event": "System optimization", "details": "Route optimization completed", "status": "🔧"},
        {"time": "9 min ago", "event": "Customer support", "details": "Issue resolved for customer #789", "status": "💬"},
        {"time": "12 min ago", "event": "Payment processed", "details": "Payment #PAY-456 processed", "status": "💳"}
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div style="padding: 10px; border-left: 4px solid #0071ce; background-color: #f8f9fa; margin: 5px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{activity['event']}</strong><br>
                    <small>{activity['details']}</small>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5em;">{activity['status']}</div>
                    <small>{activity['time']}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Alert Configuration
    st.markdown("### 🔔 Alert Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Alert Types**")
        
        alert_types = [
            "Inventory Low Stock",
            "Order Volume Spike",
            "Delivery Delays",
            "System Performance",
            "Customer Complaints",
            "Payment Issues"
        ]
        
        for alert_type in alert_types:
            enabled = st.checkbox(alert_type, value=True)
    
    with col2:
        st.markdown("**Notification Settings**")
        
        notification_methods = st.multiselect(
            "Notification Methods",
            ["Email", "SMS", "In-App", "Slack", "Teams"],
            default=["Email", "In-App"]
        )
        
        urgency_levels = st.multiselect(
            "Alert Urgency Levels",
            ["Low", "Medium", "High", "Critical"],
            default=["High", "Critical"]
        )
        
        if st.button("Save Alert Settings"):
            st.success("Alert settings saved successfully!")
    
    # Performance Monitoring
    st.markdown("### 📊 Performance Monitoring")
    
    # Real-time metrics
    dates = pd.date_range(start=datetime.now() - timedelta(hours=1), periods=60, freq='min')
    
    # Generate real-time performance data
    performance_data = pd.DataFrame({
        'Time': dates,
        'CPU_Usage': np.random.uniform(20, 80, 60),
        'Memory_Usage': np.random.uniform(30, 70, 60),
        'Response_Time': np.random.uniform(50, 200, 60),
        'Active_Users': np.random.randint(15, 45, 60)
    })
    
    # Create real-time charts
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('CPU Usage (%)', 'Memory Usage (%)', 'Response Time (ms)', 'Active Users'),
        specs=[[{'secondary_y': False}, {'secondary_y': False}],
               [{'secondary_y': False}, {'secondary_y': False}]]
    )
    
    # CPU Usage
    fig.add_trace(
        go.Scatter(x=performance_data['Time'], y=performance_data['CPU_Usage'], 
                  name='CPU', line=dict(color='red')),
        row=1, col=1
    )
    
    # Memory Usage
    fig.add_trace(
        go.Scatter(x=performance_data['Time'], y=performance_data['Memory_Usage'], 
                  name='Memory', line=dict(color='blue')),
        row=1, col=2
    )
    
    # Response Time
    fig.add_trace(
        go.Scatter(x=performance_data['Time'], y=performance_data['Response_Time'], 
                  name='Response Time', line=dict(color='green')),
        row=2, col=1
    )
    
    # Active Users
    fig.add_trace(
        go.Scatter(x=performance_data['Time'], y=performance_data['Active_Users'], 
                  name='Users', line=dict(color='purple')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Auto-refresh toggle
    if st.checkbox("Auto-refresh (30 seconds)"):
        st.rerun()
