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
    st.header("🔗 Supply Chain Optimization")
    st.markdown("**Advanced supply chain analytics, optimization, and management tools**")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Supply Chain Analytics", 
        "🎯 Route Optimization", 
        "📦 Supplier Management", 
        "🏭 Production Planning",
        "🌐 Network Analysis",
        "🧩 Problem Solver"  # New tab for problem-solving
    ])
    
    with tab1:
        display_supply_chain_analytics()
    
    with tab2:
        display_route_optimization()
    
    with tab3:
        display_supplier_management()
    
    with tab4:
        display_production_planning()
    
    with tab5:
        display_network_analysis()
    
    with tab6:
        display_problem_solver()  # New function for problem-solving

def display_supply_chain_analytics():
    st.subheader("📊 Supply Chain Analytics")
    
    # KPI Dashboard
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Supply Chain Efficiency", "91.2%", delta="2.8%")
        st.metric("Order Fulfillment Rate", "98.7%", delta="1.2%")
        
    with col2:
        st.metric("Inventory Turnover", "12.3x", delta="0.8x")
        st.metric("On-Time Delivery", "94.2%", delta="2.1%")
        
    with col3:
        st.metric("Cost per Order", "$18.45", delta="-$1.23")
        st.metric("Supplier Performance", "87.9%", delta="3.4%")
        
    with col4:
        st.metric("Network Utilization", "85.3%", delta="1.9%")
        st.metric("Risk Score", "2.1/10", delta="-0.3")
    
    # Supply Chain Flow Visualization
    st.markdown("### 🔄 Supply Chain Flow")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create supply chain flow diagram
        flow_data = generate_supply_chain_flow_data()
        
        fig = create_supply_chain_flow_chart(flow_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance trends
        st.markdown("### 📈 Performance Trends")
        
        # Generate performance data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        performance_data = pd.DataFrame({
            'Date': dates,
            'Efficiency': np.random.normal(91, 3, 30),
            'Cost_per_Order': np.random.normal(18.5, 2, 30),
            'Delivery_Time': np.random.normal(22, 3, 30),
            'Quality_Score': np.random.normal(94, 2, 30)
        })
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Supply Chain Efficiency', 'Cost per Order', 'Delivery Time', 'Quality Score'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                   [{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Efficiency
        fig.add_trace(
            go.Scatter(x=performance_data['Date'], y=performance_data['Efficiency'], 
                      name='Efficiency', line=dict(color='green')),
            row=1, col=1
        )
        
        # Cost per order
        fig.add_trace(
            go.Scatter(x=performance_data['Date'], y=performance_data['Cost_per_Order'], 
                      name='Cost', line=dict(color='red')),
            row=1, col=2
        )
        
        # Delivery time
        fig.add_trace(
            go.Scatter(x=performance_data['Date'], y=performance_data['Delivery_Time'], 
                      name='Delivery Time', line=dict(color='blue')),
            row=2, col=1
        )
        
        # Quality score
        fig.add_trace(
            go.Scatter(x=performance_data['Date'], y=performance_data['Quality_Score'], 
                      name='Quality', line=dict(color='orange')),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Real-time alerts
        st.markdown("### 🚨 Real-time Alerts")
        
        alerts = [
            {"level": "High", "message": "Supplier ABC delayed shipment", "time": "5 min ago", "color": "red"},
            {"level": "Medium", "message": "Warehouse capacity at 95%", "time": "12 min ago", "color": "orange"},
            {"level": "Low", "message": "New route optimization available", "time": "30 min ago", "color": "blue"},
            {"level": "Info", "message": "Demand forecast updated", "time": "1 hour ago", "color": "green"}
        ]
        
        for alert in alerts:
            st.markdown(f"""
            <div style="padding: 10px; border-left: 4px solid {alert['color']}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{alert['level']}:</strong> {alert['message']}<br>
                <small>{alert['time']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Network status
        st.markdown("### 🌐 Network Status")
        
        network_status = {
            "Warehouses": {"active": 12, "total": 15, "utilization": 85},
            "Distribution Centers": {"active": 8, "total": 10, "utilization": 78},
            "Suppliers": {"active": 45, "total": 50, "utilization": 92},
            "Transport Routes": {"active": 28, "total": 30, "utilization": 88}
        }
        
        for component, status in network_status.items():
            st.markdown(f"**{component}:**")
            st.markdown(f"Active: {status['active']}/{status['total']}")
            st.progress(status['utilization'] / 100)
            st.markdown(f"Utilization: {status['utilization']}%")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Optimize Routes"):
            with st.spinner("Optimizing routes..."):
                import time
                time.sleep(2)
                st.success("Routes optimized!")
        
        if st.button("📊 Generate Report", key="supply_chain_report"):
            st.info("Supply chain report generated!")
        
        if st.button("🎯 Run Simulation"):
            st.info("Supply chain simulation started!")

def display_route_optimization():
    st.subheader("🎯 Route Optimization")
    
    # Route optimization interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Route configuration
        st.markdown("### 🛠️ Route Configuration")
        
        config_col1, config_col2 = st.columns(2)
        
        with config_col1:
            optimization_type = st.selectbox(
                "Optimization Type",
                ["Time", "Distance", "Cost", "Fuel Efficiency", "Multi-objective"]
            )
            
            vehicle_type = st.selectbox(
                "Vehicle Type",
                ["Truck", "Van", "Delivery Vehicle", "All Types"]
            )
        
        with config_col2:
            max_stops = st.number_input("Maximum Stops", min_value=1, max_value=50, value=10)
            
            priority_factor = st.selectbox(
                "Priority Factor",
                ["Customer Priority", "Delivery Time", "Package Size", "Distance"]
            )
        
        # Route visualization
        st.markdown("### 🗺️ Route Visualization")
        
        # Generate route data
        route_data = generate_route_data()
        
        # Create route map
        fig = create_route_map(route_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Route details
        st.markdown("### 📋 Route Details")
        
        route_details = pd.DataFrame({
            'Stop': range(1, 11),
            'Location': [f'Location {i}' for i in range(1, 11)],
            'Address': [f'{100 + i * 10} Main St, City' for i in range(1, 11)],
            'Delivery_Time': [f'{9 + i}:00 AM' for i in range(10)],
            'Distance_km': np.random.uniform(2, 15, 10),
            'Priority': np.random.choice(['High', 'Medium', 'Low'], 10)
        })
        
        st.dataframe(route_details, use_container_width=True)
        
        # Optimization results
        st.markdown("### 📊 Optimization Results")
        
        results_col1, results_col2, results_col3 = st.columns(3)
        
        with results_col1:
            st.metric("Total Distance", "125.6 km", delta="-18.2 km")
            st.metric("Total Time", "4.2 hours", delta="-0.8 hours")
        
        with results_col2:
            st.metric("Fuel Cost", "$45.30", delta="-$8.70")
            st.metric("CO2 Emissions", "28.5 kg", delta="-5.2 kg")
        
        with results_col3:
            st.metric("Cost Savings", "$125.50", delta="+$125.50")
            st.metric("Time Savings", "48 minutes", delta="+48 minutes")
    
    with col2:
        # Route optimization controls
        st.markdown("### 🎛️ Controls")
        
        if st.button("🚀 Start Optimization", type="primary"):
            with st.spinner("Optimizing routes..."):
                import time
                time.sleep(3)
                st.success("Route optimization completed!")
        
        if st.button("💾 Save Route"):
            st.success("Route saved successfully!")
        
        if st.button("📤 Export Route"):
            st.info("Route data exported!")
        
        if st.button("🔄 Reset"):
            st.info("Route reset to original state!")
        
        # Algorithm selection
        st.markdown("### 🧮 Algorithm Settings")
        
        algorithm = st.selectbox(
            "Optimization Algorithm",
            ["Genetic Algorithm", "Ant Colony", "Simulated Annealing", "Nearest Neighbor"]
        )
        
        iterations = st.slider("Iterations", min_value=100, max_value=10000, value=1000)
        
        population_size = st.slider("Population Size", min_value=10, max_value=200, value=50)
        
        # Constraints
        st.markdown("### ⚙️ Constraints")
        
        time_windows = st.checkbox("Time Windows", value=True)
        vehicle_capacity = st.checkbox("Vehicle Capacity", value=True)
        driver_hours = st.checkbox("Driver Hours", value=True)
        customer_priority = st.checkbox("Customer Priority", value=False)
        
        # Performance metrics
        st.markdown("### 📊 Performance")
        
        performance_metrics = {
            "Algorithm Efficiency": 94.2,
            "Convergence Rate": 87.5,
            "Solution Quality": 92.8,
            "Processing Time": 2.3
        }
        
        for metric, value in performance_metrics.items():
            if metric == "Processing Time":
                st.metric(metric, f"{value} seconds")
            else:
                st.metric(metric, f"{value}%")

def display_supplier_management():
    st.subheader("📦 Supplier Management")
    
    # Supplier dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Supplier overview
        st.markdown("### 🏢 Supplier Overview")
        
        supplier_data = generate_supplier_data()
        
        # Supplier filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            category_filter = st.selectbox(
                "Category",
                ["All"] + list(supplier_data['Category'].unique())
            )
        
        with filter_col2:
            region_filter = st.selectbox(
                "Region",
                ["All"] + list(supplier_data['Region'].unique())
            )
        
        with filter_col3:
            performance_filter = st.selectbox(
                "Performance",
                ["All", "Excellent", "Good", "Average", "Poor"]
            )
        
        # Apply filters
        filtered_data = supplier_data.copy()
        
        if category_filter != "All":
            filtered_data = filtered_data[filtered_data['Category'] == category_filter]
        
        if region_filter != "All":
            filtered_data = filtered_data[filtered_data['Region'] == region_filter]
        
        if performance_filter != "All":
            filtered_data = filtered_data[filtered_data['Performance_Rating'] == performance_filter]
        
        # Supplier table
        st.dataframe(
            filtered_data,
            use_container_width=True,
            column_config={
                "Performance_Score": st.column_config.ProgressColumn(
                    "Performance",
                    help="Supplier performance score",
                    min_value=0,
                    max_value=100
                ),
                "Risk_Level": st.column_config.TextColumn(
                    "Risk Level",
                    help="Supplier risk assessment"
                )
            }
        )
        
        # Supplier performance trends
        st.markdown("### 📈 Performance Trends")
        
        # Generate performance trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=90), periods=90, freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Quality_Score': np.random.normal(92, 3, 90),
            'Delivery_Performance': np.random.normal(88, 4, 90),
            'Cost_Efficiency': np.random.normal(85, 3, 90),
            'Responsiveness': np.random.normal(90, 3, 90)
        })
        
        fig = go.Figure()
        
        metrics = ['Quality_Score', 'Delivery_Performance', 'Cost_Efficiency', 'Responsiveness']
        colors = ['blue', 'green', 'red', 'orange']
        
        for metric, color in zip(metrics, colors):
            fig.add_trace(go.Scatter(
                x=trend_data['Date'],
                y=trend_data[metric],
                name=metric.replace('_', ' '),
                line=dict(color=color, width=2)
            ))
        
        fig.update_layout(
            title="Supplier Performance Trends",
            xaxis_title="Date",
            yaxis_title="Score",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Supplier statistics
        st.markdown("### 📊 Supplier Statistics")
        
        total_suppliers = len(supplier_data)
        active_suppliers = len(supplier_data[supplier_data['Status'] == 'Active'])
        avg_performance = supplier_data['Performance_Score'].mean()
        high_risk = len(supplier_data[supplier_data['Risk_Level'] == 'High'])
        
        st.metric("Total Suppliers", total_suppliers)
        st.metric("Active Suppliers", active_suppliers, delta=f"+{active_suppliers - total_suppliers + 5}")
        st.metric("Avg Performance", f"{avg_performance:.1f}%", delta="2.3%")
        st.metric("High Risk", high_risk, delta=f"-{2}")
        
        # Supplier distribution
        st.markdown("### 🌍 Geographic Distribution")
        
        region_counts = supplier_data['Region'].value_counts()
        fig = px.pie(
            values=region_counts.values,
            names=region_counts.index,
            title="Suppliers by Region"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk assessment
        st.markdown("### ⚠️ Risk Assessment")
        
        risk_items = [
            {"supplier": "Supplier A", "risk": "Delivery delays", "level": "High"},
            {"supplier": "Supplier B", "risk": "Quality issues", "level": "Medium"},
            {"supplier": "Supplier C", "risk": "Financial stability", "level": "Low"},
            {"supplier": "Supplier D", "risk": "Capacity constraints", "level": "Medium"}
        ]
        
        for item in risk_items:
            color = "red" if item["level"] == "High" else "orange" if item["level"] == "Medium" else "green"
            st.markdown(f"""
            <div style="padding: 8px; border-left: 4px solid {color}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{item['supplier']}</strong><br>
                {item['risk']} ({item['level']} risk)
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("➕ Add Supplier"):
            st.info("New supplier form opened!")
        
        if st.button("📊 Performance Review"):
            st.info("Performance review initiated!")
        
        if st.button("🔄 Update Contracts"):
            st.info("Contract updates started!")

def display_production_planning():
    st.subheader("🏭 Production Planning")
    
    # Production planning interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Production overview
        st.markdown("### 📊 Production Overview")
        
        # Production metrics
        prod_col1, prod_col2, prod_col3, prod_col4 = st.columns(4)
        
        with prod_col1:
            st.metric("Production Rate", "95.2%", delta="2.1%")
            st.metric("Efficiency", "88.7%", delta="1.5%")
        
        with prod_col2:
            st.metric("Quality Score", "96.3%", delta="0.8%")
            st.metric("On-Time Delivery", "92.1%", delta="1.2%")
        
        with prod_col3:
            st.metric("Capacity Utilization", "84.5%", delta="3.2%")
            st.metric("Waste Reduction", "12.3%", delta="-1.8%")
        
        with prod_col4:
            st.metric("Cost per Unit", "$15.80", delta="-$0.45")
            st.metric("Cycle Time", "4.2 hrs", delta="-0.3 hrs")
        
        # Production schedule
        st.markdown("### 📅 Production Schedule")
        
        schedule_data = generate_production_schedule()
        
        st.dataframe(
            schedule_data,
            use_container_width=True,
            column_config={
                "Completion": st.column_config.ProgressColumn(
                    "Completion",
                    help="Production completion percentage",
                    min_value=0,
                    max_value=100
                ),
                "Priority": st.column_config.TextColumn(
                    "Priority",
                    help="Production priority level"
                )
            }
        )
        
        # Capacity planning
        st.markdown("### 📊 Capacity Planning")
        
        # Generate capacity data
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        capacity_data = pd.DataFrame({
            'Date': dates,
            'Planned_Capacity': np.random.normal(85, 5, 30),
            'Actual_Capacity': np.random.normal(82, 6, 30),
            'Demand_Forecast': np.random.normal(80, 8, 30)
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=capacity_data['Date'],
            y=capacity_data['Planned_Capacity'],
            name='Planned Capacity',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=capacity_data['Date'],
            y=capacity_data['Actual_Capacity'],
            name='Actual Capacity',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=capacity_data['Date'],
            y=capacity_data['Demand_Forecast'],
            name='Demand Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Capacity Planning - Next 30 Days",
            xaxis_title="Date",
            yaxis_title="Capacity (%)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Production controls
        st.markdown("### 🎛️ Production Controls")
        
        if st.button("🚀 Start Production", type="primary"):
            st.success("Production started!")
        
        if st.button("⏸️ Pause Production"):
            st.warning("Production paused!")
        
        if st.button("🔄 Reset Schedule"):
            st.info("Schedule reset!")
        
        if st.button("📊 Generate Forecast"):
            st.info("Demand forecast generated!")
        
        # Resource allocation
        st.markdown("### 🔧 Resource Allocation")
        
        resources = {
            "Labor": {"allocated": 85, "available": 100},
            "Machinery": {"allocated": 78, "available": 95},
            "Materials": {"allocated": 92, "available": 100},
            "Energy": {"allocated": 67, "available": 100}
        }
        
        for resource, data in resources.items():
            st.markdown(f"**{resource}:**")
            utilization = data['allocated'] / data['available']
            st.progress(utilization)
            st.markdown(f"{data['allocated']}/{data['available']} ({utilization*100:.1f}%)")
        
        # Bottleneck analysis
        st.markdown("### 🚧 Bottleneck Analysis")
        
        bottlenecks = [
            {"process": "Assembly Line 3", "impact": "High", "delay": "2.5 hrs"},
            {"process": "Quality Control", "impact": "Medium", "delay": "1.2 hrs"},
            {"process": "Packaging", "impact": "Low", "delay": "0.8 hrs"}
        ]
        
        for bottleneck in bottlenecks:
            color = "red" if bottleneck["impact"] == "High" else "orange" if bottleneck["impact"] == "Medium" else "green"
            st.markdown(f"""
            <div style="padding: 8px; border-left: 4px solid {color}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{bottleneck['process']}</strong><br>
                Impact: {bottleneck['impact']}<br>
                Delay: {bottleneck['delay']}
            </div>
            """, unsafe_allow_html=True)

def display_network_analysis():
    st.subheader("🌐 Network Analysis")
    
    # Network visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Network topology
        st.markdown("### 🕸️ Network Topology")
        
        # Create network visualization
        network_fig = create_network_visualization()
        st.plotly_chart(network_fig, use_container_width=True)
        
        # Network performance
        st.markdown("### 📊 Network Performance")
        
        # Generate network performance data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        network_data = pd.DataFrame({
            'Date': dates,
            'Throughput': np.random.normal(85, 8, 30),
            'Latency': np.random.normal(120, 20, 30),
            'Reliability': np.random.normal(98, 2, 30),
            'Cost_Efficiency': np.random.normal(88, 5, 30)
        })
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Throughput', 'Latency', 'Reliability', 'Cost Efficiency'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                   [{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Add traces
        fig.add_trace(
            go.Scatter(x=network_data['Date'], y=network_data['Throughput'], name='Throughput'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=network_data['Date'], y=network_data['Latency'], name='Latency'),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=network_data['Date'], y=network_data['Reliability'], name='Reliability'),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=network_data['Date'], y=network_data['Cost_Efficiency'], name='Cost Efficiency'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Network statistics
        st.markdown("### 📊 Network Statistics")
        
        st.metric("Total Nodes", "47", delta="+3")
        st.metric("Active Connections", "156", delta="+12")
        st.metric("Network Efficiency", "91.2%", delta="2.1%")
        st.metric("Redundancy Level", "3.4x", delta="0.2x")
        
        # Node status
        st.markdown("### 🔍 Node Status")
        
        node_status = {
            "Warehouses": {"active": 12, "total": 15},
            "Distribution Centers": {"active": 8, "total": 10},
            "Retail Stores": {"active": 25, "total": 30},
            "Suppliers": {"active": 42, "total": 45}
        }
        
        for node_type, status in node_status.items():
            st.markdown(f"**{node_type}:**")
            st.markdown(f"Active: {status['active']}/{status['total']}")
            st.progress(status['active'] / status['total'])
        
        # Critical path analysis
        st.markdown("### 🛣️ Critical Paths")
        
        critical_paths = [
            {"path": "Supplier A → Warehouse 1 → Store 5", "utilization": 95, "risk": "High"},
            {"path": "Supplier B → DC 2 → Store 12", "utilization": 87, "risk": "Medium"},
            {"path": "Supplier C → Warehouse 3 → Store 8", "utilization": 78, "risk": "Low"}
        ]
        
        for path in critical_paths:
            color = "red" if path["risk"] == "High" else "orange" if path["risk"] == "Medium" else "green"
            st.markdown(f"""
            <div style="padding: 8px; border-left: 4px solid {color}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{path['path']}</strong><br>
                Utilization: {path['utilization']}%<br>
                Risk: {path['risk']}
            </div>
            """, unsafe_allow_html=True)

def display_problem_solver():
    """Advanced supply chain problem solving functionality"""
    st.subheader("🧩 Supply Chain Problem Solver")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
    ">
        <div style="font-size: 1.1rem; color: #4f46e5; margin-bottom: 10px;">
            🧠 AI-Powered Problem Resolution
        </div>
        <div style="font-size: 0.95rem; color: #6b7280;">
            Select a supply chain problem category and use our advanced AI engine to generate optimized solutions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Problem categories
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 Problem Categories")
        problem_category = st.radio(
            "Select a category",
            [
                "🚚 Transportation & Logistics",
                "📦 Inventory Optimization",
                "🏭 Production Bottlenecks",
                "🌐 Network Distribution",
                "🔄 Reverse Logistics",
                "🏢 Warehouse Optimization",
                "📊 Demand Forecasting",
                "💰 Cost Reduction"
            ],
            label_visibility="collapsed"
        )
        
        # Upload option
        st.markdown("### 📤 Custom Problem")
        st.file_uploader("Upload data for analysis", type=["csv", "xlsx"], help="Upload your supply chain data for custom analysis")
    
    with col2:
        # Display different problem-solving interfaces based on the selection
        if problem_category == "🚚 Transportation & Logistics":
            display_transportation_problem_solver()
        elif problem_category == "📦 Inventory Optimization":
            display_inventory_problem_solver()
        elif problem_category == "🏭 Production Bottlenecks":
            display_production_problem_solver()
        elif problem_category == "🌐 Network Distribution":
            display_network_problem_solver()
        elif problem_category == "🔄 Reverse Logistics":
            display_reverse_logistics_solver()
        elif problem_category == "🏢 Warehouse Optimization":
            display_warehouse_optimization_solver()
        elif problem_category == "📊 Demand Forecasting":
            display_demand_forecasting_solver()
        elif problem_category == "💰 Cost Reduction":
            display_cost_reduction_solver()

def display_transportation_problem_solver():
    """Transportation and logistics problem solver"""
    st.markdown("## 🚚 Transportation & Logistics Solver")
    
    # Problem description
    st.markdown("""
    Optimize transportation routes, carrier selection, and delivery scheduling to reduce costs and improve service levels.
    """)
    
    # Input form
    with st.form("transportation_solver_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            num_destinations = st.number_input("Number of Destinations", min_value=1, max_value=100, value=5)
            vehicle_types = st.multiselect(
                "Available Vehicle Types",
                ["Small Truck", "Medium Truck", "Large Truck", "Van", "Refrigerated Truck"],
                default=["Medium Truck", "Large Truck"]
            )
        
        with col2:
            priority = st.selectbox(
                "Optimization Priority",
                ["Balance Cost & Time", "Minimize Cost", "Minimize Time", "Maximize Service Level"]
            )
            constraints = st.multiselect(
                "Constraints",
                ["Time Windows", "Vehicle Capacity", "Driver Hours", "Road Restrictions", "Loading/Unloading Times"],
                default=["Vehicle Capacity", "Time Windows"]
            )
        
        # Map for visualization
        st.markdown("### 🗺️ Distribution Network")
        
        # Generate a mock map
        fig = go.Figure(go.Scattermapbox(
            mode="markers+lines",
            lon=[-74.006, -75.165, -73.757, -72.682, -71.059, -73.935],
            lat=[40.713, 39.952, 42.652, 41.763, 42.360, 40.730],
            marker=dict(size=12, color="blue"),
            line=dict(width=2, color="red"),
        ))
        
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lon=-73.5, lat=41),
                zoom=5.5
            ),
            height=300,
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Solve Transportation Problem", use_container_width=True)
    
    # Show solution if submitted
    if submitted:
        st.success("✅ Problem solved successfully!")
        
        # Tabs for different solution views
        solution_tab1, solution_tab2, solution_tab3 = st.tabs([
            "Optimized Routes", 
            "Cost Analysis", 
            "Schedule"
        ])
        
        with solution_tab1:
            st.markdown("### 🛣️ Optimized Routes")
            
            # Route visualization
            fig = go.Figure(go.Scattermapbox(
                mode="markers+lines",
                lon=[-74.006, -73.757, -71.059, -72.682, -75.165, -74.006],
                lat=[40.713, 42.652, 42.360, 41.763, 39.952, 40.713],
                marker=dict(size=12, color="blue"),
                line=dict(width=2, color="green"),
            ))
            
            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    center=dict(lon=-73.5, lat=41),
                    zoom=5.5
                ),
                height=400,
                margin={"r":0,"t":0,"l":0,"b":0}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Route details
            route_data = {
                "Route": ["Route 1", "Route 2", "Route 3"],
                "Vehicle": ["Large Truck", "Medium Truck", "Large Truck"],
                "Destinations": ["5", "4", "3"],
                "Distance (mi)": ["285", "190", "210"],
                "Duration": ["5h 20m", "3h 45m", "4h 10m"],
                "Fuel Cost": ["$142.50", "$95.00", "$105.00"],
            }
            
            st.dataframe(pd.DataFrame(route_data), use_container_width=True)
        
        with solution_tab2:
            st.markdown("### 💰 Cost Analysis")
            
            # Cost breakdown
            cost_data = {
                "Category": ["Fuel", "Labor", "Maintenance", "Tolls", "Total"],
                "Cost": [342.50, 580.00, 95.00, 45.00, 1062.50],
                "Percentage": ["32.2%", "54.6%", "8.9%", "4.2%", "100%"]
            }
            
            # Cost chart
            fig = px.pie(
                cost_data, 
                values='Cost', 
                names='Category',
                color_discrete_sequence=px.colors.sequential.Blugrn,
                hole=0.4
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost savings
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Previous Cost", "$1,275.00")
            with col2:
                st.metric("New Cost", "$1,062.50")
            with col3:
                st.metric("Savings", "$212.50 (16.7%)", delta="16.7%")
        
        with solution_tab3:
            st.markdown("### 📅 Optimized Schedule")
            
            # Schedule visualization
            schedule_data = {
                "Vehicle": ["Large Truck 1", "Medium Truck 1", "Large Truck 2"],
                "Departure": ["08:00 AM", "09:30 AM", "10:15 AM"],
                "Stops": [5, 4, 3],
                "Return": ["02:20 PM", "01:15 PM", "02:25 PM"]
            }
            
            # Create schedule chart
            fig = px.timeline(
                pd.DataFrame([
                    {"Vehicle": "Large Truck 1", "Start": 8.0, "End": 14.33, "Task": "Route 1"},
                    {"Vehicle": "Medium Truck 1", "Start": 9.5, "End": 13.25, "Task": "Route 2"},
                    {"Vehicle": "Large Truck 2", "Start": 10.25, "End": 14.42, "Task": "Route 3"}
                ]),
                x_start="Start",
                x_end="End",
                y="Vehicle",
                color="Task",
                title="Vehicle Schedule (24h)"
            )
            
            fig.update_layout(height=300)
            fig.update_xaxes(
                tickvals=[6, 8, 10, 12, 14, 16, 18],
                ticktext=["6 AM", "8 AM", "10 AM", "12 PM", "2 PM", "4 PM", "6 PM"]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Driver assignments
            st.markdown("#### 👤 Driver Assignments")
            driver_data = {
                "Driver": ["John D.", "Sarah M.", "Robert K."],
                "Vehicle": ["Large Truck 1", "Medium Truck 1", "Large Truck 2"],
                "Route": ["Route 1", "Route 2", "Route 3"],
                "Hours": ["6h 20m", "3h 45m", "4h 10m"]
            }
            
            st.dataframe(pd.DataFrame(driver_data), use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        st.info("""
        1. **Consolidate Shipments**: Combine deliveries to northeastern destinations to reduce total mileage by 12%
        2. **Adjust Departure Times**: Schedule departures between 7-9 AM to avoid rush hour traffic
        3. **Vehicle Optimization**: Replace one large truck with two vans for urban deliveries to improve fuel efficiency
        4. **Route Adjustment**: Use alternative route for Route 1 to avoid construction on I-95 during the next 2 weeks
        """)

def display_inventory_problem_solver():
    """Inventory optimization problem solver"""
    st.markdown("## 📦 Inventory Optimization Solver")
    
    st.markdown("""
    Optimize inventory levels across your supply chain to minimize costs while ensuring adequate stock to meet customer demand.
    """)
    
    # Input form
    with st.form("inventory_solver_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            num_products = st.number_input("Number of Products", min_value=1, max_value=1000, value=50)
            storage_cost = st.slider("Storage Cost ($/unit/month)", min_value=0.1, max_value=10.0, value=2.5, step=0.1)
            lead_time = st.slider("Average Lead Time (days)", min_value=1, max_value=60, value=14)
        
        with col2:
            service_level = st.slider("Target Service Level (%)", min_value=80, max_value=99, value=95)
            seasonality = st.selectbox(
                "Demand Pattern",
                ["Stable", "Seasonal", "Highly Variable", "Trending Up", "Trending Down"]
            )
            reorder_policy = st.selectbox(
                "Reorder Policy",
                ["Fixed Order Quantity", "Min-Max", "Periodic Review", "Continuous Review"]
            )
        
        # Demand chart
        st.markdown("### 📈 Historical Demand Pattern")
        
        # Generate mock demand data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), periods=52, freq='W')
        base_demand = np.ones(52) * 1000
        
        # Add seasonality
        if seasonality == "Seasonal":
            seasonal_factors = np.sin(np.linspace(0, 4*np.pi, 52)) * 300 + base_demand
            demand_data = seasonal_factors
        elif seasonality == "Highly Variable":
            demand_data = base_demand + np.random.normal(0, 300, 52)
        elif seasonality == "Trending Up":
            demand_data = base_demand + np.linspace(0, 500, 52)
        elif seasonality == "Trending Down":
            demand_data = base_demand + np.linspace(500, 0, 52)
        else:  # Stable
            demand_data = base_demand + np.random.normal(0, 100, 52)
        
        # Create demand chart
        fig = px.line(
            x=dates, 
            y=demand_data,
            title="Weekly Demand (Last 12 Months)",
            labels={"x": "Date", "y": "Units"}
        )
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Optimize Inventory Levels", use_container_width=True)
    
    # Show solution if submitted
    if submitted:
        st.success("✅ Inventory optimization completed successfully!")
        
        # Tabs for different solution views
        solution_tab1, solution_tab2, solution_tab3 = st.tabs([
            "Optimized Levels", 
            "Cost Analysis", 
            "Implementation Plan"
        ])
        
        with solution_tab1:
            st.markdown("### 📊 Optimized Inventory Levels")
            
            # Create mock optimization results
            product_categories = ["Electronics", "Clothing", "Food", "Home Goods", "Toys"]
            current_levels = [2500, 1800, 3200, 1500, 900]
            optimal_levels = [1800, 1500, 2600, 1200, 750]
            safety_stock = [350, 300, 450, 220, 150]
            
            # Bar chart comparing current vs. optimal
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=product_categories,
                y=current_levels,
                name="Current Inventory",
                marker_color='indianred'
            ))
            
            fig.add_trace(go.Bar(
                x=product_categories,
                y=optimal_levels,
                name="Optimal Inventory",
                marker_color='lightsalmon'
            ))
            
            fig.add_trace(go.Bar(
                x=product_categories,
                y=safety_stock,
                name="Safety Stock",
                marker_color='royalblue'
            ))
            
            fig.update_layout(
                title="Current vs. Optimized Inventory Levels",
                xaxis_title="Product Category",
                yaxis_title="Units",
                legend=dict(y=0.99, x=0.01),
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Inventory Reduction", "-27.3%", "-2,750 units")
            with col2:
                st.metric("Service Level Impact", "0%", "Maintained at 95%")
            with col3:
                st.metric("Avg Safety Stock", "294 units", "14.7% of optimal")
            with col4:
                st.metric("Inventory Turns", "8.2", delta="2.1")
        
        with solution_tab2:
            st.markdown("### 💰 Cost Analysis")
            
            # Cost comparison
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Annual Holding Cost", "$297,500", "")
            with col2:
                st.metric("Optimized Annual Holding Cost", "$216,500", "")
            with col3:
                st.metric("Annual Savings", "$81,000", delta="27.2%")
            
            # Cost breakdown
            st.markdown("#### 📊 Cost Breakdown")
            
            cost_data = {
                "Cost Type": ["Holding Cost", "Ordering Cost", "Stockout Cost", "Total"],
                "Current": [297500, 42000, 15000, 354500],
                "Optimized": [216500, 48600, 8400, 273500],
                "Savings": [81000, -6600, 6600, 81000]
            }
            
            fig = px.bar(
                pd.DataFrame(cost_data),
                x="Cost Type",
                y=["Current", "Optimized"],
                barmode="group",
                labels={"value": "Annual Cost ($)", "variable": "Scenario"},
                color_discrete_sequence=["indianred", "royalblue"],
                title="Cost Breakdown"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # ROI analysis
            st.markdown("#### 📈 Return on Investment")
            
            roi_data = {
                "Month": list(range(1, 13)),
                "Cumulative Savings": [6750, 13500, 20250, 27000, 33750, 40500, 
                                      47250, 54000, 60750, 67500, 74250, 81000]
            }
            
            fig = px.line(
                pd.DataFrame(roi_data),
                x="Month",
                y="Cumulative Savings",
                markers=True,
                labels={"Cumulative Savings": "Cumulative Savings ($)"},
                title="Projected 12-Month Savings"
            )
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with solution_tab3:
            st.markdown("### 📝 Implementation Plan")
            
            # Timeline
            st.markdown("#### ⏱️ Implementation Timeline")
            
            timeline_data = {
                "Task": ["Data Validation", "Adjust Order Quantities", "Update Safety Stock", "Monitor & Adjust", "Full Implementation"],
                "Start": [0, 10, 20, 30, 60],
                "Duration": [10, 10, 10, 30, 30]
            }
            
            df = pd.DataFrame(timeline_data)
            df["End"] = df["Start"] + df["Duration"]
            
            fig = px.timeline(
                df, 
                x_start="Start", 
                x_end="End", 
                y="Task",
                color="Task",
                title="Implementation Timeline (Days)",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk assessment
            st.markdown("#### 🔍 Risk Assessment")
            
            risk_data = {
                "Risk": ["Demand Volatility", "Supplier Delays", "Data Accuracy", "System Integration"],
                "Impact": [4, 3, 5, 2],
                "Probability": [3, 4, 2, 3],
                "Score": [12, 12, 10, 6],
                "Mitigation": [
                    "Increase safety stock for volatile items by 10%",
                    "Develop backup suppliers for critical items",
                    "Validate data with physical inventory count",
                    "Test integration in staging environment first"
                ]
            }
            
            st.dataframe(pd.DataFrame(risk_data), use_container_width=True)
            
            # Action items
            st.markdown("#### ✅ Action Items")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Immediate Actions:**
                1. Update reorder points for Top 20 products
                2. Reduce order quantities for overstocked items
                3. Implement weekly review process
                4. Set up alert thresholds for stockouts
                """)
            
            with col2:
                st.markdown("""
                **30-Day Actions:**
                1. Integrate with demand forecasting system
                2. Train warehouse staff on new policies
                3. Develop supplier collaboration portal
                4. Implement ABC classification system
                """)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        st.info("""
        1. **ABC Classification**: Implement ABC analysis to prioritize inventory management efforts (20% of products represent 80% of value)
        2. **Safety Stock Levels**: Reduce safety stock for stable products, maintain higher levels for variable demand items
        3. **Order Frequency**: Increase order frequency and decrease order size for high-value items to improve cash flow
        4. **Cross-Docking**: Implement cross-docking for fast-moving items to reduce storage costs
        5. **Predictive Analytics**: Deploy machine learning for demand forecasting to further improve accuracy
        """)

# Add function stubs for the other problem solvers
def display_production_problem_solver():
    st.markdown("## 🏭 Production Bottlenecks Solver")
    st.markdown("Identify and resolve production bottlenecks to maximize throughput and efficiency.")
    st.info("Select specific production line and process parameters in the sidebar to analyze and optimize production flow.")
    
    # Mock UI - to be completed with full functionality
    st.markdown("### Coming Soon: Advanced Production Optimization")
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Kanban_board_example.jpg/800px-Kanban_board_example.jpg", 
             caption="Production Flow Visualization")
    
def display_network_problem_solver():
    st.markdown("## 🌐 Network Distribution Solver")
    st.markdown("Optimize your distribution network to reduce costs and improve service levels.")
    st.info("Upload your network data or use our simulation tools to find the optimal distribution strategy.")
    
    # Mock UI - to be completed with full functionality
    st.markdown("### Coming Soon: Network Optimization")
    
    # Display sample network graph
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Breadth-First-Search-Algorithm.gif/440px-Breadth-First-Search-Algorithm.gif",
             caption="Network Optimization Example")

def display_reverse_logistics_solver():
    st.markdown("## 🔄 Reverse Logistics Solver")
    st.markdown("Optimize the flow of returned products, recycling, and waste management.")
    st.info("Configure return processing parameters to streamline reverse logistics operations.")
    
    # Mock UI - to be completed with full functionality
    st.markdown("### Coming Soon: Return Process Optimization")

def display_warehouse_optimization_solver():
    st.markdown("## 🏢 Warehouse Optimization Solver")
    st.markdown("Optimize warehouse layout, picking routes, and storage assignments.")
    st.info("Upload warehouse layout to generate optimized storage and retrieval strategies.")
    
    # Mock UI - to be completed with full functionality
    st.markdown("### Coming Soon: Warehouse Layout Optimization")

def display_demand_forecasting_solver():
    """
    Advanced demand forecasting module using machine learning and statistical models.
    
    This function implements a comprehensive demand forecasting tool that:
    1. Allows users to select forecast parameters (horizon, models, etc.)
    2. Visualizes historical demand data
    3. Generates forecasts using multiple models
    4. Compares model performance
    5. Provides implementation recommendations
    
    The interface is designed for both technical and non-technical users with
    intuitive controls and informative visualizations.
    """
    st.markdown("## 📊 Demand Forecasting Solver")
    st.markdown("Apply advanced machine learning models to improve demand forecasting accuracy.")
    
    # Input form for forecast parameters
    with st.form("demand_forecasting_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Left column parameters
            forecast_periods = st.slider(
                "Forecast Horizon (weeks)", 
                min_value=4, 
                max_value=52, 
                value=12,
                help="Number of weeks to forecast into the future"
            )
            
            # Product category selection
            product_category = st.selectbox(
                "Product Category",
                ["Electronics", "Clothing", "Food & Grocery", "Home & Garden", "Toys & Games", "All Categories"],
                help="Select a product category to forecast"
            )
            
            # Seasonality control - higher values produce stronger seasonal patterns
            seasonality_strength = st.slider(
                "Seasonality Strength", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.5, 
                step=0.1,
                help="Controls how strong seasonal patterns appear in the forecast (0=none, 1=strong)"
            )
        
        with col2:
            # Right column parameters
            
            # Model selection for ensemble forecasting
            models = st.multiselect(
                "Select Forecast Models",
                ["ARIMA", "Prophet", "Exponential Smoothing", "LSTM", "Linear Regression", "Random Forest", "XGBoost"],
                default=["ARIMA", "Prophet", "Exponential Smoothing"],
                help="Select multiple models for ensemble forecasting"
            )
            
            # Confidence interval for uncertainty visualization
            confidence_interval = st.slider(
                "Confidence Interval", 
                min_value=70, 
                max_value=99, 
                value=95,
                help="Controls the width of the prediction interval (higher = wider bands)"
            )
            
            # External features to incorporate into the forecast
            include_features = st.multiselect(
                "External Features to Include",
                ["Holidays", "Promotions", "Competitor Pricing", "Weather", "Economic Indicators"],
                default=["Holidays", "Promotions"],
                help="Additional factors to consider in the forecast models"
            )
        
        # Historical data visualization
        st.markdown("### 📈 Historical Data")
        
        # Generate mock historical data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365*2), periods=104, freq='W')
        base_demand = 1000 + np.random.normal(0, 50, 104)
        
        # Add trend
        trend = np.linspace(0, 300, 104)
        
        # Add seasonality
        seasonality = np.sin(np.linspace(0, 2*np.pi*4, 104)) * 200 * seasonality_strength
        
        # Add holidays effect
        holidays = np.zeros(104)
        # Major holidays indexes (approximate)
        holiday_indexes = [0, 12, 24, 51, 52, 64, 76, 103]
        holidays[holiday_indexes] = 300
        
        # Combine components
        demand = base_demand + trend + seasonality + holidays
        
        # Create historical data chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates, 
            y=demand,
            mode='lines',
            name='Historical Demand',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Historical Demand Data",
            xaxis_title="Date",
            yaxis_title="Units Sold",
            height=300,
            margin=dict(t=50, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate Forecast", use_container_width=True)
    
    # Show solution if submitted
    if submitted:
        st.success("✅ Demand forecast generated successfully!")
        
        # Tabs for different solution views
        solution_tab1, solution_tab2, solution_tab3 = st.tabs([
            "Forecast Results", 
            "Model Comparison", 
            "Implementation Plan"
        ])
        
        with solution_tab1:
            st.markdown("### 🔮 Demand Forecast")
            
            # Generate forecast data
            historical_dates = pd.date_range(start=datetime.now() - timedelta(days=365), periods=52, freq='W')
            forecast_dates = pd.date_range(start=datetime.now(), periods=forecast_periods, freq='W')
            
            # Historical data
            historical_demand = 1000 + np.random.normal(0, 50, 52)
            historical_demand += np.sin(np.linspace(0, 2*np.pi*2, 52)) * 200 * seasonality_strength
            historical_demand += np.linspace(0, 150, 52)  # Add trend
            
            # Forecast data
            forecast_demand = 1150 + np.random.normal(0, 30, forecast_periods)
            forecast_demand += np.sin(np.linspace(0, 2*np.pi*(forecast_periods/52), forecast_periods)) * 200 * seasonality_strength
            forecast_demand += np.linspace(0, 75, forecast_periods)  # Continue trend
            
            # Upper and lower bounds
            forecast_upper = forecast_demand + np.linspace(50, 100, forecast_periods)
            forecast_lower = forecast_demand - np.linspace(50, 100, forecast_periods)
            
            # Create forecast chart
            fig = go.Figure()
            
            # Add historical data
            fig.add_trace(go.Scatter(
                x=historical_dates,
                y=historical_demand,
                mode='lines',
                name='Historical Data',
                line=dict(color='blue', width=2)
            ))
            
            # Add forecast
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=forecast_demand,
                mode='lines',
                name='Forecast',
                line=dict(color='red', width=2)
            ))
            
            # Add confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_dates.tolist() + forecast_dates.tolist()[::-1],
                y=forecast_upper.tolist() + forecast_lower.tolist()[::-1],
                fill='toself',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,0,0,0)'),
                name=f'{confidence_interval}% Confidence Interval'
            ))
            
            # Add vertical line for today
            fig.add_vline(x=datetime.now(), line_dash="dash", line_color="green", annotation_text="Today")
            
            fig.update_layout(
                title="Demand Forecast with Confidence Intervals",
                xaxis_title="Date",
                yaxis_title="Units",
                legend=dict(y=0.99, x=0.01),
                height=400,
                margin=dict(t=50, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key metrics
            st.markdown("### 📊 Forecast Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg. Weekly Demand", f"{int(forecast_demand.mean())}", delta=f"{int(forecast_demand.mean() - historical_demand.mean())}")
            with col2:
                st.metric("Peak Demand", f"{int(forecast_demand.max())}", delta=f"{int(forecast_demand.max() - historical_demand.max())}")
            with col3:
                st.metric("Total Forecast", f"{int(forecast_demand.sum())}", delta=f"{int((forecast_demand.sum() / historical_demand[-forecast_periods:].sum() - 1) * 100)}%")
            with col4:
                st.metric("MAPE", "4.3%", delta="-0.7%", delta_color="inverse")
        
        with solution_tab2:
            st.markdown("### 🧪 Model Comparison")
            
            # Model performance comparison
            model_data = pd.DataFrame({
                "Model": ["ARIMA", "Prophet", "Exponential Smoothing", "LSTM", "Linear Regression", "Random Forest", "XGBoost"],
                "MAPE": [4.3, 4.9, 5.1, 3.8, 6.2, 4.0, 3.5],
                "RMSE": [42.1, 48.5, 50.2, 37.3, 61.5, 39.6, 34.2],
                "Computation Time (s)": [3.2, 5.8, 1.2, 12.5, 0.8, 7.3, 9.1]
            })
            
            # Filter to only selected models
            model_data = model_data[model_data["Model"].isin(models)]
            
            # Sort by MAPE
            model_data = model_data.sort_values("MAPE")
            
            # Display model comparison table
            st.dataframe(
                model_data,
                use_container_width=True,
                column_config={
                    "MAPE": st.column_config.ProgressColumn(
                        "MAPE (%)",
                        help="Mean Absolute Percentage Error",
                        format="%.1f%%",
                        min_value=0,
                        max_value=10
                    ),
                    "RMSE": st.column_config.NumberColumn(
                        "RMSE",
                        help="Root Mean Square Error",
                        format="%.1f"
                    )
                }
            )
            
            # Model comparison chart
            fig = go.Figure()
            
            # Add bars for MAPE
            fig.add_trace(go.Bar(
                x=model_data["Model"],
                y=model_data["MAPE"],
                name="MAPE (%)",
                marker_color='indianred'
            ))
            
            # Add secondary axis for computation time
            fig.add_trace(go.Scatter(
                x=model_data["Model"],
                y=model_data["Computation Time (s)"],
                name="Computation Time (s)",
                marker_color='royalblue',
                mode='markers+lines',
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Model Performance Comparison",
                xaxis_title="Model",
                yaxis_title="MAPE (%)",
                yaxis2=dict(
                    title="Computation Time (s)",
                    overlaying="y",
                    side="right"
                ),
                legend=dict(y=0.99, x=0.01),
                height=400,
                margin=dict(t=50, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Feature importance
            if "Random Forest" in models or "XGBoost" in models:
                st.markdown("### 🔍 Feature Importance")
                
                feature_data = {
                    "Feature": ["Previous Week", "Season", "Holiday", "Promotions", "Weather", "Price Change", "Day of Week", "Competitor"],
                    "Importance": [0.35, 0.18, 0.15, 0.12, 0.08, 0.06, 0.04, 0.02]
                }
                
                fig = px.bar(
                    pd.DataFrame(feature_data),
                    x="Importance",
                    y="Feature",
                    orientation='h',
                    title="Feature Importance",
                    color="Importance",
                    color_continuous_scale="Viridis"
                )
                
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with solution_tab3:
            st.markdown("### 📝 Implementation Plan")
            
            # Model deployment steps
            st.markdown("#### ⚙️ Model Deployment")
            
            steps = [
                "**Data Validation & Preparation**: Clean historical data and prepare feature engineering pipeline",
                "**Model Training**: Set up automated training workflow for selected models",
                "**Hyperparameter Tuning**: Fine-tune model parameters for optimal performance",
                "**Monitoring Setup**: Implement drift detection and model performance tracking",
                "**Integration**: Connect forecast outputs to inventory planning systems"
            ]
            
            for i, step in enumerate(steps):
                st.markdown(f"{i+1}. {step}")
            
            # Timeline
            st.markdown("#### ⏱️ Implementation Timeline")
            
            timeline_data = {
                "Task": ["Data Preparation", "Model Training", "Hyperparameter Tuning", "Testing & Validation", "Production Deployment"],
                "Start": [0, 7, 14, 21, 28],
                "Duration": [7, 7, 7, 7, 14]
            }
            
            df = pd.DataFrame(timeline_data)
            df["End"] = df["Start"] + df["Duration"]
            
            fig = px.timeline(
                df, 
                x_start="Start", 
                x_end="End", 
                y="Task",
                color="Task",
                title="Implementation Timeline (Days)",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            # Business impact
            st.markdown("#### 💰 Expected Business Impact")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Inventory Cost Reduction", "15%", delta="-$320K annually")
            
            with col2:
                st.metric("Stockout Reduction", "35%", delta="Improved customer satisfaction")
            
            with col3:
                st.metric("Planning Efficiency", "60%", delta="Reduced manual effort")
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        st.info("""
        1. **Model Ensemble**: Combine predictions from multiple models for improved accuracy (weighted average of ARIMA, Prophet and XGBoost)
        2. **Feature Engineering**: Include additional external factors like local events and competitor promotions
        3. **Hierarchical Forecasting**: Implement top-down and bottom-up forecasting approaches for multi-level product categories
        4. **Anomaly Detection**: Add pre-processing to identify and adjust for outliers in historical data
        5. **Forecast Frequency**: Update forecasts weekly and analyze variances to continuously improve the model
        """)
        
        # Download forecast data button
        st.download_button(
            label="📥 Download Forecast Data (CSV)",
            data=pd.DataFrame({
                'Date': forecast_dates,
                'Forecast': forecast_demand,
                'Upper_Bound': forecast_upper,
                'Lower_Bound': forecast_lower
            }).to_csv(index=False),
            file_name="demand_forecast.csv",
            mime="text/csv"
        )

def display_cost_reduction_solver():
    st.markdown("## 💰 Cost Reduction Solver")
    st.markdown("Identify cost-saving opportunities throughout your supply chain.")
    st.info("Enter cost structure details to identify and quantify potential savings.")
    
    # Mock UI - to be completed with full functionality
    st.markdown("### Coming Soon: Cost Optimization Analytics")

# Helper functions
def generate_supply_chain_flow_data():
    """Generate mock supply chain flow data"""
    return {
        'nodes': [
            {'id': 'suppliers', 'label': 'Suppliers', 'value': 45},
            {'id': 'warehouses', 'label': 'Warehouses', 'value': 12},
            {'id': 'distribution', 'label': 'Distribution Centers', 'value': 8},
            {'id': 'stores', 'label': 'Retail Stores', 'value': 25}
        ],
        'edges': [
            {'from': 'suppliers', 'to': 'warehouses', 'value': 1200},
            {'from': 'warehouses', 'to': 'distribution', 'value': 800},
            {'from': 'distribution', 'to': 'stores', 'value': 600}
        ]
    }

def create_supply_chain_flow_chart(data):
    """Create supply chain flow visualization"""
    fig = go.Figure()
    
    # Add nodes
    for i, node in enumerate(data['nodes']):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode='markers+text',
            marker=dict(size=node['value'], color=f'rgba(0, 100, 200, 0.7)'),
            text=f"{node['label']}<br>{node['value']}",
            textposition="middle center",
            name=node['label']
        ))
    
    # Add edges (simplified representation)
    for i in range(len(data['nodes']) - 1):
        fig.add_trace(go.Scatter(
            x=[i, i+1],
            y=[0, 0],
            mode='lines',
            line=dict(width=3, color='gray'),
            showlegend=False
        ))
    
    fig.update_layout(
        title="Supply Chain Flow",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=300
    )
    
    return fig

def generate_route_data():
    """Generate mock route data"""
    np.random.seed(42)
    
    # Generate coordinates for stops
    center_lat, center_lon = 40.7128, -74.0060  # NYC coordinates
    
    stops = []
    for i in range(10):
        lat = center_lat + np.random.normal(0, 0.1)
        lon = center_lon + np.random.normal(0, 0.1)
        stops.append({
            'stop_id': i + 1,
            'latitude': lat,
            'longitude': lon,
            'name': f'Stop {i + 1}',
            'priority': np.random.choice(['High', 'Medium', 'Low'])
        })
    
    return stops

def create_route_map(route_data):
    """Create route map visualization"""
    fig = go.Figure()
    
    # Add route stops
    lats = [stop['latitude'] for stop in route_data]
    lons = [stop['longitude'] for stop in route_data]
    names = [stop['name'] for stop in route_data]
    
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='markers+lines',
        marker=dict(size=10, color='red'),
        text=names,
        name='Route'
    ))
    
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=40.7128, lon=-74.0060),
            zoom=10
        ),
        height=500,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def generate_supplier_data():
    """Generate mock supplier data"""
    np.random.seed(42)
    
    categories = ['Electronics', 'Clothing', 'Food', 'Furniture', 'Books']
    regions = ['North America', 'Europe', 'Asia', 'South America']
    performance_ratings = ['Excellent', 'Good', 'Average', 'Poor']
    risk_levels = ['Low', 'Medium', 'High']
    statuses = ['Active', 'Inactive', 'Pending']
    
    suppliers = []
    for i in range(30):
        suppliers.append({
            'Supplier_ID': f'SUP{1000 + i}',
            'Name': f'Supplier {i + 1}',
            'Category': np.random.choice(categories),
            'Region': np.random.choice(regions),
            'Performance_Score': np.random.uniform(70, 100),
            'Performance_Rating': np.random.choice(performance_ratings),
            'Risk_Level': np.random.choice(risk_levels),
            'Status': np.random.choice(statuses, p=[0.8, 0.15, 0.05]),
            'Contract_Value': np.random.randint(50000, 2000000),
            'Lead_Time_Days': np.random.randint(5, 30),
            'Quality_Score': np.random.uniform(80, 100)
        })
    
    return pd.DataFrame(suppliers)

def generate_production_schedule():
    """Generate mock production schedule"""
    np.random.seed(42)
    
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Scheduled', 'In Progress', 'Completed', 'Delayed']
    
    schedule = []
    for i in range(20):
        schedule.append({
            'Order_ID': f'ORD{2000 + i}',
            'Product': np.random.choice(products),
            'Quantity': np.random.randint(50, 500),
            'Start_Date': datetime.now() + timedelta(days=np.random.randint(0, 30)),
            'End_Date': datetime.now() + timedelta(days=np.random.randint(1, 45)),
            'Priority': np.random.choice(priorities),
            'Status': np.random.choice(statuses),
            'Completion': np.random.uniform(0, 100),
            'Assigned_Line': f'Line {np.random.randint(1, 6)}'
        })
    
    return pd.DataFrame(schedule)

def create_network_visualization():
    """Create network topology visualization"""
    fig = go.Figure()
    
    # Mock network nodes
    nodes = [
        {'id': 'warehouse1', 'x': 0, 'y': 0, 'type': 'warehouse'},
        {'id': 'warehouse2', 'x': 2, 'y': 0, 'type': 'warehouse'},
        {'id': 'dc1', 'x': 1, 'y': 1, 'type': 'distribution'},
        {'id': 'store1', 'x': 0, 'y': 2, 'type': 'store'},
        {'id': 'store2', 'x': 2, 'y': 2, 'type': 'store'},
        {'id': 'supplier1', 'x': 0.5, 'y': -1, 'type': 'supplier'},
        {'id': 'supplier2', 'x': 1.5, 'y': -1, 'type': 'supplier'}
    ]
    
    # Add connections
    connections = [
        ('supplier1', 'warehouse1'), ('supplier2', 'warehouse2'),
        ('warehouse1', 'dc1'), ('warehouse2', 'dc1'),
        ('dc1', 'store1'), ('dc1', 'store2')
    ]
    
    # Draw connections
    for conn in connections:
        node1 = next(n for n in nodes if n['id'] == conn[0])
        node2 = next(n for n in nodes if n['id'] == conn[1])
        
        fig.add_trace(go.Scatter(
            x=[node1['x'], node2['x']],
            y=[node1['y'], node2['y']],
            mode='lines',
            line=dict(width=2, color='gray'),
            showlegend=False
        ))
    
    # Draw nodes
    colors = {'warehouse': 'blue', 'distribution': 'green', 'store': 'red', 'supplier': 'orange'}
    
    for node_type in set(n['type'] for n in nodes):
        type_nodes = [n for n in nodes if n['type'] == node_type]
        
        fig.add_trace(go.Scatter(
            x=[n['x'] for n in type_nodes],
            y=[n['y'] for n in type_nodes],
            mode='markers+text',
            marker=dict(size=20, color=colors[node_type]),
            text=[n['id'] for n in type_nodes],
            textposition="middle center",
            name=node_type.capitalize()
        ))
    
    fig.update_layout(
        title="Supply Chain Network Topology",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400
    )
    
    return fig
