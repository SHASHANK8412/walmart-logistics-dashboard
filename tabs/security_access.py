import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import random
import hashlib
import time
from utils.helpers import display_kpi_metrics, show_notification

def app():
    """Security & Access Control Management System"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                padding: 20px; border-radius: 15px; margin-bottom: 20px; color: white;">
        <h1 style="margin: 0; text-align: center;">🔐 Security & Access Control</h1>
        <p style="margin: 10px 0 0 0; text-align: center; font-size: 16px;">
            User authentication • Role management • Activity monitoring • Threat detection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Security level check
    if 'security_level' not in st.session_state:
        st.session_state.security_level = 'Admin'
    
    # Sidebar for security settings
    with st.sidebar:
        st.header("🔒 Security Settings")
        
        # User role
        user_role = st.selectbox(
            "Current User Role",
            ["Admin", "Security Manager", "IT Manager", "Supervisor", "User"],
            index=0
        )
        st.session_state.security_level = user_role
        
        # Security level
        security_level = st.selectbox(
            "Security Level",
            ["High", "Medium", "Low"],
            index=0
        )
        
        # Monitoring settings
        st.subheader("🔍 Monitoring")
        real_time_monitoring = st.checkbox("Real-time Monitoring", value=True)
        alert_notifications = st.checkbox("Alert Notifications", value=True)
        audit_logging = st.checkbox("Audit Logging", value=True)
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        if st.button("🚨 Security Alert"):
            st.error("Security alert triggered!")
        if st.button("🔄 Refresh Tokens"):
            st.success("Authentication tokens refreshed")
        if st.button("📊 Generate Report", key="security_main_report"):
            st.info("Security report generated")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🛡️ Security Dashboard", "👥 User Management", "🔑 Access Control", "🔍 Activity Monitor", "🚨 Threat Detection", "📋 Compliance"])
    
    with tab1:
        display_security_dashboard()
    
    with tab2:
        display_user_management()
    
    with tab3:
        display_access_control()
    
    with tab4:
        display_activity_monitor()
    
    with tab5:
        display_threat_detection()
    
    with tab6:
        display_compliance()

def display_security_dashboard():
    """Display security dashboard with key metrics"""
    st.header("🛡️ Security Dashboard")
    
    # Security metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        active_users = random.randint(150, 250)
        st.metric("👥 Active Users", active_users, "↑ 12")
    
    with col2:
        failed_logins = random.randint(5, 25)
        st.metric("🚫 Failed Logins", failed_logins, "↑ 3")
    
    with col3:
        security_score = random.uniform(85, 98)
        st.metric("🎯 Security Score", f"{security_score:.1f}%", "↑ 2.3%")
    
    with col4:
        active_sessions = random.randint(75, 125)
        st.metric("🔐 Active Sessions", active_sessions, "↑ 8")
    
    with col5:
        threat_level = random.choice(["Low", "Medium", "High"])
        color = "🟢" if threat_level == "Low" else "🟡" if threat_level == "Medium" else "🔴"
        st.metric("⚠️ Threat Level", f"{color} {threat_level}", "→ Stable")
    
    # Security events timeline
    st.subheader("📅 Recent Security Events")
    
    events = [
        {"time": "2 min ago", "event": "Successful login", "user": "john.doe@walmart.com", "location": "Dallas, TX", "severity": "Info"},
        {"time": "5 min ago", "event": "Failed login attempt", "user": "unknown_user", "location": "Unknown", "severity": "Warning"},
        {"time": "12 min ago", "event": "Password changed", "user": "jane.smith@walmart.com", "location": "Chicago, IL", "severity": "Info"},
        {"time": "25 min ago", "event": "Suspicious activity detected", "user": "bob.johnson@walmart.com", "location": "Miami, FL", "severity": "High"},
        {"time": "1 hour ago", "event": "Admin access granted", "user": "admin@walmart.com", "location": "Seattle, WA", "severity": "Critical"}
    ]
    
    for event in events:
        severity_color = {
            "Info": "🔵",
            "Warning": "🟡", 
            "High": "🟠",
            "Critical": "🔴"
        }.get(event["severity"], "🔵")
        
        st.write(f"{severity_color} **{event['time']}** - {event['event']} by {event['user']} from {event['location']}")
    
    # Security metrics charts
    st.subheader("📊 Security Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Login attempts over time
        hours = list(range(24))
        login_attempts = [random.randint(10, 50) for _ in hours]
        failed_attempts = [random.randint(0, 8) for _ in hours]
        
        fig_logins = go.Figure()
        fig_logins.add_trace(go.Scatter(x=hours, y=login_attempts, mode='lines+markers', name='Total Logins'))
        fig_logins.add_trace(go.Scatter(x=hours, y=failed_attempts, mode='lines+markers', name='Failed Logins'))
        fig_logins.update_layout(title="Login Attempts (Last 24 Hours)", xaxis_title="Hour", yaxis_title="Count")
        st.plotly_chart(fig_logins, use_container_width=True)
    
    with col2:
        # Security incidents by type
        incident_types = ['Failed Login', 'Unauthorized Access', 'Suspicious Activity', 'Policy Violation', 'System Breach']
        incident_counts = [random.randint(5, 30) for _ in incident_types]
        
        fig_incidents = px.pie(values=incident_counts, names=incident_types, title="Security Incidents by Type")
        st.plotly_chart(fig_incidents, use_container_width=True)
    
    # Security alerts
    st.subheader("🚨 Active Security Alerts")
    
    alerts = [
        {"severity": "🔴 Critical", "message": "Multiple failed login attempts from IP 192.168.1.100", "time": "5 min ago"},
        {"severity": "🟠 High", "message": "Unusual access pattern detected for user bob.johnson", "time": "15 min ago"},
        {"severity": "🟡 Medium", "message": "Password policy violation - weak password detected", "time": "30 min ago"},
        {"severity": "🔵 Low", "message": "Session timeout increased for maintenance window", "time": "2 hours ago"}
    ]
    
    for alert in alerts:
        with st.expander(f"{alert['severity']} - {alert['message']}"):
            st.write(f"**Time:** {alert['time']}")
            st.write(f"**Status:** Active")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"🔍 Investigate", key=f"investigate_{alert['time']}"):
                    st.info("Investigation initiated")
            with col2:
                if st.button(f"✅ Resolve", key=f"resolve_{alert['time']}"):
                    st.success("Alert resolved")
            with col3:
                if st.button(f"🚨 Escalate", key=f"escalate_{alert['time']}"):
                    st.warning("Alert escalated to security team")

def display_user_management():
    """Display user management interface"""
    st.header("👥 User Management")
    
    # User statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = random.randint(300, 500)
        st.metric("👤 Total Users", total_users, "↑ 15")
    
    with col2:
        active_users = random.randint(200, 300)
        st.metric("✅ Active Users", active_users, "↑ 8")
    
    with col3:
        pending_users = random.randint(5, 20)
        st.metric("⏳ Pending Approval", pending_users, "↑ 3")
    
    with col4:
        locked_users = random.randint(2, 10)
        st.metric("🔒 Locked Accounts", locked_users, "↓ 2")
    
    # User management actions
    st.subheader("🔧 User Management Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New User", use_container_width=True):
            st.session_state.show_add_user = True
    
    with col2:
        if st.button("📤 Bulk Import", use_container_width=True):
            st.session_state.show_bulk_import = True
    
    with col3:
        if st.button("📊 Export Users", use_container_width=True):
            st.success("User data exported successfully!")
    
    # Add user form
    if st.session_state.get('show_add_user', False):
        with st.expander("➕ Add New User", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone")
            
            with col2:
                department = st.selectbox("Department", ["IT", "Operations", "Management", "HR", "Finance"])
                role = st.selectbox("Role", ["Admin", "Manager", "Supervisor", "Employee", "Contractor"])
                access_level = st.selectbox("Access Level", ["Full", "Limited", "Read-only"])
                start_date = st.date_input("Start Date")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Create User"):
                    st.success(f"User {first_name} {last_name} created successfully!")
                    st.session_state.show_add_user = False
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.show_add_user = False
    
    # User directory
    st.subheader("📖 User Directory")
    
    # Generate sample user data
    users = []
    departments = ["IT", "Operations", "Management", "HR", "Finance", "Security"]
    roles = ["Admin", "Manager", "Supervisor", "Employee", "Contractor"]
    statuses = ["Active", "Inactive", "Locked", "Pending"]
    
    for i in range(50):
        user = {
            'ID': f'U{1000 + i}',
            'Name': f'User {i+1}',
            'Email': f'user{i+1}@walmart.com',
            'Department': random.choice(departments),
            'Role': random.choice(roles),
            'Status': random.choice(statuses),
            'Last Login': (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'Created': (datetime.datetime.now() - datetime.timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        }
        users.append(user)
    
    df_users = pd.DataFrame(users)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dept_filter = st.selectbox("Filter by Department", ['All'] + departments)
    
    with col2:
        role_filter = st.selectbox("Filter by Role", ['All'] + roles)
    
    with col3:
        status_filter = st.selectbox("Filter by Status", ['All'] + statuses)
    
    # Apply filters
    filtered_users = df_users.copy()
    if dept_filter != 'All':
        filtered_users = filtered_users[filtered_users['Department'] == dept_filter]
    if role_filter != 'All':
        filtered_users = filtered_users[filtered_users['Role'] == role_filter]
    if status_filter != 'All':
        filtered_users = filtered_users[filtered_users['Status'] == status_filter]
    
    # Display users
    st.dataframe(filtered_users, use_container_width=True)
    
    # User analytics
    st.subheader("📊 User Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Users by department
        dept_counts = df_users['Department'].value_counts()
        fig_dept = px.bar(x=dept_counts.index, y=dept_counts.values, title="Users by Department")
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col2:
        # Users by status
        status_counts = df_users['Status'].value_counts()
        fig_status = px.pie(values=status_counts.values, names=status_counts.index, title="Users by Status")
        st.plotly_chart(fig_status, use_container_width=True)

def display_access_control():
    """Display access control interface"""
    st.header("🔑 Access Control Management")
    
    # Access control metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_resources = random.randint(50, 100)
        st.metric("🗂️ Protected Resources", total_resources, "↑ 5")
    
    with col2:
        active_permissions = random.randint(200, 500)
        st.metric("✅ Active Permissions", active_permissions, "↑ 25")
    
    with col3:
        role_groups = random.randint(15, 30)
        st.metric("👥 Role Groups", role_groups, "↑ 2")
    
    with col4:
        policy_violations = random.randint(0, 5)
        st.metric("⚠️ Policy Violations", policy_violations, "↓ 1")
    
    # Role-based access control
    st.subheader("🎭 Role-Based Access Control")
    
    # Role definitions
    roles = {
        "Super Admin": {
            "description": "Full system access",
            "permissions": ["All Operations", "User Management", "System Configuration", "Security Settings"],
            "users": 3,
            "color": "#ff4757"
        },
        "Admin": {
            "description": "Administrative access",
            "permissions": ["User Management", "Reports", "Inventory Management", "Order Processing"],
            "users": 12,
            "color": "#ffa726"
        },
        "Manager": {
            "description": "Departmental management",
            "permissions": ["Department Reports", "Staff Management", "Inventory View", "Order Approval"],
            "users": 25,
            "color": "#42a5f5"
        },
        "Supervisor": {
            "description": "Team supervision",
            "permissions": ["Team Reports", "Task Assignment", "Inventory View", "Order Processing"],
            "users": 45,
            "color": "#66bb6a"
        },
        "Employee": {
            "description": "Standard user access",
            "permissions": ["Basic Operations", "Personal Dashboard", "Order Entry", "Inventory Check"],
            "users": 180,
            "color": "#ab47bc"
        }
    }
    
    # Display roles
    for role_name, role_data in roles.items():
        with st.expander(f"{role_name} ({role_data['users']} users)"):
            st.write(f"**Description:** {role_data['description']}")
            st.write("**Permissions:**")
            for perm in role_data['permissions']:
                st.write(f"  • {perm}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"✏️ Edit", key=f"edit_{role_name}"):
                    st.info(f"Editing {role_name} role")
            with col2:
                if st.button(f"👥 View Users", key=f"users_{role_name}"):
                    st.info(f"Showing users with {role_name} role")
            with col3:
                if st.button(f"📊 Analytics", key=f"analytics_{role_name}"):
                    st.info(f"Showing analytics for {role_name} role")
    
    # Permission matrix
    st.subheader("📋 Permission Matrix")
    
    resources = ["Dashboard", "Orders", "Inventory", "Reports", "Settings", "Users", "Analytics", "Warehouse"]
    actions = ["View", "Create", "Edit", "Delete", "Approve"]
    
    # Create permission matrix
    matrix_data = []
    for resource in resources:
        for action in actions:
            matrix_data.append({
                'Resource': resource,
                'Action': action,
                'Super Admin': '✅',
                'Admin': '✅' if action != 'Delete' else '❌',
                'Manager': '✅' if action in ['View', 'Create', 'Edit'] else '❌',
                'Supervisor': '✅' if action in ['View', 'Create'] else '❌',
                'Employee': '✅' if action == 'View' else '❌'
            })
    
    df_matrix = pd.DataFrame(matrix_data)
    
    # Filter by resource
    selected_resource = st.selectbox("Select Resource", ['All'] + resources)
    if selected_resource != 'All':
        df_matrix = df_matrix[df_matrix['Resource'] == selected_resource]
    
    st.dataframe(df_matrix, use_container_width=True)
    
    # Access requests
    st.subheader("📝 Access Requests")
    
    requests = [
        {"user": "john.doe@walmart.com", "resource": "Analytics Dashboard", "action": "View", "reason": "Need access for monthly reports", "status": "Pending"},
        {"user": "jane.smith@walmart.com", "resource": "User Management", "action": "Edit", "reason": "Promote to manager role", "status": "Approved"},
        {"user": "bob.johnson@walmart.com", "resource": "System Settings", "action": "Edit", "reason": "Update configuration", "status": "Rejected"},
    ]
    
    for req in requests:
        with st.expander(f"{req['user']} - {req['resource']} ({req['action']})"):
            st.write(f"**Reason:** {req['reason']}")
            st.write(f"**Status:** {req['status']}")
            
            if req['status'] == 'Pending':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve", key=f"approve_{req['user']}"):
                        st.success("Access request approved")
                with col2:
                    if st.button(f"❌ Reject", key=f"reject_{req['user']}"):
                        st.error("Access request rejected")

def display_activity_monitor():
    """Display activity monitoring dashboard"""
    st.header("🔍 Activity Monitoring")
    
    # Activity metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_activities = random.randint(5000, 10000)
        st.metric("📊 Total Activities", f"{total_activities:,}", "↑ 1,250")
    
    with col2:
        unique_users = random.randint(100, 200)
        st.metric("👥 Unique Users", unique_users, "↑ 15")
    
    with col3:
        avg_session = random.randint(15, 45)
        st.metric("⏱️ Avg Session (min)", avg_session, "↑ 3")
    
    with col4:
        suspicious_activities = random.randint(0, 10)
        st.metric("⚠️ Suspicious Activities", suspicious_activities, "↓ 2")
    
    # Real-time activity feed
    st.subheader("📡 Real-time Activity Feed")
    
    # Generate real-time activities
    activities = []
    users = [f"user{i}@walmart.com" for i in range(1, 21)]
    actions = ["Login", "Logout", "View Dashboard", "Create Order", "Update Inventory", "Generate Report", "Edit Settings"]
    
    for i in range(20):
        activity = {
            'Timestamp': datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 120)),
            'User': random.choice(users),
            'Action': random.choice(actions),
            'Resource': random.choice(["Dashboard", "Orders", "Inventory", "Reports", "Settings"]),
            'IP Address': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'Status': random.choice(["Success", "Failed", "Warning"])
        }
        activities.append(activity)
    
    df_activities = pd.DataFrame(activities)
    df_activities = df_activities.sort_values('Timestamp', ascending=False)
    
    # Display activities
    st.dataframe(df_activities, use_container_width=True)
    
    # Activity analytics
    st.subheader("📊 Activity Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Activity by hour
        hours = list(range(24))
        activity_counts = [random.randint(50, 200) for _ in hours]
        
        fig_hourly = px.bar(x=hours, y=activity_counts, title="Activity by Hour")
        fig_hourly.update_layout(xaxis_title="Hour", yaxis_title="Activity Count")
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col2:
        # Top activities
        action_counts = df_activities['Action'].value_counts()
        fig_actions = px.pie(values=action_counts.values, names=action_counts.index, title="Top Activities")
        st.plotly_chart(fig_actions, use_container_width=True)
    
    # User behavior analysis
    st.subheader("👤 User Behavior Analysis")
    
    # Generate user behavior data
    user_behavior = []
    for user in users[:10]:  # Top 10 users
        behavior = {
            'User': user,
            'Sessions': random.randint(5, 50),
            'Avg Session Duration': random.randint(10, 120),
            'Pages Visited': random.randint(20, 200),
            'Actions Performed': random.randint(50, 500),
            'Risk Score': random.randint(1, 10)
        }
        user_behavior.append(behavior)
    
    df_behavior = pd.DataFrame(user_behavior)
    
    # Risk score visualization
    fig_risk = px.scatter(df_behavior, x='Sessions', y='Actions Performed', 
                         size='Risk Score', color='Risk Score',
                         hover_data=['User', 'Avg Session Duration'],
                         title="User Risk Analysis")
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # Anomaly detection
    st.subheader("🔍 Anomaly Detection")
    
    anomalies = [
        {"user": "john.doe@walmart.com", "anomaly": "Unusual login time (3:00 AM)", "severity": "Medium", "time": "2 hours ago"},
        {"user": "jane.smith@walmart.com", "anomaly": "Multiple failed login attempts", "severity": "High", "time": "30 min ago"},
        {"user": "bob.johnson@walmart.com", "anomaly": "Accessing resources outside normal pattern", "severity": "Low", "time": "1 hour ago"},
    ]
    
    for anomaly in anomalies:
        severity_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(anomaly['severity'], "🔵")
        st.write(f"{severity_color} **{anomaly['user']}**: {anomaly['anomaly']} ({anomaly['time']})")

def display_threat_detection():
    """Display threat detection interface"""
    st.header("🚨 Threat Detection & Response")
    
    # Threat metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        threats_detected = random.randint(5, 25)
        st.metric("🎯 Threats Detected", threats_detected, "↑ 3")
    
    with col2:
        threats_blocked = random.randint(10, 50)
        st.metric("🛡️ Threats Blocked", threats_blocked, "↑ 8")
    
    with col3:
        response_time = random.randint(30, 180)
        st.metric("⚡ Avg Response Time", f"{response_time}s", "↓ 15s")
    
    with col4:
        threat_score = random.randint(1, 10)
        st.metric("📊 Current Threat Score", f"{threat_score}/10", "↓ 1")
    
    # Threat detection rules
    st.subheader("🔧 Threat Detection Rules")
    
    rules = [
        {"name": "Brute Force Detection", "status": "✅ Active", "triggers": 15, "description": "Detect multiple failed login attempts"},
        {"name": "Unusual Access Pattern", "status": "✅ Active", "triggers": 8, "description": "Detect access outside normal hours"},
        {"name": "Privilege Escalation", "status": "✅ Active", "triggers": 3, "description": "Detect unauthorized privilege changes"},
        {"name": "Data Exfiltration", "status": "⚠️ Warning", "triggers": 12, "description": "Detect unusual data download patterns"},
        {"name": "Malware Detection", "status": "✅ Active", "triggers": 0, "description": "Detect malicious file uploads"}
    ]
    
    for rule in rules:
        with st.expander(f"{rule['name']} - {rule['status']}"):
            st.write(f"**Description:** {rule['description']}")
            st.write(f"**Triggers Today:** {rule['triggers']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📊 View Details", key=f"details_{rule['name']}"):
                    st.info(f"Showing details for {rule['name']}")
            with col2:
                if st.button(f"✏️ Edit Rule", key=f"edit_{rule['name']}"):
                    st.info(f"Editing {rule['name']}")
            with col3:
                status = "Disable" if rule['status'] == "✅ Active" else "Enable"
                if st.button(f"🔄 {status}", key=f"toggle_{rule['name']}"):
                    st.success(f"Rule {status.lower()}d")
    
    # Threat intelligence
    st.subheader("🧠 Threat Intelligence")
    
    # Generate threat intelligence data
    threat_sources = ["IP Reputation", "Domain Blacklist", "File Hash", "Behavioral Analysis", "Network Traffic"]
    
    intel_data = []
    for source in threat_sources:
        intel_data.append({
            'Source': source,
            'Threats Identified': random.randint(10, 100),
            'Confidence': random.randint(70, 95),
            'Last Updated': datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 24))
        })
    
    df_intel = pd.DataFrame(intel_data)
    st.dataframe(df_intel, use_container_width=True)
    
    # Threat timeline
    st.subheader("📅 Threat Timeline")
    
    # Generate threat timeline data
    timeline_data = []
    for i in range(7):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        timeline_data.append({
            'Date': date,
            'Threats Detected': random.randint(5, 30),
            'Threats Blocked': random.randint(10, 50),
            'False Positives': random.randint(1, 8)
        })
    
    df_timeline = pd.DataFrame(timeline_data)
    
    fig_timeline = px.line(df_timeline, x='Date', y=['Threats Detected', 'Threats Blocked', 'False Positives'],
                          title="Threat Detection Timeline (Last 7 Days)")
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Incident response
    st.subheader("🚨 Incident Response")
    
    incidents = [
        {"id": "INC-001", "type": "Brute Force Attack", "severity": "High", "status": "Investigating", "time": "30 min ago"},
        {"id": "INC-002", "type": "Suspicious Login", "severity": "Medium", "status": "Resolved", "time": "2 hours ago"},
        {"id": "INC-003", "type": "Data Access Anomaly", "severity": "Low", "status": "Monitoring", "time": "4 hours ago"},
    ]
    
    for incident in incidents:
        severity_color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(incident['severity'], "🔵")
        
        with st.expander(f"{incident['id']} - {incident['type']} {severity_color}"):
            st.write(f"**Severity:** {incident['severity']}")
            st.write(f"**Status:** {incident['status']}")
            st.write(f"**Time:** {incident['time']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"🔍 Investigate", key=f"investigate_{incident['id']}"):
                    st.info("Investigation started")
            with col2:
                if st.button(f"🛡️ Contain", key=f"contain_{incident['id']}"):
                    st.success("Threat contained")
            with col3:
                if st.button(f"✅ Resolve", key=f"resolve_{incident['id']}"):
                    st.success("Incident resolved")

def display_compliance():
    """Display compliance dashboard"""
    st.header("📋 Compliance & Audit")
    
    # Compliance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        compliance_score = random.randint(85, 100)
        st.metric("📊 Compliance Score", f"{compliance_score}%", "↑ 2%")
    
    with col2:
        audit_items = random.randint(200, 500)
        st.metric("📋 Audit Items", audit_items, "↑ 25")
    
    with col3:
        violations = random.randint(0, 5)
        st.metric("⚠️ Violations", violations, "↓ 2")
    
    with col4:
        last_audit = random.randint(30, 90)
        st.metric("📅 Last Audit", f"{last_audit} days ago", "→ 0")
    
    # Compliance frameworks
    st.subheader("📜 Compliance Frameworks")
    
    frameworks = [
        {"name": "SOX (Sarbanes-Oxley)", "status": "✅ Compliant", "score": 95, "last_review": "2 weeks ago"},
        {"name": "GDPR", "status": "✅ Compliant", "score": 92, "last_review": "1 month ago"},
        {"name": "HIPAA", "status": "⚠️ Partial", "score": 78, "last_review": "3 weeks ago"},
        {"name": "PCI DSS", "status": "✅ Compliant", "score": 88, "last_review": "2 months ago"},
        {"name": "ISO 27001", "status": "✅ Compliant", "score": 94, "last_review": "1 week ago"}
    ]
    
    for framework in frameworks:
        with st.expander(f"{framework['name']} - {framework['status']}"):
            st.write(f"**Compliance Score:** {framework['score']}%")
            st.write(f"**Last Review:** {framework['last_review']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📊 View Details", key=f"details_{framework['name']}"):
                    st.info(f"Showing compliance details for {framework['name']}")
            with col2:
                if st.button(f"📋 Generate Report", key=f"report_{framework['name']}"):
                    st.success(f"Compliance report generated for {framework['name']}")
            with col3:
                if st.button(f"🔄 Run Audit", key=f"audit_{framework['name']}"):
                    st.info(f"Audit initiated for {framework['name']}")
    
    # Audit trail
    st.subheader("📝 Audit Trail")
    
    # Generate audit trail data
    audit_actions = ["User Created", "Role Modified", "Permission Granted", "Data Accessed", "System Configuration", "Report Generated"]
    
    audit_trail = []
    for i in range(20):
        audit_trail.append({
            'Timestamp': datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 168)),
            'User': f"user{random.randint(1, 20)}@walmart.com",
            'Action': random.choice(audit_actions),
            'Resource': random.choice(["Users", "Roles", "Data", "Settings", "Reports"]),
            'IP Address': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'Status': random.choice(["Success", "Failed"])
        })
    
    df_audit = pd.DataFrame(audit_trail)
    df_audit = df_audit.sort_values('Timestamp', ascending=False)
    
    st.dataframe(df_audit, use_container_width=True)
    
    # Compliance reports
    st.subheader("📊 Compliance Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Access Control Report"):
            st.success("Access control report generated")
    
    with col2:
        if st.button("📊 Activity Summary"):
            st.success("Activity summary generated")
    
    with col3:
        if st.button("⚠️ Violation Report"):
            st.success("Violation report generated")
    
    # Policy management
    st.subheader("📋 Policy Management")
    
    policies = [
        {"name": "Password Policy", "status": "✅ Active", "compliance": 95, "violations": 3},
        {"name": "Access Control Policy", "status": "✅ Active", "compliance": 92, "violations": 1},
        {"name": "Data Retention Policy", "status": "⚠️ Review Required", "compliance": 78, "violations": 5},
        {"name": "Incident Response Policy", "status": "✅ Active", "compliance": 88, "violations": 2}
    ]
    
    policy_data = pd.DataFrame(policies)
    st.dataframe(policy_data, use_container_width=True)
