import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import random
from utils.helpers import display_kpi_metrics, show_notification

def app():
    """Sustainability & Environmental Impact Dashboard"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; text-align: center;">🌱 Sustainability & Environmental Impact</h1>
        <p style="margin: 10px 0 0 0; text-align: center; font-size: 16px;">
            Carbon tracking • Waste reduction • Energy efficiency • Sustainable practices
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for sustainability settings
    with st.sidebar:
        st.header("🌍 Sustainability Settings")
        
        # Time period selection
        time_period = st.selectbox(
            "Analysis Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year", "Custom Range"]
        )
        
        # Sustainability goals
        st.subheader("🎯 Sustainability Goals")
        carbon_goal = st.slider("Carbon Reduction Goal (%)", 0, 50, 25)
        waste_goal = st.slider("Waste Reduction Goal (%)", 0, 50, 30)
        energy_goal = st.slider("Energy Efficiency Goal (%)", 0, 50, 20)
        
        # Reporting preferences
        st.subheader("📊 Reporting")
        auto_reports = st.checkbox("Auto-generate Reports", value=True)
        email_alerts = st.checkbox("Email Sustainability Alerts", value=True)
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("📊 Generate ESG Report"):
            st.success("ESG report generated!")
        if st.button("🌱 Calculate Carbon Footprint"):
            st.info("Carbon footprint calculation started")
        if st.button("♻️ Waste Audit"):
            st.info("Waste audit initiated")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌍 Overview", "💨 Carbon Footprint", "♻️ Waste Management", "⚡ Energy Usage", "🚛 Green Logistics", "📊 ESG Reporting"])
    
    with tab1:
        display_sustainability_overview()
    
    with tab2:
        display_carbon_footprint()
    
    with tab3:
        display_waste_management()
    
    with tab4:
        display_energy_usage()
    
    with tab5:
        display_green_logistics()
    
    with tab6:
        display_esg_reporting()

def display_sustainability_overview():
    """Display sustainability overview dashboard"""
    st.header("🌍 Sustainability Overview")
    
    # Key sustainability metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        carbon_reduction = random.uniform(15, 35)
        st.metric("💨 Carbon Reduction", f"{carbon_reduction:.1f}%", "↓ 2.3%")
    
    with col2:
        waste_diverted = random.uniform(60, 85)
        st.metric("♻️ Waste Diverted", f"{waste_diverted:.1f}%", "↑ 5.2%")
    
    with col3:
        energy_efficiency = random.uniform(20, 40)
        st.metric("⚡ Energy Efficiency", f"{energy_efficiency:.1f}%", "↑ 3.1%")
    
    with col4:
        renewable_energy = random.uniform(25, 50)
        st.metric("🌞 Renewable Energy", f"{renewable_energy:.1f}%", "↑ 8.5%")
    
    with col5:
        sustainability_score = random.randint(75, 95)
        st.metric("🌱 Sustainability Score", f"{sustainability_score}/100", "↑ 3")
    
    # Sustainability goals progress
    st.subheader("🎯 Sustainability Goals Progress")
    
    goals = [
        {"name": "Carbon Neutrality by 2030", "current": 65, "target": 100, "unit": "%"},
        {"name": "Zero Waste to Landfill", "current": 78, "target": 100, "unit": "%"},
        {"name": "100% Renewable Energy", "current": 42, "target": 100, "unit": "%"},
        {"name": "Sustainable Packaging", "current": 85, "target": 100, "unit": "%"},
        {"name": "Water Conservation", "current": 55, "target": 100, "unit": "%"}
    ]
    
    for goal in goals:
        progress = goal['current'] / goal['target']
        st.write(f"**{goal['name']}**")
        st.progress(progress)
        st.write(f"Progress: {goal['current']}{goal['unit']} of {goal['target']}{goal['unit']}")
        st.write("---")
    
    # Environmental impact summary
    st.subheader("🌍 Environmental Impact Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Carbon emissions breakdown
        emissions_data = {
            'Source': ['Transportation', 'Energy', 'Waste', 'Manufacturing', 'Supply Chain'],
            'CO2 Emissions (tons)': [1250, 890, 340, 670, 1120]
        }
        df_emissions = pd.DataFrame(emissions_data)
        
        fig_emissions = px.pie(df_emissions, values='CO2 Emissions (tons)', names='Source',
                              title="Carbon Emissions by Source")
        st.plotly_chart(fig_emissions, use_container_width=True)
    
    with col2:
        # Sustainability initiatives impact
        initiatives = {
            'Initiative': ['Solar Panels', 'LED Lighting', 'Recycling Program', 'Electric Fleet', 'Green Building'],
            'Annual Savings ($)': [125000, 85000, 45000, 95000, 150000]
        }
        df_initiatives = pd.DataFrame(initiatives)
        
        fig_initiatives = px.bar(df_initiatives, x='Initiative', y='Annual Savings ($)',
                                title="Sustainability Initiatives Impact")
        st.plotly_chart(fig_initiatives, use_container_width=True)
    
    # Recent sustainability achievements
    st.subheader("🏆 Recent Sustainability Achievements")
    
    achievements = [
        {"icon": "🌟", "title": "LEED Gold Certification", "description": "Achieved for new warehouse facility", "date": "2 weeks ago"},
        {"icon": "♻️", "title": "95% Waste Diversion", "description": "Exceeded monthly waste reduction target", "date": "1 month ago"},
        {"icon": "🌞", "title": "Solar Installation Complete", "description": "1MW solar array now operational", "date": "6 weeks ago"},
        {"icon": "🚛", "title": "Electric Fleet Expansion", "description": "Added 50 electric delivery vehicles", "date": "2 months ago"},
        {"icon": "💧", "title": "Water Conservation Milestone", "description": "Reduced water usage by 25%", "date": "3 months ago"}
    ]
    
    for achievement in achievements:
        st.info(f"{achievement['icon']} **{achievement['title']}** - {achievement['description']} ({achievement['date']})")
    
    # Sustainability trends
    st.subheader("📈 Sustainability Trends")
    
    # Generate trend data
    dates = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=365), 
                         end=datetime.datetime.now(), freq='M')
    
    trend_data = []
    for date in dates:
        trend_data.append({
            'Date': date,
            'Carbon Emissions (tons)': 1000 - (date.month * 50) + random.uniform(-100, 100),
            'Waste Diverted (%)': 50 + (date.month * 2) + random.uniform(-5, 5),
            'Energy Efficiency (%)': 15 + (date.month * 1.5) + random.uniform(-3, 3)
        })
    
    df_trends = pd.DataFrame(trend_data)
    
    fig_trends = px.line(df_trends, x='Date', y=['Carbon Emissions (tons)', 'Waste Diverted (%)', 'Energy Efficiency (%)'],
                        title="Sustainability Trends (Last 12 Months)")
    st.plotly_chart(fig_trends, use_container_width=True)

def display_carbon_footprint():
    """Display carbon footprint tracking"""
    st.header("💨 Carbon Footprint Tracking")
    
    # Carbon metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_emissions = random.randint(3000, 5000)
        st.metric("🏭 Total Emissions", f"{total_emissions:,} tons CO2", "↓ 250 tons")
    
    with col2:
        emissions_per_unit = random.uniform(0.5, 1.5)
        st.metric("📦 Emissions per Unit", f"{emissions_per_unit:.2f} kg CO2", "↓ 0.15 kg")
    
    with col3:
        carbon_offset = random.randint(500, 1000)
        st.metric("🌳 Carbon Offset", f"{carbon_offset:,} tons", "↑ 100 tons")
    
    with col4:
        net_emissions = total_emissions - carbon_offset
        st.metric("🎯 Net Emissions", f"{net_emissions:,} tons CO2", "↓ 350 tons")
    
    # Carbon emissions by scope
    st.subheader("📊 Carbon Emissions by Scope")
    
    scope_data = {
        'Scope': ['Scope 1 (Direct)', 'Scope 2 (Indirect)', 'Scope 3 (Value Chain)'],
        'Emissions (tons CO2)': [1200, 1800, 2000],
        'Percentage': [24, 36, 40]
    }
    df_scope = pd.DataFrame(scope_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scope_pie = px.pie(df_scope, values='Emissions (tons CO2)', names='Scope',
                              title="Emissions by Scope")
        st.plotly_chart(fig_scope_pie, use_container_width=True)
    
    with col2:
        fig_scope_bar = px.bar(df_scope, x='Scope', y='Emissions (tons CO2)',
                              title="Emissions by Scope (Detailed)")
        st.plotly_chart(fig_scope_bar, use_container_width=True)
    
    # Carbon footprint by facility
    st.subheader("🏢 Carbon Footprint by Facility")
    
    facilities = ['Dallas DC', 'Chicago Hub', 'Atlanta Hub', 'Austin Specialty', 'Miami Branch']
    facility_data = []
    
    for facility in facilities:
        facility_data.append({
            'Facility': facility,
            'Emissions (tons CO2)': random.randint(500, 1200),
            'Energy Usage (MWh)': random.randint(800, 2000),
            'Carbon Intensity': random.uniform(0.4, 0.8)
        })
    
    df_facilities = pd.DataFrame(facility_data)
    
    fig_facilities = px.scatter(df_facilities, x='Energy Usage (MWh)', y='Emissions (tons CO2)',
                               size='Carbon Intensity', color='Facility',
                               title="Facility Carbon Footprint Analysis")
    st.plotly_chart(fig_facilities, use_container_width=True)
    
    # Carbon reduction initiatives
    st.subheader("🌱 Carbon Reduction Initiatives")
    
    initiatives = [
        {"name": "LED Lighting Upgrade", "reduction": 150, "investment": 50000, "payback": 2.5, "status": "✅ Complete"},
        {"name": "HVAC Optimization", "reduction": 200, "investment": 75000, "payback": 3.2, "status": "🔄 In Progress"},
        {"name": "Solar Panel Installation", "reduction": 300, "investment": 200000, "payback": 5.8, "status": "📋 Planned"},
        {"name": "Electric Vehicle Fleet", "reduction": 250, "investment": 150000, "payback": 4.1, "status": "🔄 In Progress"},
        {"name": "Renewable Energy Contract", "reduction": 400, "investment": 0, "payback": 0, "status": "📋 Planned"}
    ]
    
    for initiative in initiatives:
        with st.expander(f"{initiative['name']} - {initiative['status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("CO2 Reduction", f"{initiative['reduction']} tons/year")
            
            with col2:
                st.metric("Investment", f"${initiative['investment']:,}")
            
            with col3:
                if initiative['payback'] > 0:
                    st.metric("Payback Period", f"{initiative['payback']} years")
                else:
                    st.metric("Payback Period", "N/A")
    
    # Carbon footprint timeline
    st.subheader("📅 Carbon Footprint Timeline")
    
    # Generate monthly carbon data
    months = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=365), 
                          end=datetime.datetime.now(), freq='M')
    
    carbon_timeline = []
    for month in months:
        carbon_timeline.append({
            'Month': month,
            'Total Emissions': 4000 - (month.month * 20) + random.uniform(-200, 200),
            'Scope 1': 1200 - (month.month * 8) + random.uniform(-50, 50),
            'Scope 2': 1800 - (month.month * 7) + random.uniform(-75, 75),
            'Scope 3': 2000 - (month.month * 5) + random.uniform(-100, 100)
        })
    
    df_carbon_timeline = pd.DataFrame(carbon_timeline)
    
    fig_timeline = px.line(df_carbon_timeline, x='Month', y=['Total Emissions', 'Scope 1', 'Scope 2', 'Scope 3'],
                          title="Carbon Emissions Timeline")
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Carbon offset projects
    st.subheader("🌳 Carbon Offset Projects")
    
    offset_projects = [
        {"name": "Forest Conservation Project", "offset": 500, "location": "Amazon Basin", "verification": "Gold Standard"},
        {"name": "Renewable Energy Project", "offset": 300, "location": "Wind Farm Texas", "verification": "VCS"},
        {"name": "Methane Capture Project", "offset": 200, "location": "Landfill California", "verification": "CAR"},
    ]
    
    for project in offset_projects:
        st.info(f"🌍 **{project['name']}** - {project['offset']} tons CO2 offset ({project['location']}) - Verified by {project['verification']}")

def display_waste_management():
    """Display waste management dashboard"""
    st.header("♻️ Waste Management")
    
    # Waste metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_waste = random.randint(500, 1000)
        st.metric("🗑️ Total Waste", f"{total_waste:,} tons", "↓ 50 tons")
    
    with col2:
        waste_diverted = random.uniform(75, 90)
        st.metric("♻️ Waste Diverted", f"{waste_diverted:.1f}%", "↑ 5.2%")
    
    with col3:
        recycling_rate = random.uniform(60, 80)
        st.metric("♻️ Recycling Rate", f"{recycling_rate:.1f}%", "↑ 3.5%")
    
    with col4:
        landfill_waste = total_waste * (1 - waste_diverted/100)
        st.metric("🏭 Landfill Waste", f"{landfill_waste:.0f} tons", "↓ 75 tons")
    
    # Waste breakdown
    st.subheader("📊 Waste Breakdown")
    
    waste_types = {
        'Waste Type': ['Cardboard', 'Plastic', 'Electronics', 'Organic', 'Metal', 'Other'],
        'Amount (tons)': [200, 150, 75, 100, 50, 125],
        'Diversion Rate (%)': [95, 85, 90, 80, 98, 60]
    }
    df_waste = pd.DataFrame(waste_types)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_waste_amount = px.bar(df_waste, x='Waste Type', y='Amount (tons)',
                                 title="Waste Generation by Type")
        st.plotly_chart(fig_waste_amount, use_container_width=True)
    
    with col2:
        fig_diversion = px.bar(df_waste, x='Waste Type', y='Diversion Rate (%)',
                              title="Waste Diversion Rate by Type")
        st.plotly_chart(fig_diversion, use_container_width=True)
    
    # Waste streams
    st.subheader("🔄 Waste Streams")
    
    streams = [
        {"name": "Cardboard Recycling", "volume": 200, "vendor": "RecycleCorp", "revenue": 15000, "status": "✅ Active"},
        {"name": "Plastic Recovery", "volume": 150, "vendor": "PlasticReborn", "revenue": 8000, "status": "✅ Active"},
        {"name": "Electronics Recycling", "volume": 75, "vendor": "TechRecycle", "revenue": 5000, "status": "✅ Active"},
        {"name": "Organic Composting", "volume": 100, "vendor": "GreenCompost", "revenue": 3000, "status": "🔄 Expanding"},
        {"name": "Metal Recovery", "volume": 50, "vendor": "MetalWorks", "revenue": 12000, "status": "✅ Active"}
    ]
    
    for stream in streams:
        with st.expander(f"{stream['name']} - {stream['status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Volume", f"{stream['volume']} tons/month")
            
            with col2:
                st.metric("Monthly Revenue", f"${stream['revenue']:,}")
            
            with col3:
                st.write(f"**Vendor:** {stream['vendor']}")
    
    # Waste reduction initiatives
    st.subheader("🎯 Waste Reduction Initiatives")
    
    initiatives = [
        {"name": "Packaging Optimization", "reduction": 25, "savings": 45000, "status": "✅ Implemented"},
        {"name": "Reusable Containers", "reduction": 30, "savings": 35000, "status": "🔄 Rolling Out"},
        {"name": "Supplier Packaging Standards", "reduction": 20, "savings": 25000, "status": "📋 Planning"},
        {"name": "Digital Documentation", "reduction": 15, "savings": 20000, "status": "✅ Implemented"},
        {"name": "Food Waste Reduction", "reduction": 40, "savings": 50000, "status": "🔄 Pilot Program"}
    ]
    
    for initiative in initiatives:
        st.info(f"🌱 **{initiative['name']}** - {initiative['reduction']}% reduction, ${initiative['savings']:,} savings ({initiative['status']})")
    
    # Waste management timeline
    st.subheader("📅 Waste Management Timeline")
    
    # Generate waste timeline data
    months = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=365), 
                          end=datetime.datetime.now(), freq='M')
    
    waste_timeline = []
    for month in months:
        waste_timeline.append({
            'Month': month,
            'Total Waste': 800 - (month.month * 15) + random.uniform(-50, 50),
            'Recycled': 500 + (month.month * 10) + random.uniform(-30, 30),
            'Composted': 100 + (month.month * 5) + random.uniform(-10, 10),
            'Landfill': 200 - (month.month * 30) + random.uniform(-20, 20)
        })
    
    df_waste_timeline = pd.DataFrame(waste_timeline)
    
    fig_waste_timeline = px.area(df_waste_timeline, x='Month', y=['Recycled', 'Composted', 'Landfill'],
                                title="Waste Management Timeline")
    st.plotly_chart(fig_waste_timeline, use_container_width=True)

def display_energy_usage():
    """Display energy usage dashboard"""
    st.header("⚡ Energy Usage & Efficiency")
    
    # Energy metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_energy = random.randint(5000, 8000)
        st.metric("⚡ Total Energy", f"{total_energy:,} MWh", "↓ 450 MWh")
    
    with col2:
        renewable_pct = random.uniform(30, 50)
        st.metric("🌞 Renewable Energy", f"{renewable_pct:.1f}%", "↑ 8.2%")
    
    with col3:
        energy_intensity = random.uniform(0.3, 0.7)
        st.metric("📊 Energy Intensity", f"{energy_intensity:.2f} MWh/unit", "↓ 0.05")
    
    with col4:
        energy_savings = random.randint(500, 1000)
        st.metric("💰 Energy Savings", f"${energy_savings:,}K", "↑ $125K")
    
    # Energy consumption by source
    st.subheader("🔌 Energy Consumption by Source")
    
    energy_sources = {
        'Source': ['Grid Electricity', 'Solar', 'Wind', 'Natural Gas', 'Other'],
        'Consumption (MWh)': [3500, 1200, 800, 600, 400],
        'Cost ($)': [350000, 60000, 40000, 45000, 30000]
    }
    df_energy = pd.DataFrame(energy_sources)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_energy_consumption = px.pie(df_energy, values='Consumption (MWh)', names='Source',
                                       title="Energy Consumption by Source")
        st.plotly_chart(fig_energy_consumption, use_container_width=True)
    
    with col2:
        fig_energy_cost = px.bar(df_energy, x='Source', y='Cost ($)',
                                title="Energy Cost by Source")
        st.plotly_chart(fig_energy_cost, use_container_width=True)
    
    # Energy efficiency projects
    st.subheader("🎯 Energy Efficiency Projects")
    
    projects = [
        {"name": "LED Lighting Retrofit", "savings": 500, "investment": 150000, "roi": 3.2, "status": "✅ Complete"},
        {"name": "HVAC System Upgrade", "savings": 300, "investment": 200000, "roi": 4.5, "status": "🔄 In Progress"},
        {"name": "Building Automation", "savings": 200, "investment": 100000, "roi": 2.8, "status": "📋 Planned"},
        {"name": "Motor Efficiency Upgrade", "savings": 150, "investment": 75000, "roi": 2.1, "status": "✅ Complete"},
        {"name": "Energy Recovery System", "savings": 250, "investment": 125000, "roi": 3.5, "status": "🔄 Design Phase"}
    ]
    
    for project in projects:
        with st.expander(f"{project['name']} - {project['status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Annual Savings", f"{project['savings']} MWh")
            
            with col2:
                st.metric("Investment", f"${project['investment']:,}")
            
            with col3:
                st.metric("ROI", f"{project['roi']} years")
    
    # Energy usage patterns
    st.subheader("📈 Energy Usage Patterns")
    
    # Generate hourly energy usage
    hours = list(range(24))
    energy_usage = []
    
    for hour in hours:
        # Simulate typical usage pattern
        if 6 <= hour <= 18:  # Business hours
            usage = 400 + 100 * np.sin((hour - 6) * np.pi / 12) + random.uniform(-20, 20)
        else:  # Off hours
            usage = 200 + random.uniform(-30, 30)
        energy_usage.append(usage)
    
    fig_hourly = px.line(x=hours, y=energy_usage, title="Hourly Energy Usage Pattern")
    fig_hourly.update_layout(xaxis_title="Hour of Day", yaxis_title="Energy Usage (kWh)")
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Energy benchmarking
    st.subheader("📊 Energy Benchmarking")
    
    benchmark_data = {
        'Facility': ['Dallas DC', 'Chicago Hub', 'Atlanta Hub', 'Austin Specialty', 'Industry Average'],
        'Energy Intensity (kWh/sqft)': [12.5, 14.2, 11.8, 13.9, 15.5],
        'Energy Cost ($/sqft)': [1.85, 2.10, 1.75, 2.05, 2.30]
    }
    df_benchmark = pd.DataFrame(benchmark_data)
    
    fig_benchmark = px.bar(df_benchmark, x='Facility', y='Energy Intensity (kWh/sqft)',
                          title="Energy Intensity Benchmarking")
    st.plotly_chart(fig_benchmark, use_container_width=True)
    
    # Renewable energy tracking
    st.subheader("🌞 Renewable Energy Tracking")
    
    # Generate renewable energy data
    months = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=365), 
                          end=datetime.datetime.now(), freq='M')
    
    renewable_data = []
    for month in months:
        renewable_data.append({
            'Month': month,
            'Solar Generation': 100 + 50 * np.sin((month.month - 6) * np.pi / 6) + random.uniform(-10, 10),
            'Wind Generation': 80 + 30 * np.sin((month.month - 3) * np.pi / 6) + random.uniform(-15, 15),
            'Total Renewable': 0  # Will be calculated
        })
    
    df_renewable = pd.DataFrame(renewable_data)
    df_renewable['Total Renewable'] = df_renewable['Solar Generation'] + df_renewable['Wind Generation']
    
    fig_renewable = px.line(df_renewable, x='Month', y=['Solar Generation', 'Wind Generation', 'Total Renewable'],
                           title="Renewable Energy Generation")
    st.plotly_chart(fig_renewable, use_container_width=True)

def display_green_logistics():
    """Display green logistics dashboard"""
    st.header("🚛 Green Logistics & Transportation")
    
    # Green logistics metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fleet_efficiency = random.uniform(15, 25)
        st.metric("🚛 Fleet Efficiency", f"{fleet_efficiency:.1f} MPG", "↑ 2.3 MPG")
    
    with col2:
        electric_vehicles = random.randint(20, 40)
        st.metric("⚡ Electric Vehicles", f"{electric_vehicles}%", "↑ 8%")
    
    with col3:
        route_optimization = random.uniform(10, 25)
        st.metric("🗺️ Route Optimization", f"{route_optimization:.1f}%", "↑ 3.2%")
    
    with col4:
        delivery_emissions = random.uniform(0.2, 0.5)
        st.metric("💨 Delivery Emissions", f"{delivery_emissions:.2f} kg CO2/mile", "↓ 0.05 kg")
    
    # Fleet composition
    st.subheader("🚗 Fleet Composition")
    
    fleet_data = {
        'Vehicle Type': ['Diesel Trucks', 'Electric Trucks', 'Hybrid Vans', 'Electric Vans', 'Conventional Vans'],
        'Count': [120, 30, 45, 25, 80],
        'Efficiency (MPG)': [8.5, 0, 22, 0, 18],  # 0 for electric (measured differently)
        'CO2 Emissions (g/mile)': [1200, 0, 400, 0, 600]
    }
    df_fleet = pd.DataFrame(fleet_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_fleet_count = px.pie(df_fleet, values='Count', names='Vehicle Type',
                                title="Fleet Composition by Vehicle Type")
        st.plotly_chart(fig_fleet_count, use_container_width=True)
    
    with col2:
        # Filter out electric vehicles for MPG chart
        df_fleet_mpg = df_fleet[df_fleet['Efficiency (MPG)'] > 0]
        fig_fleet_efficiency = px.bar(df_fleet_mpg, x='Vehicle Type', y='Efficiency (MPG)',
                                     title="Fleet Fuel Efficiency")
        st.plotly_chart(fig_fleet_efficiency, use_container_width=True)
    
    # Green logistics initiatives
    st.subheader("🌱 Green Logistics Initiatives")
    
    initiatives = [
        {"name": "Electric Vehicle Deployment", "impact": "30% reduction in delivery emissions", "investment": 2000000, "status": "🔄 Expanding"},
        {"name": "Route Optimization AI", "impact": "15% reduction in miles driven", "investment": 500000, "status": "✅ Implemented"},
        {"name": "Consolidated Shipping", "impact": "20% reduction in shipments", "investment": 300000, "status": "✅ Implemented"},
        {"name": "Alternative Fuel Vehicles", "impact": "25% reduction in fuel consumption", "investment": 1500000, "status": "📋 Planning"},
        {"name": "Last-Mile Optimization", "impact": "10% reduction in delivery time", "investment": 750000, "status": "🔄 Pilot Program"}
    ]
    
    for initiative in initiatives:
        with st.expander(f"{initiative['name']} - {initiative['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Impact:** {initiative['impact']}")
            
            with col2:
                st.write(f"**Investment:** ${initiative['investment']:,}")
    
    # Transportation emissions
    st.subheader("💨 Transportation Emissions")
    
    # Generate transportation emissions data
    months = pd.date_range(start=datetime.datetime.now() - datetime.timedelta(days=365), 
                          end=datetime.datetime.now(), freq='M')
    
    transport_emissions = []
    for month in months:
        transport_emissions.append({
            'Month': month,
            'Diesel Fleet': 800 - (month.month * 20) + random.uniform(-50, 50),
            'Electric Fleet': 0 + (month.month * 5) + random.uniform(-5, 5),
            'Third-Party Carriers': 600 - (month.month * 10) + random.uniform(-30, 30)
        })
    
    df_transport = pd.DataFrame(transport_emissions)
    
    fig_transport = px.line(df_transport, x='Month', y=['Diesel Fleet', 'Electric Fleet', 'Third-Party Carriers'],
                           title="Transportation Emissions Timeline")
    st.plotly_chart(fig_transport, use_container_width=True)
    
    # Delivery performance
    st.subheader("📦 Sustainable Delivery Performance")
    
    delivery_metrics = {
        'Metric': ['On-Time Delivery', 'Delivery Efficiency', 'Customer Satisfaction', 'Cost per Delivery'],
        'Current': [95.2, 87.5, 4.6, 8.50],
        'Target': [96.0, 90.0, 4.8, 8.00],
        'Unit': ['%', '%', '/5', '$']
    }
    
    for i, metric in enumerate(delivery_metrics['Metric']):
        current = delivery_metrics['Current'][i]
        target = delivery_metrics['Target'][i]
        unit = delivery_metrics['Unit'][i]
        
        st.write(f"**{metric}**")
        progress = current / target if target > 0 else 1
        st.progress(min(progress, 1.0))
        st.write(f"Current: {current}{unit} | Target: {target}{unit}")
        st.write("---")

def display_esg_reporting():
    """Display ESG reporting dashboard"""
    st.header("📊 ESG Reporting & Compliance")
    
    # ESG score overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        esg_score = random.randint(75, 95)
        st.metric("🌍 ESG Score", f"{esg_score}/100", "↑ 3")
    
    with col2:
        environmental_score = random.randint(80, 95)
        st.metric("🌱 Environmental", f"{environmental_score}/100", "↑ 5")
    
    with col3:
        social_score = random.randint(75, 90)
        st.metric("👥 Social", f"{social_score}/100", "↑ 2")
    
    with col4:
        governance_score = random.randint(85, 95)
        st.metric("🏛️ Governance", f"{governance_score}/100", "↑ 1")
    
    # ESG framework compliance
    st.subheader("📋 ESG Framework Compliance")
    
    frameworks = [
        {"name": "GRI Standards", "compliance": 92, "last_report": "Q3 2024", "status": "✅ Compliant"},
        {"name": "SASB Standards", "compliance": 88, "last_report": "Q3 2024", "status": "✅ Compliant"},
        {"name": "TCFD Recommendations", "compliance": 85, "last_report": "Annual 2024", "status": "✅ Compliant"},
        {"name": "UN Global Compact", "compliance": 90, "last_report": "Annual 2024", "status": "✅ Compliant"},
        {"name": "CDP Climate Change", "compliance": 87, "last_report": "Annual 2024", "status": "✅ Compliant"}
    ]
    
    framework_df = pd.DataFrame(frameworks)
    
    fig_compliance = px.bar(framework_df, x='name', y='compliance',
                           title="ESG Framework Compliance Scores")
    st.plotly_chart(fig_compliance, use_container_width=True)
    
    # ESG metrics summary
    st.subheader("📊 ESG Metrics Summary")
    
    # Environmental metrics
    with st.expander("🌱 Environmental Metrics"):
        env_metrics = {
            'Metric': ['Carbon Emissions', 'Water Usage', 'Waste Diverted', 'Energy Efficiency', 'Renewable Energy'],
            'Current': [4500, 125000, 78, 32, 42],
            'Target': [3500, 100000, 85, 40, 50],
            'Unit': ['tons CO2', 'gallons', '%', '%', '%']
        }
        
        env_df = pd.DataFrame(env_metrics)
        st.dataframe(env_df, use_container_width=True)
    
    # Social metrics
    with st.expander("👥 Social Metrics"):
        social_metrics = {
            'Metric': ['Employee Satisfaction', 'Safety Incidents', 'Training Hours', 'Diversity Index', 'Community Investment'],
            'Current': [4.2, 12, 45000, 0.85, 250000],
            'Target': [4.5, 8, 50000, 0.90, 300000],
            'Unit': ['/5', 'incidents', 'hours', 'index', '$']
        }
        
        social_df = pd.DataFrame(social_metrics)
        st.dataframe(social_df, use_container_width=True)
    
    # Governance metrics
    with st.expander("🏛️ Governance Metrics"):
        governance_metrics = {
            'Metric': ['Board Independence', 'Ethics Training', 'Compliance Score', 'Audit Frequency', 'Transparency Index'],
            'Current': [75, 98, 92, 4, 88],
            'Target': [80, 100, 95, 4, 90],
            'Unit': ['%', '%', '%', 'times/year', '%']
        }
        
        governance_df = pd.DataFrame(governance_metrics)
        st.dataframe(governance_df, use_container_width=True)
    
    # ESG reporting calendar
    st.subheader("📅 ESG Reporting Calendar")
    
    reports = [
        {"report": "Quarterly ESG Report", "due_date": "2024-01-15", "status": "✅ Submitted"},
        {"report": "Annual Sustainability Report", "due_date": "2024-03-31", "status": "🔄 In Progress"},
        {"report": "CDP Climate Disclosure", "due_date": "2024-07-31", "status": "📋 Planned"},
        {"report": "GRI Standards Report", "due_date": "2024-06-30", "status": "📋 Planned"},
        {"report": "SASB Report", "due_date": "2024-08-15", "status": "📋 Planned"}
    ]
    
    for report in reports:
        st.write(f"**{report['report']}** - Due: {report['due_date']} - Status: {report['status']}")
    
    # ESG performance trends
    st.subheader("📈 ESG Performance Trends")
    
    # Generate ESG trend data
    quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    
    esg_trends = []
    for i, quarter in enumerate(quarters):
        esg_trends.append({
            'Quarter': quarter,
            'Environmental': 75 + i * 2 + random.uniform(-2, 2),
            'Social': 78 + i * 1.5 + random.uniform(-2, 2),
            'Governance': 85 + i * 1 + random.uniform(-2, 2),
            'Overall ESG': 79 + i * 1.8 + random.uniform(-2, 2)
        })
    
    df_esg_trends = pd.DataFrame(esg_trends)
    
    fig_esg_trends = px.line(df_esg_trends, x='Quarter', y=['Environmental', 'Social', 'Governance', 'Overall ESG'],
                            title="ESG Performance Trends")
    st.plotly_chart(fig_esg_trends, use_container_width=True)
    
    # ESG risk assessment
    st.subheader("⚠️ ESG Risk Assessment")
    
    risks = [
        {"category": "Climate Change", "risk_level": "Medium", "impact": "High", "mitigation": "Carbon reduction initiatives"},
        {"category": "Water Scarcity", "risk_level": "Low", "impact": "Medium", "mitigation": "Water conservation programs"},
        {"category": "Supply Chain", "risk_level": "Medium", "impact": "High", "mitigation": "Supplier sustainability audits"},
        {"category": "Regulatory", "risk_level": "Low", "impact": "Medium", "mitigation": "Compliance monitoring"},
        {"category": "Reputation", "risk_level": "Low", "impact": "High", "mitigation": "Transparent reporting"}
    ]
    
    for risk in risks:
        risk_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(risk['risk_level'], "🔵")
        st.write(f"{risk_color} **{risk['category']}** - Risk: {risk['risk_level']}, Impact: {risk['impact']}")
        st.write(f"   Mitigation: {risk['mitigation']}")
    
    # Generate ESG report
    st.subheader("📄 Generate ESG Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Quarterly Report"):
            st.success("Quarterly ESG report generated!")
    
    with col2:
        if st.button("📋 Annual Report"):
            st.success("Annual ESG report generated!")
    
    with col3:
        if st.button("📈 Custom Report"):
            st.success("Custom ESG report generated!")
    
    # ESG data export
    st.subheader("📤 ESG Data Export")
    
    export_options = ["CSV", "Excel", "PDF", "JSON"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox("Select Export Format", export_options)
    
    with col2:
        if st.button("📤 Export Data"):
            st.success(f"ESG data exported in {export_format} format!")
