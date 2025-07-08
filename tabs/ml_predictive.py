import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def app():
    """Machine Learning & Predictive Analytics Dashboard"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; text-align: center;">🤖 Machine Learning & Predictive Analytics</h1>
        <p style="margin: 10px 0 0 0; text-align: center; font-size: 16px;">
            Demand forecasting • Inventory optimization • Smart recommendations • Predictive maintenance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for ML configuration
    with st.sidebar:
        st.header("🤖 ML Configuration")
        
        # Model selection
        model_type = st.selectbox(
            "Select Model Type",
            ["Demand Forecasting", "Inventory Optimization", "Price Prediction", "Customer Behavior", "Maintenance Prediction"]
        )
        
        # Time horizon
        time_horizon = st.slider("Prediction Horizon (days)", 1, 90, 30)
        
        # Model parameters
        st.subheader("Model Parameters")
        confidence_level = st.slider("Confidence Level (%)", 80, 99, 95)
        update_frequency = st.selectbox("Update Frequency", ["Real-time", "Hourly", "Daily", "Weekly"])
        
        # Training settings
        st.subheader("Training Settings")
        auto_retrain = st.checkbox("Auto Retrain", value=True)
        feature_importance = st.checkbox("Show Feature Importance", value=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 ML Dashboard", "📈 Demand Forecasting", "🎯 Recommendations", "🔧 Model Training", "📋 Performance"])
    
    with tab1:
        display_ml_dashboard()
    
    with tab2:
        display_demand_forecasting(time_horizon, confidence_level)
    
    with tab3:
        display_recommendations()
    
    with tab4:
        display_model_training(feature_importance)
    
    with tab5:
        display_model_performance()

def display_ml_dashboard():
    """Display ML dashboard with key metrics"""
    st.header("🤖 Machine Learning Dashboard")
    
    # Key ML metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        model_accuracy = random.uniform(85, 95)
        st.metric("🎯 Model Accuracy", f"{model_accuracy:.1f}%", "↑ 2.3%")
    
    with col2:
        predictions_made = random.randint(1000, 5000)
        st.metric("📊 Predictions Today", f"{predictions_made:,}", "↑ 15%")
    
    with col3:
        cost_savings = random.randint(50000, 150000)
        st.metric("💰 Cost Savings", f"${cost_savings:,}", "↑ $25K")
    
    with col4:
        active_models = random.randint(8, 15)
        st.metric("🔄 Active Models", active_models, "↑ 2")
    
    with col5:
        data_quality = random.uniform(90, 100)
        st.metric("📋 Data Quality", f"{data_quality:.1f}%", "↑ 1.2%")
    
    # Model performance overview
    st.subheader("📈 Model Performance Overview")
    
    # Create sample model performance data
    models = ['Demand Forecasting', 'Inventory Optimization', 'Price Prediction', 'Customer Behavior', 'Maintenance Prediction']
    performance_data = []
    
    for model in models:
        performance_data.append({
            'Model': model,
            'Accuracy': random.uniform(80, 95),
            'Precision': random.uniform(75, 90),
            'Recall': random.uniform(70, 85),
            'F1-Score': random.uniform(72, 88),
            'Last Updated': datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 48))
        })
    
    df_performance = pd.DataFrame(performance_data)
    
    # Performance metrics chart
    fig_performance = px.bar(df_performance, x='Model', y=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                            title="Model Performance Metrics", barmode='group')
    st.plotly_chart(fig_performance, use_container_width=True)
    
    # Recent predictions
    st.subheader("🔮 Recent Predictions")
    
    predictions = [
        {"Time": "5 min ago", "Model": "Demand Forecasting", "Prediction": "High demand expected for Electronics next week", "Confidence": "92%"},
        {"Time": "12 min ago", "Model": "Inventory Optimization", "Prediction": "Restock SKU-12345 by Friday", "Confidence": "88%"},
        {"Time": "25 min ago", "Model": "Price Prediction", "Prediction": "Price increase recommended for Category A", "Confidence": "85%"},
        {"Time": "1 hour ago", "Model": "Customer Behavior", "Prediction": "Increased mobile shopping this weekend", "Confidence": "90%"},
        {"Time": "2 hours ago", "Model": "Maintenance Prediction", "Prediction": "Conveyor belt maintenance needed in 3 days", "Confidence": "94%"}
    ]
    
    for pred in predictions:
        with st.expander(f"{pred['Model']} - {pred['Prediction']}"):
            st.write(f"**Time:** {pred['Time']}")
            st.write(f"**Confidence:** {pred['Confidence']}")
            st.write(f"**Status:** Active")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"👍 Accept", key=f"accept_{pred['Time']}"):
                    st.success("Prediction accepted and action scheduled")
            with col2:
                if st.button(f"👎 Reject", key=f"reject_{pred['Time']}"):
                    st.info("Prediction rejected. Model will be retrained.")
    
    # ML insights
    st.subheader("💡 ML Insights")
    
    insights = [
        "🚀 Demand forecasting model shows 15% improvement in accuracy this month",
        "📊 Customer behavior patterns indicate shift towards mobile purchases",
        "💰 Price optimization model generated $50K savings this quarter",
        "🔧 Predictive maintenance prevented 3 major equipment failures",
        "📈 Inventory optimization reduced stockouts by 25%"
    ]
    
    for insight in insights:
        st.info(insight)

def display_demand_forecasting(time_horizon, confidence_level):
    """Display demand forecasting dashboard"""
    st.header("📈 Demand Forecasting")
    
    # Generate historical demand data
    dates = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=365), 
                         end=datetime.datetime.now(), freq='D')
    
    # Categories for forecasting
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys']
    
    # Historical demand
    st.subheader("📊 Historical Demand Patterns")
    
    historical_data = []
    for date in dates:
        for category in categories:
            # Add seasonality and trends
            base_demand = 100 + 20 * np.sin(date.dayofyear / 365 * 2 * np.pi)
            weekend_boost = 30 if date.weekday() >= 5 else 0
            random_variation = random.uniform(-20, 20)
            demand = max(0, base_demand + weekend_boost + random_variation)
            
            historical_data.append({
                'Date': date,
                'Category': category,
                'Demand': demand
            })
    
    df_historical = pd.DataFrame(historical_data)
    
    # Category selection
    selected_categories = st.multiselect(
        "Select Categories for Forecasting",
        categories,
        default=categories[:3]
    )
    
    if selected_categories:
        # Filter data for selected categories
        filtered_data = df_historical[df_historical['Category'].isin(selected_categories)]
        
        # Historical trend
        fig_historical = px.line(filtered_data, x='Date', y='Demand', color='Category',
                               title=f"Historical Demand Trends (Last 365 Days)")
        st.plotly_chart(fig_historical, use_container_width=True)
        
        # Forecast
        st.subheader("🔮 Demand Forecast")
        
        # Generate future dates
        future_dates = pd.date_range(start=datetime.datetime.now() + datetime.timedelta(days=1),
                                   periods=time_horizon, freq='D')
        
        # Simple forecast simulation
        forecast_data = []
        for date in future_dates:
            for category in selected_categories:
                # Simple trend + seasonality forecast
                base_forecast = 100 + 20 * np.sin(date.dayofyear / 365 * 2 * np.pi)
                weekend_boost = 30 if date.weekday() >= 5 else 0
                trend_factor = 1.02 ** ((date - datetime.datetime.now()).days / 30)  # 2% monthly growth
                
                forecast = base_forecast * trend_factor + weekend_boost
                
                # Add confidence intervals
                lower_bound = forecast * (1 - (100 - confidence_level) / 100)
                upper_bound = forecast * (1 + (100 - confidence_level) / 100)
                
                forecast_data.append({
                    'Date': date,
                    'Category': category,
                    'Forecast': forecast,
                    'Lower_Bound': lower_bound,
                    'Upper_Bound': upper_bound
                })
        
        df_forecast = pd.DataFrame(forecast_data)
        
        # Forecast visualization
        fig_forecast = go.Figure()
        
        for category in selected_categories:
            cat_data = df_forecast[df_forecast['Category'] == category]
            
            # Add forecast line
            fig_forecast.add_trace(go.Scatter(
                x=cat_data['Date'],
                y=cat_data['Forecast'],
                mode='lines',
                name=f'{category} Forecast',
                line=dict(width=3)
            ))
            
            # Add confidence interval
            fig_forecast.add_trace(go.Scatter(
                x=cat_data['Date'].tolist() + cat_data['Date'].tolist()[::-1],
                y=cat_data['Upper_Bound'].tolist() + cat_data['Lower_Bound'].tolist()[::-1],
                fill='tonexty',
                fillcolor='rgba(0,100,80,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name=f'{category} Confidence Interval',
                showlegend=False
            ))
        
        fig_forecast.update_layout(
            title=f"Demand Forecast - Next {time_horizon} Days ({confidence_level}% Confidence)",
            xaxis_title="Date",
            yaxis_title="Demand",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Forecast summary
        st.subheader("📋 Forecast Summary")
        
        summary_data = []
        for category in selected_categories:
            cat_forecast = df_forecast[df_forecast['Category'] == category]
            avg_forecast = cat_forecast['Forecast'].mean()
            total_forecast = cat_forecast['Forecast'].sum()
            peak_demand = cat_forecast['Forecast'].max()
            peak_date = cat_forecast.loc[cat_forecast['Forecast'].idxmax(), 'Date']
            
            summary_data.append({
                'Category': category,
                'Avg Daily Demand': f"{avg_forecast:.0f}",
                'Total Demand': f"{total_forecast:.0f}",
                'Peak Demand': f"{peak_demand:.0f}",
                'Peak Date': peak_date.strftime('%Y-%m-%d')
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True)
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        for category in selected_categories:
            cat_forecast = df_forecast[df_forecast['Category'] == category]
            avg_demand = cat_forecast['Forecast'].mean()
            
            if avg_demand > 150:
                st.success(f"📈 {category}: High demand expected - increase inventory by 20%")
            elif avg_demand > 100:
                st.info(f"📊 {category}: Moderate demand expected - maintain current inventory")
            else:
                st.warning(f"📉 {category}: Low demand expected - consider promotional campaigns")

def display_recommendations():
    """Display AI-powered recommendations"""
    st.header("🎯 AI-Powered Recommendations")
    
    # Recommendation categories
    rec_tab1, rec_tab2, rec_tab3, rec_tab4 = st.tabs(["📦 Inventory", "💰 Pricing", "📊 Operations", "👥 Customers"])
    
    with rec_tab1:
        st.subheader("📦 Inventory Recommendations")
        
        inventory_recs = [
            {
                "type": "🔴 Critical",
                "item": "SKU-12345 (Wireless Headphones)",
                "recommendation": "Immediate restock required - only 2 days of inventory left",
                "action": "Order 500 units",
                "impact": "Prevent stockout, maintain $50K revenue"
            },
            {
                "type": "🟡 Warning",
                "item": "SKU-67890 (Gaming Console)",
                "recommendation": "Stock level approaching minimum threshold",
                "action": "Order 200 units",
                "impact": "Maintain service level, prevent backorders"
            },
            {
                "type": "🟢 Opportunity",
                "item": "SKU-11111 (Smart Watch)",
                "recommendation": "Increase stock for upcoming promotion",
                "action": "Order 300 units",
                "impact": "Maximize promotional revenue"
            }
        ]
        
        for rec in inventory_recs:
            with st.expander(f"{rec['type']} - {rec['item']}"):
                st.write(f"**Recommendation:** {rec['recommendation']}")
                st.write(f"**Suggested Action:** {rec['action']}")
                st.write(f"**Expected Impact:** {rec['impact']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Accept", key=f"inv_{rec['item']}"):
                        st.success("Recommendation accepted. Purchase order created.")
                with col2:
                    if st.button(f"❌ Decline", key=f"inv_decline_{rec['item']}"):
                        st.info("Recommendation declined.")
    
    with rec_tab2:
        st.subheader("💰 Pricing Recommendations")
        
        pricing_recs = [
            {
                "type": "🚀 Increase",
                "item": "Premium Electronics Category",
                "current_price": "$299",
                "recommended_price": "$319",
                "reason": "High demand, low price sensitivity",
                "impact": "+$25K monthly revenue"
            },
            {
                "type": "📉 Decrease",
                "item": "Seasonal Clothing",
                "current_price": "$79",
                "recommended_price": "$65",
                "reason": "Clear inventory before season end",
                "impact": "Reduce excess inventory by 40%"
            },
            {
                "type": "🎯 Optimize",
                "item": "Home Appliances",
                "current_price": "$199",
                "recommended_price": "$189",
                "reason": "Match competitor pricing",
                "impact": "Increase market share by 5%"
            }
        ]
        
        for rec in pricing_recs:
            with st.expander(f"{rec['type']} - {rec['item']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Current Price:** {rec['current_price']}")
                    st.write(f"**Recommended Price:** {rec['recommended_price']}")
                with col2:
                    st.write(f"**Reason:** {rec['reason']}")
                    st.write(f"**Expected Impact:** {rec['impact']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Accept", key=f"price_{rec['item']}"):
                        st.success("Price change scheduled.")
                with col2:
                    if st.button(f"❌ Decline", key=f"price_decline_{rec['item']}"):
                        st.info("Price recommendation declined.")
    
    with rec_tab3:
        st.subheader("📊 Operations Recommendations")
        
        ops_recs = [
            "🚛 Optimize delivery routes to reduce costs by 12%",
            "⏰ Adjust staffing schedule for peak hours (11 AM - 2 PM)",
            "📦 Consolidate shipments to reduce packaging waste",
            "🤖 Implement automation for high-volume SKUs",
            "📍 Relocate fast-moving items closer to packing stations"
        ]
        
        for i, rec in enumerate(ops_recs):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(rec)
            with col2:
                if st.button(f"✅", key=f"ops_{i}"):
                    st.success("Implemented!")
    
    with rec_tab4:
        st.subheader("👥 Customer Recommendations")
        
        customer_recs = [
            {
                "segment": "High-Value Customers",
                "recommendation": "Offer premium membership with exclusive benefits",
                "potential_impact": "+15% customer lifetime value"
            },
            {
                "segment": "At-Risk Customers",
                "recommendation": "Send personalized retention offers",
                "potential_impact": "Reduce churn by 25%"
            },
            {
                "segment": "New Customers",
                "recommendation": "Targeted welcome campaign with product recommendations",
                "potential_impact": "Increase repeat purchases by 30%"
            }
        ]
        
        for rec in customer_recs:
            with st.expander(f"{rec['segment']} - {rec['recommendation']}"):
                st.write(f"**Potential Impact:** {rec['potential_impact']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Launch Campaign", key=f"cust_{rec['segment']}"):
                        st.success("Campaign launched!")
                with col2:
                    if st.button(f"📝 Customize", key=f"cust_custom_{rec['segment']}"):
                        st.info("Campaign customization opened.")

def display_model_training(show_feature_importance=True):
    """Display model training interface"""
    st.header("🔧 Model Training & Management")
    
    # Training status
    st.subheader("📊 Training Status")
    
    models = [
        {"name": "Demand Forecasting", "status": "✅ Active", "accuracy": 92.3, "last_trained": "2 hours ago"},
        {"name": "Inventory Optimization", "status": "🔄 Training", "accuracy": 88.7, "last_trained": "In progress"},
        {"name": "Price Prediction", "status": "✅ Active", "accuracy": 85.1, "last_trained": "1 day ago"},
        {"name": "Customer Behavior", "status": "⚠️ Needs Update", "accuracy": 78.9, "last_trained": "5 days ago"},
        {"name": "Maintenance Prediction", "status": "✅ Active", "accuracy": 94.2, "last_trained": "6 hours ago"}
    ]
    
    df_models = pd.DataFrame(models)
    st.dataframe(df_models, use_container_width=True)
    
    # Model training controls
    st.subheader("🎛️ Training Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_model = st.selectbox("Select Model", [m["name"] for m in models])
    
    with col2:
        training_data_size = st.slider("Training Data Size (%)", 50, 100, 80)
    
    with col3:
        validation_split = st.slider("Validation Split (%)", 10, 30, 20)
    
    # Training parameters
    st.subheader("⚙️ Training Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        learning_rate = st.number_input("Learning Rate", 0.001, 0.1, 0.01, format="%.3f")
        epochs = st.number_input("Epochs", 10, 1000, 100)
    
    with col2:
        batch_size = st.number_input("Batch Size", 16, 512, 32)
        early_stopping = st.checkbox("Early Stopping", value=True)
    
    # Train model
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Training", type="primary"):
            with st.spinner("Training model..."):
                # Simulate training
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                    time.sleep(0.01)
                st.success(f"Model '{selected_model}' trained successfully!")
    
    with col2:
        if st.button("⏹️ Stop Training"):
            st.warning("Training stopped by user.")
    
    with col3:
        if st.button("📊 Evaluate Model"):
            st.info("Model evaluation started.")
    
    # Feature importance (if enabled)
    if show_feature_importance:
        st.subheader("🎯 Feature Importance")
        
        # Generate sample feature importance
        features = ['Historical Demand', 'Seasonality', 'Price', 'Promotions', 'Weather', 'Events', 'Inventory Level', 'Competitor Price']
        importance = np.random.random(len(features))
        importance = importance / importance.sum()
        
        df_importance = pd.DataFrame({
            'Feature': features,
            'Importance': importance
        }).sort_values('Importance', ascending=True)
        
        fig_importance = px.bar(df_importance, x='Importance', y='Feature', orientation='h',
                               title="Feature Importance for Selected Model")
        st.plotly_chart(fig_importance, use_container_width=True)

def display_model_performance():
    """Display model performance metrics"""
    st.header("📋 Model Performance & Monitoring")
    
    # Performance metrics
    st.subheader("📊 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Overall Accuracy", "89.2%", "↑ 2.1%")
    
    with col2:
        st.metric("⚡ Avg Prediction Time", "45ms", "↓ 5ms")
    
    with col3:
        st.metric("💾 Model Size", "12.3MB", "↓ 0.5MB")
    
    with col4:
        st.metric("🔄 Predictions/Day", "15,234", "↑ 1,205")
    
    # Performance trends
    st.subheader("📈 Performance Trends")
    
    # Generate performance trend data
    dates = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=30), 
                         end=datetime.datetime.now(), freq='D')
    
    performance_data = []
    for date in dates:
        accuracy = 85 + 10 * np.sin(date.dayofyear / 365 * 2 * np.pi) + random.uniform(-2, 2)
        precision = 82 + 8 * np.sin(date.dayofyear / 365 * 2 * np.pi) + random.uniform(-2, 2)
        recall = 80 + 12 * np.sin(date.dayofyear / 365 * 2 * np.pi) + random.uniform(-2, 2)
        
        performance_data.append({
            'Date': date,
            'Accuracy': max(0, min(100, accuracy)),
            'Precision': max(0, min(100, precision)),
            'Recall': max(0, min(100, recall))
        })
    
    df_performance = pd.DataFrame(performance_data)
    
    fig_performance = px.line(df_performance, x='Date', y=['Accuracy', 'Precision', 'Recall'],
                             title="Model Performance Trends (Last 30 Days)")
    st.plotly_chart(fig_performance, use_container_width=True)
    
    # Model comparison
    st.subheader("🔍 Model Comparison")
    
    comparison_data = {
        'Model': ['Random Forest', 'XGBoost', 'Neural Network', 'Linear Regression', 'SVM'],
        'Accuracy': [89.2, 87.5, 91.1, 76.3, 82.8],
        'Training Time': [45, 120, 300, 5, 90],
        'Prediction Time': [2, 1, 5, 0.5, 3],
        'Memory Usage': [12, 8, 25, 2, 6]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Accuracy comparison
    fig_accuracy = px.bar(df_comparison, x='Model', y='Accuracy',
                         title="Model Accuracy Comparison")
    st.plotly_chart(fig_accuracy, use_container_width=True)
    
    # Detailed comparison table
    st.dataframe(df_comparison, use_container_width=True)
    
    # Model diagnostics
    st.subheader("🔧 Model Diagnostics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Quality Issues**")
        issues = [
            "Missing values: 2.3%",
            "Outliers detected: 0.8%",
            "Data drift: Low",
            "Feature correlation: Normal"
        ]
        for issue in issues:
            st.info(issue)
    
    with col2:
        st.write("**Model Health**")
        health = [
            "Model stability: High",
            "Prediction consistency: 96%",
            "Error distribution: Normal",
            "Bias detection: Minimal"
        ]
        for h in health:
            st.success(h)
    
    # Alerts and notifications
    st.subheader("🚨 Model Alerts")
    
    alerts = [
        {"type": "⚠️ Warning", "message": "Model accuracy dropped below 85% for Customer Behavior model", "time": "2 hours ago"},
        {"type": "🔵 Info", "message": "New training data available for Demand Forecasting", "time": "4 hours ago"},
        {"type": "✅ Success", "message": "Model retraining completed successfully", "time": "1 day ago"}
    ]
    
    for alert in alerts:
        st.write(f"{alert['type']} {alert['message']} ({alert['time']})")
