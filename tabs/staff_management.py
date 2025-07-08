import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta, time
import json
from utils.api import get_data
from utils.helpers import show_notification

def app():
    st.header("👥 Staff Management & Scheduling")
    st.markdown("**Comprehensive staff management, scheduling, and performance tracking**")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Staff Directory", 
        "📅 Scheduling", 
        "📊 Performance", 
        "🎯 Training",
        "💰 Payroll"
    ])
    
    with tab1:
        display_staff_directory()
    
    with tab2:
        display_scheduling()
    
    with tab3:
        display_performance()
    
    with tab4:
        display_training()
    
    with tab5:
        display_payroll()

def display_staff_directory():
    st.subheader("👥 Staff Directory")
    
    # Generate mock staff data
    staff_data = generate_staff_data()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Staff search and filters
        st.markdown("### 🔍 Search & Filter")
        
        search_col1, search_col2, search_col3 = st.columns(3)
        
        with search_col1:
            search_term = st.text_input("Search by name or ID", placeholder="Enter name or employee ID")
        
        with search_col2:
            department_filter = st.selectbox(
                "Filter by Department",
                ["All", "Warehouse", "Delivery", "Customer Service", "IT", "Management"]
            )
        
        with search_col3:
            role_filter = st.selectbox(
                "Filter by Role",
                ["All", "Manager", "Supervisor", "Associate", "Driver", "Specialist"]
            )
        
        # Apply filters
        filtered_staff = staff_data.copy()
        
        if search_term:
            filtered_staff = filtered_staff[
                filtered_staff['Name'].str.contains(search_term, case=False, na=False) |
                filtered_staff['Employee_ID'].str.contains(search_term, case=False, na=False)
            ]
        
        if department_filter != "All":
            filtered_staff = filtered_staff[filtered_staff['Department'] == department_filter]
        
        if role_filter != "All":
            filtered_staff = filtered_staff[filtered_staff['Role'] == role_filter]
        
        # Staff table
        st.markdown("### 📋 Staff List")
        
        # Add action buttons
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            if st.button("➕ Add New Employee"):
                st.session_state['show_add_employee'] = True
        
        with action_col2:
            if st.button("📤 Export Staff Data"):
                csv_data = filtered_staff.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"staff_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with action_col3:
            if st.button("📊 Generate Report", key="staff_directory_report"):
                st.info("Staff report generated successfully!")
        
        # Display staff table with enhanced formatting
        st.dataframe(
            filtered_staff.style.apply(highlight_performance, axis=1),
            use_container_width=True,
            column_config={
                "Performance_Score": st.column_config.ProgressColumn(
                    "Performance",
                    help="Employee performance score",
                    min_value=0,
                    max_value=100
                ),
                "Salary": st.column_config.NumberColumn(
                    "Salary",
                    help="Annual salary",
                    min_value=0,
                    max_value=200000,
                    step=1000,
                    format="$%.0f"
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Employment status"
                )
            }
        )
    
    with col2:
        # Staff statistics
        st.markdown("### 📊 Staff Statistics")
        
        total_staff = len(staff_data)
        active_staff = len(staff_data[staff_data['Status'] == 'Active'])
        avg_performance = staff_data['Performance_Score'].mean()
        
        st.metric("Total Staff", total_staff)
        st.metric("Active Staff", active_staff, delta=f"{active_staff - total_staff + active_staff}")
        st.metric("Avg Performance", f"{avg_performance:.1f}%", delta="2.3%")
        
        # Department distribution
        st.markdown("### 🏢 Department Distribution")
        
        dept_counts = staff_data['Department'].value_counts()
        fig = px.pie(
            values=dept_counts.values,
            names=dept_counts.index,
            title="Staff by Department"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent activities
        st.markdown("### 📱 Recent Activities")
        
        activities = [
            {"time": "2 hours ago", "action": "New hire: John Smith", "type": "hire"},
            {"time": "1 day ago", "action": "Performance review: Jane Doe", "type": "review"},
            {"time": "2 days ago", "action": "Training completed: Safety Course", "type": "training"},
            {"time": "3 days ago", "action": "Promotion: Mike Johnson to Supervisor", "type": "promotion"}
        ]
        
        for activity in activities:
            icon = "🆕" if activity["type"] == "hire" else "📊" if activity["type"] == "review" else "🎓" if activity["type"] == "training" else "⬆️"
            st.markdown(f"{icon} {activity['action']}")
            st.markdown(f"<small>{activity['time']}</small>", unsafe_allow_html=True)
    
    # Add Employee Modal
    if st.session_state.get('show_add_employee', False):
        display_add_employee_form()

def display_scheduling():
    st.subheader("📅 Staff Scheduling")
    
    # Scheduling interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Calendar view
        st.markdown("### 📅 Weekly Schedule")
        
        # Date selection
        selected_date = st.date_input("Select Week Starting", value=datetime.now())
        
        # Generate schedule data
        schedule_data = generate_schedule_data(selected_date)
        
        # Display schedule as a table
        st.dataframe(schedule_data, use_container_width=True)
        
        # Shift management
        st.markdown("### ⏰ Shift Management")
        
        shift_col1, shift_col2, shift_col3 = st.columns(3)
        
        with shift_col1:
            if st.button("➕ Add Shift"):
                st.session_state['show_add_shift'] = True
        
        with shift_col2:
            if st.button("🔄 Auto-Schedule"):
                with st.spinner("Optimizing schedule..."):
                    import time
                    time.sleep(2)
                    st.success("Schedule optimized successfully!")
        
        with shift_col3:
            if st.button("📧 Send Notifications"):
                st.success("Schedule notifications sent to all staff!")
        
        # Availability management
        st.markdown("### 🗓️ Staff Availability")
        
        availability_data = pd.DataFrame({
            'Employee': ['John Smith', 'Jane Doe', 'Mike Johnson', 'Sarah Wilson', 'Bob Brown'],
            'Monday': ['Available', 'Available', 'Available', 'Not Available', 'Available'],
            'Tuesday': ['Available', 'Available', 'Available', 'Available', 'Not Available'],
            'Wednesday': ['Available', 'Not Available', 'Available', 'Available', 'Available'],
            'Thursday': ['Available', 'Available', 'Not Available', 'Available', 'Available'],
            'Friday': ['Available', 'Available', 'Available', 'Available', 'Available'],
            'Saturday': ['Not Available', 'Available', 'Available', 'Not Available', 'Available'],
            'Sunday': ['Not Available', 'Not Available', 'Available', 'Available', 'Not Available']
        })
        
        st.dataframe(availability_data, use_container_width=True)
    
    with col2:
        # Scheduling statistics
        st.markdown("### 📊 Scheduling Stats")
        
        st.metric("Total Shifts", "156", delta="8")
        st.metric("Coverage Rate", "98.7%", delta="1.2%")
        st.metric("Overtime Hours", "32", delta="-5")
        st.metric("Staff Utilization", "87%", delta="3%")
        
        # Shift distribution
        st.markdown("### 📈 Shift Distribution")
        
        shift_data = pd.DataFrame({
            'Shift': ['Morning', 'Afternoon', 'Evening', 'Night'],
            'Count': [45, 52, 38, 21]
        })
        
        fig = px.bar(
            shift_data,
            x='Shift',
            y='Count',
            title="Shifts by Time",
            color='Count',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Alerts and notifications
        st.markdown("### 🚨 Alerts")
        
        alerts = [
            {"type": "warning", "message": "Understaffed on Saturday evening"},
            {"type": "info", "message": "3 overtime approvals pending"},
            {"type": "success", "message": "100% coverage achieved for next week"}
        ]
        
        for alert in alerts:
            alert_color = "yellow" if alert["type"] == "warning" else "blue" if alert["type"] == "info" else "green"
            st.markdown(f"""
            <div style="padding: 10px; border-left: 4px solid {alert_color}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                {alert['message']}
            </div>
            """, unsafe_allow_html=True)

def display_performance():
    st.subheader("📊 Performance Management")
    
    # Performance dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Performance metrics
        st.markdown("### 📈 Performance Metrics")
        
        # Employee selector
        staff_data = generate_staff_data()
        selected_employee = st.selectbox(
            "Select Employee",
            staff_data['Name'].tolist()
        )
        
        employee_data = staff_data[staff_data['Name'] == selected_employee].iloc[0]
        
        # Performance overview
        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        
        with perf_col1:
            st.metric("Overall Score", f"{employee_data['Performance_Score']:.1f}%", delta="2.3%")
        
        with perf_col2:
            st.metric("Productivity", f"{np.random.uniform(85, 95):.1f}%", delta="1.8%")
        
        with perf_col3:
            st.metric("Quality", f"{np.random.uniform(90, 98):.1f}%", delta="0.5%")
        
        with perf_col4:
            st.metric("Attendance", f"{np.random.uniform(95, 100):.1f}%", delta="-0.2%")
        
        # Performance trends
        st.markdown("### 📊 Performance Trends")
        
        # Generate performance trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=90), periods=90, freq='D')
        performance_trend = pd.DataFrame({
            'Date': dates,
            'Performance': np.random.normal(employee_data['Performance_Score'], 5, 90),
            'Productivity': np.random.normal(90, 3, 90),
            'Quality': np.random.normal(94, 2, 90)
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=performance_trend['Date'],
            y=performance_trend['Performance'],
            name='Overall Performance',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=performance_trend['Date'],
            y=performance_trend['Productivity'],
            name='Productivity',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=performance_trend['Date'],
            y=performance_trend['Quality'],
            name='Quality',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title=f"Performance Trends - {selected_employee}",
            xaxis_title="Date",
            yaxis_title="Score (%)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Goals and objectives
        st.markdown("### 🎯 Goals & Objectives")
        
        goals_data = pd.DataFrame({
            'Goal': ['Increase Productivity', 'Reduce Errors', 'Complete Training', 'Improve Customer Satisfaction'],
            'Target': ['95%', '< 2%', '100%', '4.8/5'],
            'Current': ['92%', '2.3%', '80%', '4.6/5'],
            'Progress': [92, 77, 80, 96],
            'Status': ['On Track', 'Needs Attention', 'Behind', 'Excellent']
        })
        
        st.dataframe(
            goals_data,
            use_container_width=True,
            column_config={
                "Progress": st.column_config.ProgressColumn(
                    "Progress",
                    help="Goal completion progress",
                    min_value=0,
                    max_value=100
                )
            }
        )
    
    with col2:
        # Performance actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📝 Schedule Review"):
            st.info("Performance review scheduled!")
        
        if st.button("🎯 Set Goals"):
            st.info("Goal setting session scheduled!")
        
        if st.button("📊 Generate Report", key="performance_report"):
            st.info("Performance report generated!")
        
        if st.button("🏆 Recognition"):
            st.info("Recognition sent to employee!")
        
        # Performance distribution
        st.markdown("### 📊 Team Performance")
        
        performance_dist = staff_data['Performance_Score'].value_counts(bins=5)
        fig = px.histogram(
            staff_data,
            x='Performance_Score',
            nbins=10,
            title="Performance Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top performers
        st.markdown("### 🏆 Top Performers")
        
        top_performers = staff_data.nlargest(5, 'Performance_Score')[['Name', 'Performance_Score', 'Department']]
        
        for idx, performer in top_performers.iterrows():
            st.markdown(f"""
            <div style="padding: 10px; background-color: rgba(255,215,0,0.1); margin: 5px 0; border-radius: 5px;">
                <strong>{performer['Name']}</strong><br>
                {performer['Department']} - {performer['Performance_Score']:.1f}%
            </div>
            """, unsafe_allow_html=True)

def display_training():
    st.subheader("🎓 Training & Development")
    
    # Training dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Training programs
        st.markdown("### 📚 Training Programs")
        
        programs_data = pd.DataFrame({
            'Program': ['Safety Training', 'Customer Service Excellence', 'Leadership Development', 'Technical Skills', 'Compliance Training'],
            'Duration': ['2 days', '3 days', '5 days', '4 days', '1 day'],
            'Enrolled': [25, 18, 12, 15, 30],
            'Completed': [20, 15, 8, 12, 28],
            'Completion_Rate': [80, 83, 67, 80, 93],
            'Status': ['Active', 'Active', 'Active', 'Active', 'Active']
        })
        
        st.dataframe(
            programs_data,
            use_container_width=True,
            column_config={
                "Completion_Rate": st.column_config.ProgressColumn(
                    "Completion Rate",
                    help="Training completion rate",
                    min_value=0,
                    max_value=100
                )
            }
        )
        
        # Training calendar
        st.markdown("### 📅 Training Calendar")
        
        training_schedule = pd.DataFrame({
            'Date': pd.date_range(start=datetime.now(), periods=10, freq='D'),
            'Training': ['Safety Training', 'Customer Service', 'Leadership', 'Technical Skills', 'Compliance',
                        'Safety Training', 'Customer Service', 'Leadership', 'Technical Skills', 'Compliance'],
            'Instructor': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson', 'Bob Brown',
                          'John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson', 'Bob Brown'],
            'Participants': [8, 12, 6, 10, 15, 9, 11, 7, 8, 12]
        })
        
        st.dataframe(training_schedule, use_container_width=True)
        
        # Skills matrix
        st.markdown("### 🔧 Skills Matrix")
        
        skills_data = pd.DataFrame({
            'Employee': ['John Smith', 'Jane Doe', 'Mike Johnson', 'Sarah Wilson', 'Bob Brown'],
            'Warehouse Operations': [85, 92, 78, 95, 88],
            'Customer Service': [90, 95, 85, 92, 80],
            'Leadership': [70, 88, 92, 85, 75],
            'Technical Skills': [88, 75, 95, 82, 90],
            'Safety Compliance': [95, 90, 88, 92, 85]
        })
        
        # Create heatmap
        skills_matrix = skills_data.set_index('Employee')
        fig = px.imshow(
            skills_matrix.T,
            labels=dict(x="Employee", y="Skills", color="Proficiency"),
            x=skills_matrix.index,
            y=skills_matrix.columns,
            color_continuous_scale="RdYlGn",
            aspect="auto"
        )
        fig.update_layout(title="Skills Proficiency Matrix")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Training statistics
        st.markdown("### 📊 Training Stats")
        
        st.metric("Active Programs", "5", delta="1")
        st.metric("Total Enrolled", "100", delta="12")
        st.metric("Completion Rate", "82%", delta="5%")
        st.metric("Avg Rating", "4.6/5", delta="0.2")
        
        # Training budget
        st.markdown("### 💰 Training Budget")
        
        budget_data = pd.DataFrame({
            'Category': ['Programs', 'Materials', 'Instructors', 'Facilities'],
            'Budget': [50000, 15000, 30000, 10000],
            'Spent': [35000, 12000, 25000, 8000],
            'Remaining': [15000, 3000, 5000, 2000]
        })
        
        fig = px.bar(
            budget_data,
            x='Category',
            y=['Budget', 'Spent', 'Remaining'],
            title="Training Budget Overview",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Upcoming deadlines
        st.markdown("### ⏰ Upcoming Deadlines")
        
        deadlines = [
            {"training": "Safety Certification", "deadline": "Dec 15", "employees": 8},
            {"training": "Customer Service", "deadline": "Dec 20", "employees": 12},
            {"training": "Leadership Program", "deadline": "Jan 5", "employees": 6}
        ]
        
        for deadline in deadlines:
            st.markdown(f"""
            <div style="padding: 10px; border-left: 4px solid orange; background-color: rgba(255,165,0,0.1); margin: 5px 0;">
                <strong>{deadline['training']}</strong><br>
                Due: {deadline['deadline']} ({deadline['employees']} employees)
            </div>
            """, unsafe_allow_html=True)

def display_payroll():
    st.subheader("💰 Payroll Management")
    
    # Payroll dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Payroll summary
        st.markdown("### 💵 Payroll Summary")
        
        payroll_data = generate_payroll_data()
        
        # Payroll overview
        payroll_col1, payroll_col2, payroll_col3, payroll_col4 = st.columns(4)
        
        with payroll_col1:
            total_payroll = payroll_data['Gross_Pay'].sum()
            st.metric("Total Payroll", f"${total_payroll:,.2f}", delta="3.2%")
        
        with payroll_col2:
            avg_salary = payroll_data['Gross_Pay'].mean()
            st.metric("Average Salary", f"${avg_salary:,.2f}", delta="1.8%")
        
        with payroll_col3:
            overtime_total = payroll_data['Overtime_Pay'].sum()
            st.metric("Overtime Pay", f"${overtime_total:,.2f}", delta="-5.2%")
        
        with payroll_col4:
            benefits_total = payroll_data['Benefits'].sum()
            st.metric("Benefits Cost", f"${benefits_total:,.2f}", delta="2.1%")
        
        # Payroll table
        st.markdown("### 📋 Payroll Details")
        
        st.dataframe(
            payroll_data,
            use_container_width=True,
            column_config={
                "Gross_Pay": st.column_config.NumberColumn(
                    "Gross Pay",
                    help="Gross monthly pay",
                    min_value=0,
                    max_value=50000,
                    step=100,
                    format="$%.2f"
                ),
                "Net_Pay": st.column_config.NumberColumn(
                    "Net Pay",
                    help="Net monthly pay",
                    min_value=0,
                    max_value=50000,
                    step=100,
                    format="$%.2f"
                )
            }
        )
        
        # Payroll trends
        st.markdown("### 📈 Payroll Trends")
        
        # Generate payroll trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), periods=12, freq='M')
        trend_data = pd.DataFrame({
            'Month': dates,
            'Total_Payroll': np.random.normal(total_payroll, total_payroll * 0.1, 12),
            'Overtime': np.random.normal(overtime_total, overtime_total * 0.2, 12),
            'Benefits': np.random.normal(benefits_total, benefits_total * 0.05, 12)
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_data['Month'],
            y=trend_data['Total_Payroll'],
            name='Total Payroll',
            line=dict(color='blue', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_data['Month'],
            y=trend_data['Overtime'],
            name='Overtime',
            line=dict(color='red', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_data['Month'],
            y=trend_data['Benefits'],
            name='Benefits',
            line=dict(color='green', width=2)
        ))
        
        fig.update_layout(
            title="Payroll Trends (Last 12 Months)",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Payroll actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Process Payroll"):
            with st.spinner("Processing payroll..."):
                import time
                time.sleep(2)
                st.success("Payroll processed successfully!")
        
        if st.button("📊 Generate Reports"):
            st.info("Payroll reports generated!")
        
        if st.button("📧 Send Pay Stubs"):
            st.success("Pay stubs sent to all employees!")
        
        if st.button("💾 Export Data"):
            csv_data = payroll_data.to_csv(index=False)
            st.download_button(
                label="Download Payroll CSV",
                data=csv_data,
                file_name=f"payroll_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Department costs
        st.markdown("### 🏢 Department Costs")
        
        dept_costs = payroll_data.groupby('Department')['Gross_Pay'].sum().sort_values(ascending=False)
        
        fig = px.pie(
            values=dept_costs.values,
            names=dept_costs.index,
            title="Payroll by Department"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tax and deductions
        st.markdown("### 💸 Tax & Deductions")
        
        tax_data = {
            "Federal Tax": payroll_data['Federal_Tax'].sum(),
            "State Tax": payroll_data['State_Tax'].sum(),
            "Social Security": payroll_data['Social_Security'].sum(),
            "Medicare": payroll_data['Medicare'].sum(),
            "Other Deductions": payroll_data['Other_Deductions'].sum()
        }
        
        for tax_type, amount in tax_data.items():
            st.metric(tax_type, f"${amount:,.2f}")

# Helper functions
def generate_staff_data():
    """Generate mock staff data"""
    np.random.seed(42)  # For consistent data
    
    departments = ['Warehouse', 'Delivery', 'Customer Service', 'IT', 'Management']
    roles = ['Manager', 'Supervisor', 'Associate', 'Driver', 'Specialist']
    statuses = ['Active', 'On Leave', 'Training']
    
    staff_data = []
    for i in range(50):
        staff_data.append({
            'Employee_ID': f'EMP{1000 + i}',
            'Name': f'Employee {i+1}',
            'Department': np.random.choice(departments),
            'Role': np.random.choice(roles),
            'Hire_Date': datetime.now() - timedelta(days=np.random.randint(30, 2000)),
            'Status': np.random.choice(statuses, p=[0.85, 0.10, 0.05]),
            'Performance_Score': np.random.uniform(70, 100),
            'Salary': np.random.randint(35000, 120000),
            'Email': f'employee{i+1}@walmart.com',
            'Phone': f'555-{np.random.randint(1000, 9999)}',
            'Manager': f'Manager {np.random.randint(1, 10)}'
        })
    
    return pd.DataFrame(staff_data)

def generate_schedule_data(start_date):
    """Generate mock schedule data"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    shifts = ['Morning (6-14)', 'Afternoon (14-22)', 'Night (22-6)']
    
    schedule_data = []
    for day in days:
        for shift in shifts:
            schedule_data.append({
                'Day': day,
                'Shift': shift,
                'Required_Staff': np.random.randint(5, 15),
                'Assigned_Staff': np.random.randint(4, 16),
                'Status': 'Fully Staffed' if np.random.random() > 0.2 else 'Understaffed'
            })
    
    return pd.DataFrame(schedule_data)

def generate_payroll_data():
    """Generate mock payroll data"""
    staff_data = generate_staff_data()
    
    payroll_data = []
    for _, employee in staff_data.iterrows():
        gross_pay = employee['Salary'] / 12  # Monthly salary
        overtime_pay = np.random.uniform(0, gross_pay * 0.2)
        
        # Calculate deductions
        federal_tax = gross_pay * 0.12
        state_tax = gross_pay * 0.05
        social_security = gross_pay * 0.062
        medicare = gross_pay * 0.0145
        benefits = gross_pay * 0.08
        other_deductions = gross_pay * 0.02
        
        total_deductions = federal_tax + state_tax + social_security + medicare + benefits + other_deductions
        net_pay = gross_pay + overtime_pay - total_deductions
        
        payroll_data.append({
            'Employee_ID': employee['Employee_ID'],
            'Name': employee['Name'],
            'Department': employee['Department'],
            'Gross_Pay': gross_pay,
            'Overtime_Pay': overtime_pay,
            'Federal_Tax': federal_tax,
            'State_Tax': state_tax,
            'Social_Security': social_security,
            'Medicare': medicare,
            'Benefits': benefits,
            'Other_Deductions': other_deductions,
            'Net_Pay': net_pay
        })
    
    return pd.DataFrame(payroll_data)

def highlight_performance(row):
    """Highlight performance scores in the dataframe"""
    if row['Performance_Score'] >= 90:
        return ['background-color: lightgreen'] * len(row)
    elif row['Performance_Score'] >= 80:
        return ['background-color: lightyellow'] * len(row)
    elif row['Performance_Score'] >= 70:
        return ['background-color: lightcoral'] * len(row)
    else:
        return [''] * len(row)

def display_add_employee_form():
    """Display add employee form"""
    st.markdown("### ➕ Add New Employee")
    
    with st.form("add_employee_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*")
            department = st.selectbox("Department*", ['Warehouse', 'Delivery', 'Customer Service', 'IT', 'Management'])
            role = st.selectbox("Role*", ['Manager', 'Supervisor', 'Associate', 'Driver', 'Specialist'])
            salary = st.number_input("Annual Salary*", min_value=25000, max_value=200000, value=50000)
        
        with col2:
            email = st.text_input("Email*")
            phone = st.text_input("Phone Number*")
            hire_date = st.date_input("Hire Date*", value=datetime.now())
            manager = st.text_input("Manager")
        
        submitted = st.form_submit_button("Add Employee")
        
        if submitted:
            if name and department and role and email and phone:
                st.success(f"Employee {name} added successfully!")
                st.session_state['show_add_employee'] = False
                st.rerun()
            else:
                st.error("Please fill in all required fields marked with *")
