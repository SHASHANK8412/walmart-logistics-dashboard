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
    st.header("🔍 Quality Control & Compliance")
    st.markdown("**Comprehensive quality management, compliance tracking, and audit systems**")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Quality Dashboard", 
        "📋 Compliance Tracking", 
        "🔍 Audit Management", 
        "🚨 Issue Tracking",
        "📈 Quality Analytics"
    ])
    
    with tab1:
        display_quality_dashboard()
    
    with tab2:
        display_compliance_tracking()
    
    with tab3:
        display_audit_management()
    
    with tab4:
        display_issue_tracking()
    
    with tab5:
        display_quality_analytics()

def display_quality_dashboard():
    st.subheader("📊 Quality Dashboard")
    
    # Quality KPIs
    st.markdown("### 📈 Quality KPIs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Quality Score", "96.2%", delta="1.8%")
        st.metric("Defect Rate", "0.8%", delta="-0.2%")
        
    with col2:
        st.metric("Customer Satisfaction", "4.7/5.0", delta="0.1")
        st.metric("Return Rate", "2.3%", delta="-0.5%")
        
    with col3:
        st.metric("Compliance Rate", "98.5%", delta="0.8%")
        st.metric("Audit Pass Rate", "94.1%", delta="2.3%")
        
    with col4:
        st.metric("Process Efficiency", "92.7%", delta="1.5%")
        st.metric("Time to Resolution", "4.2 hrs", delta="-0.8 hrs")
    
    # Quality trends
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Quality Trends")
        
        # Generate quality trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        quality_data = pd.DataFrame({
            'Date': dates,
            'Quality_Score': np.random.normal(96, 2, 30),
            'Defect_Rate': np.random.normal(0.8, 0.3, 30),
            'Customer_Satisfaction': np.random.normal(4.7, 0.2, 30),
            'Compliance_Rate': np.random.normal(98.5, 1, 30)
        })
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quality Score', 'Defect Rate', 'Customer Satisfaction', 'Compliance Rate'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                   [{'secondary_y': False}, {'secondary_y': False}]]
        )
        
        # Quality Score
        fig.add_trace(
            go.Scatter(x=quality_data['Date'], y=quality_data['Quality_Score'], 
                      name='Quality Score', line=dict(color='green')),
            row=1, col=1
        )
        
        # Defect Rate
        fig.add_trace(
            go.Scatter(x=quality_data['Date'], y=quality_data['Defect_Rate'], 
                      name='Defect Rate', line=dict(color='red')),
            row=1, col=2
        )
        
        # Customer Satisfaction
        fig.add_trace(
            go.Scatter(x=quality_data['Date'], y=quality_data['Customer_Satisfaction'], 
                      name='Customer Satisfaction', line=dict(color='blue')),
            row=2, col=1
        )
        
        # Compliance Rate
        fig.add_trace(
            go.Scatter(x=quality_data['Date'], y=quality_data['Compliance_Rate'], 
                      name='Compliance Rate', line=dict(color='orange')),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Quality by department
        st.markdown("### 🏢 Quality by Department")
        
        dept_quality = pd.DataFrame({
            'Department': ['Warehouse', 'Delivery', 'Customer Service', 'IT', 'Procurement'],
            'Quality_Score': [94.2, 96.8, 98.1, 92.5, 95.7],
            'Defect_Rate': [1.2, 0.5, 0.3, 1.8, 0.9],
            'Compliance_Rate': [97.8, 99.2, 98.9, 96.1, 98.4]
        })
        
        fig = px.bar(
            dept_quality,
            x='Department',
            y=['Quality_Score', 'Compliance_Rate'],
            title="Quality and Compliance by Department",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Quality alerts
        st.markdown("### 🚨 Quality Alerts")
        
        alerts = [
            {"level": "High", "message": "Defect rate spike in Warehouse A", "time": "10 min ago", "color": "red"},
            {"level": "Medium", "message": "Customer complaint - Order #12345", "time": "1 hour ago", "color": "orange"},
            {"level": "Low", "message": "Quality audit scheduled for tomorrow", "time": "2 hours ago", "color": "blue"},
            {"level": "Info", "message": "New quality standard implemented", "time": "1 day ago", "color": "green"}
        ]
        
        for alert in alerts:
            st.markdown(f"""
            <div style="padding: 10px; border-left: 4px solid {alert['color']}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{alert['level']}:</strong> {alert['message']}<br>
                <small>{alert['time']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Quality checklist
        st.markdown("### ✅ Quality Checklist")
        
        checklist_items = [
            "Daily quality inspections",
            "Customer feedback review",
            "Compliance documentation",
            "Training completion",
            "Audit preparation",
            "Issue resolution"
        ]
        
        for item in checklist_items:
            completed = np.random.random() > 0.3
            st.checkbox(item, value=completed, disabled=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📋 New Quality Check"):
            st.info("Quality check form opened!")
        
        if st.button("🚨 Report Issue"):
            st.info("Issue reporting form opened!")
        
        if st.button("📊 Generate Report", key="quality_metrics_report"):
            st.info("Quality report generated!")

def display_compliance_tracking():
    st.subheader("📋 Compliance Tracking")
    
    # Compliance overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Compliance Overview")
        
        # Compliance by regulation
        compliance_data = pd.DataFrame({
            'Regulation': ['FDA', 'OSHA', 'ISO 9001', 'SOX', 'GDPR', 'FTC'],
            'Compliance_Rate': [98.5, 96.2, 99.1, 97.8, 94.3, 98.9],
            'Last_Audit': ['2023-10-15', '2023-11-02', '2023-09-20', '2023-11-10', '2023-10-28', '2023-11-05'],
            'Next_Audit': ['2024-01-15', '2024-02-02', '2024-01-20', '2024-02-10', '2024-01-28', '2024-02-05'],
            'Status': ['Compliant', 'Compliant', 'Compliant', 'Compliant', 'Action Required', 'Compliant'],
            'Risk_Level': ['Low', 'Medium', 'Low', 'Low', 'High', 'Low']
        })
        
        # Convert date strings to datetime
        compliance_data['Last_Audit'] = pd.to_datetime(compliance_data['Last_Audit'])
        compliance_data['Next_Audit'] = pd.to_datetime(compliance_data['Next_Audit'])
        
        st.dataframe(
            compliance_data,
            use_container_width=True,
            column_config={
                "Compliance_Rate": st.column_config.ProgressColumn(
                    "Compliance Rate",
                    help="Regulatory compliance rate",
                    min_value=0,
                    max_value=100
                ),
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Compliance status"
                ),
                "Risk_Level": st.column_config.TextColumn(
                    "Risk Level",
                    help="Risk assessment"
                )
            }
        )
        
        # Compliance timeline
        st.markdown("### 📅 Compliance Timeline")
        
        # Generate compliance events
        timeline_data = pd.DataFrame({
            'Date': pd.date_range(start=datetime.now() - timedelta(days=90), periods=20, freq='5D'),
            'Event': ['Audit Completed', 'Policy Updated', 'Training Conducted', 'Compliance Check', 'Documentation Review'] * 4,
            'Regulation': ['FDA', 'OSHA', 'ISO 9001', 'SOX', 'GDPR'] * 4,
            'Status': np.random.choice(['Completed', 'In Progress', 'Planned'], 20),
            'Priority': np.random.choice(['Low', 'Medium', 'High'], 20)
        })
        
        fig = px.timeline(
            timeline_data,
            x_start="Date",
            x_end="Date",
            y="Regulation",
            color="Status",
            title="Compliance Timeline",
            hover_data=["Event", "Priority"]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Compliance documentation
        st.markdown("### 📄 Compliance Documentation")
        
        doc_data = pd.DataFrame({
            'Document': ['Privacy Policy', 'Quality Manual', 'Safety Procedures', 'Audit Reports', 'Training Records'],
            'Version': ['v2.1', 'v3.0', 'v1.8', 'v4.2', 'v2.3'],
            'Last_Updated': pd.date_range(start=datetime.now() - timedelta(days=180), periods=5, freq='30D'),
            'Status': ['Current', 'Current', 'Needs Update', 'Current', 'Current'],
            'Owner': ['Legal Team', 'Quality Team', 'Safety Team', 'Audit Team', 'HR Team']
        })
        
        st.dataframe(doc_data, use_container_width=True)
    
    with col2:
        # Compliance statistics
        st.markdown("### 📊 Compliance Statistics")
        
        overall_compliance = compliance_data['Compliance_Rate'].mean()
        pending_actions = len(compliance_data[compliance_data['Status'] == 'Action Required'])
        high_risk_items = len(compliance_data[compliance_data['Risk_Level'] == 'High'])
        
        st.metric("Overall Compliance", f"{overall_compliance:.1f}%", delta="1.2%")
        st.metric("Pending Actions", pending_actions, delta="-2")
        st.metric("High Risk Items", high_risk_items, delta="0")
        
        # Compliance distribution
        st.markdown("### 📊 Compliance Distribution")
        
        status_counts = compliance_data['Status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Compliance Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Upcoming deadlines
        st.markdown("### ⏰ Upcoming Deadlines")
        
        # Calculate days until next audit
        today = datetime.now()
        compliance_data['Days_Until_Audit'] = (compliance_data['Next_Audit'] - today).dt.days
        
        upcoming = compliance_data[compliance_data['Days_Until_Audit'] <= 30].sort_values('Days_Until_Audit')
        
        for _, row in upcoming.iterrows():
            days = row['Days_Until_Audit']
            color = "red" if days <= 7 else "orange" if days <= 14 else "yellow"
            st.markdown(f"""
            <div style="padding: 8px; border-left: 4px solid {color}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{row['Regulation']}</strong><br>
                Next audit in {days} days
            </div>
            """, unsafe_allow_html=True)

def display_audit_management():
    st.subheader("🔍 Audit Management")
    
    # Audit dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Audit Schedule")
        
        # Generate audit data
        audit_data = generate_audit_data()
        
        # Audit filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            audit_type_filter = st.selectbox(
                "Audit Type",
                ["All"] + list(audit_data['Type'].unique())
            )
        
        with filter_col2:
            status_filter = st.selectbox(
                "Status",
                ["All"] + list(audit_data['Status'].unique())
            )
        
        with filter_col3:
            department_filter = st.selectbox(
                "Department",
                ["All"] + list(audit_data['Department'].unique())
            )
        
        # Apply filters
        filtered_audits = audit_data.copy()
        
        if audit_type_filter != "All":
            filtered_audits = filtered_audits[filtered_audits['Type'] == audit_type_filter]
        
        if status_filter != "All":
            filtered_audits = filtered_audits[filtered_audits['Status'] == status_filter]
        
        if department_filter != "All":
            filtered_audits = filtered_audits[filtered_audits['Department'] == department_filter]
        
        # Display audit table
        st.dataframe(
            filtered_audits,
            use_container_width=True,
            column_config={
                "Progress": st.column_config.ProgressColumn(
                    "Progress",
                    help="Audit completion progress",
                    min_value=0,
                    max_value=100
                ),
                "Risk_Level": st.column_config.TextColumn(
                    "Risk Level",
                    help="Risk assessment"
                )
            }
        )
        
        # Audit findings
        st.markdown("### 🔍 Audit Findings")
        
        findings_data = pd.DataFrame({
            'Finding_ID': [f'F{1000 + i}' for i in range(8)],
            'Audit_ID': ['A001', 'A002', 'A001', 'A003', 'A002', 'A004', 'A003', 'A001'],
            'Category': ['Process', 'Documentation', 'Compliance', 'Safety', 'Quality', 'Process', 'Documentation', 'Safety'],
            'Severity': ['Medium', 'High', 'Low', 'Critical', 'Medium', 'Low', 'High', 'Medium'],
            'Description': [
                'Incomplete documentation process',
                'Missing compliance certificates',
                'Minor process deviation',
                'Safety protocol violation',
                'Quality control gap',
                'Process inefficiency',
                'Outdated procedures',
                'Safety equipment missing'
            ],
            'Status': ['Open', 'Closed', 'In Progress', 'Open', 'Closed', 'In Progress', 'Open', 'Closed'],
            'Assigned_To': ['Team A', 'Team B', 'Team C', 'Team A', 'Team B', 'Team C', 'Team A', 'Team B']
        })
        
        st.dataframe(findings_data, use_container_width=True)
    
    with col2:
        # Audit statistics
        st.markdown("### 📊 Audit Statistics")
        
        total_audits = len(audit_data)
        completed_audits = len(audit_data[audit_data['Status'] == 'Completed'])
        pass_rate = (completed_audits / total_audits) * 100 if total_audits > 0 else 0
        
        st.metric("Total Audits", total_audits)
        st.metric("Completed Audits", completed_audits, delta=f"+{completed_audits-5}")
        st.metric("Pass Rate", f"{pass_rate:.1f}%", delta="3.2%")
        
        # Audit type distribution
        st.markdown("### 📊 Audit Types")
        
        type_counts = audit_data['Type'].value_counts()
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Audit Type Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Findings by severity
        st.markdown("### 🚨 Findings by Severity")
        
        severity_counts = findings_data['Severity'].value_counts()
        colors = {'Critical': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}
        
        for severity, count in severity_counts.items():
            color = colors.get(severity, 'gray')
            st.markdown(f"""
            <div style="padding: 8px; border-left: 4px solid {color}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{severity}:</strong> {count} findings
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("➕ Schedule Audit"):
            st.info("Audit scheduling form opened!")
        
        if st.button("📋 Create Checklist"):
            st.info("Audit checklist created!")
        
        if st.button("📊 Generate Report", key="audit_report"):
            st.info("Audit report generated!")

def display_issue_tracking():
    st.subheader("🚨 Issue Tracking")
    
    # Issue dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Issue Management")
        
        # Generate issue data
        issue_data = generate_issue_data()
        
        # Issue filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            category_filter = st.selectbox(
                "Category",
                ["All"] + list(issue_data['Category'].unique())
            )
        
        with filter_col2:
            priority_filter = st.selectbox(
                "Priority",
                ["All"] + list(issue_data['Priority'].unique())
            )
        
        with filter_col3:
            status_filter = st.selectbox(
                "Status",
                ["All"] + list(issue_data['Status'].unique())
            )
        
        # Apply filters
        filtered_issues = issue_data.copy()
        
        if category_filter != "All":
            filtered_issues = filtered_issues[filtered_issues['Category'] == category_filter]
        
        if priority_filter != "All":
            filtered_issues = filtered_issues[filtered_issues['Priority'] == priority_filter]
        
        if status_filter != "All":
            filtered_issues = filtered_issues[filtered_issues['Status'] == status_filter]
        
        # Display issue table
        st.dataframe(
            filtered_issues,
            use_container_width=True,
            column_config={
                "Progress": st.column_config.ProgressColumn(
                    "Progress",
                    help="Issue resolution progress",
                    min_value=0,
                    max_value=100
                ),
                "Priority": st.column_config.TextColumn(
                    "Priority",
                    help="Issue priority level"
                )
            }
        )
        
        # Issue resolution timeline
        st.markdown("### 📊 Issue Resolution Timeline")
        
        # Generate resolution data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        resolution_data = pd.DataFrame({
            'Date': dates,
            'Issues_Opened': np.random.poisson(3, 30),
            'Issues_Closed': np.random.poisson(2.5, 30),
            'Issues_Escalated': np.random.poisson(0.5, 30)
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=resolution_data['Date'],
            y=resolution_data['Issues_Opened'],
            name='Opened',
            line=dict(color='red', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=resolution_data['Date'],
            y=resolution_data['Issues_Closed'],
            name='Closed',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=resolution_data['Date'],
            y=resolution_data['Issues_Escalated'],
            name='Escalated',
            line=dict(color='orange', width=2)
        ))
        
        fig.update_layout(
            title="Issue Resolution Timeline",
            xaxis_title="Date",
            yaxis_title="Number of Issues",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Root cause analysis
        st.markdown("### 🔍 Root Cause Analysis")
        
        root_causes = pd.DataFrame({
            'Root_Cause': ['Process Gap', 'Human Error', 'System Failure', 'Communication', 'Training', 'Equipment'],
            'Frequency': [15, 12, 8, 6, 4, 3],
            'Impact_Score': [8.5, 7.2, 9.1, 6.8, 5.5, 8.9]
        })
        
        fig = px.scatter(
            root_causes,
            x='Frequency',
            y='Impact_Score',
            size='Frequency',
            color='Root_Cause',
            title="Root Cause Analysis Matrix",
            labels={'Impact_Score': 'Impact Score (1-10)'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Issue statistics
        st.markdown("### 📊 Issue Statistics")
        
        total_issues = len(issue_data)
        open_issues = len(issue_data[issue_data['Status'] == 'Open'])
        critical_issues = len(issue_data[issue_data['Priority'] == 'Critical'])
        avg_resolution_time = issue_data['Resolution_Time_Hours'].mean()
        
        st.metric("Total Issues", total_issues)
        st.metric("Open Issues", open_issues, delta=f"-{3}")
        st.metric("Critical Issues", critical_issues, delta=f"-{1}")
        st.metric("Avg Resolution Time", f"{avg_resolution_time:.1f} hrs", delta="-2.3 hrs")
        
        # Issue priority distribution
        st.markdown("### 📊 Priority Distribution")
        
        priority_counts = issue_data['Priority'].value_counts()
        colors = {'Critical': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}
        
        fig = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            title="Issue Priority Distribution",
            color_discrete_map=colors
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent issues
        st.markdown("### 🕐 Recent Issues")
        
        recent_issues = issue_data.head(5)
        
        for _, issue in recent_issues.iterrows():
            priority_color = colors.get(issue['Priority'], 'gray')
            st.markdown(f"""
            <div style="padding: 8px; border-left: 4px solid {priority_color}; background-color: rgba(255,255,255,0.1); margin: 5px 0;">
                <strong>{issue['Issue_ID']}</strong><br>
                {issue['Description'][:50]}...<br>
                <small>{issue['Priority']} Priority • {issue['Status']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🚨 Report New Issue"):
            st.info("Issue reporting form opened!")
        
        if st.button("📋 Assign Issues"):
            st.info("Issue assignment interface opened!")
        
        if st.button("📊 Generate Analysis"):
            st.info("Issue analysis report generated!")

def display_quality_analytics():
    st.subheader("📈 Quality Analytics")
    
    # Advanced analytics
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Quality Performance Analysis")
        
        # Generate quality metrics over time
        dates = pd.date_range(start=datetime.now() - timedelta(days=90), periods=90, freq='D')
        quality_metrics = pd.DataFrame({
            'Date': dates,
            'Quality_Score': np.random.normal(95, 3, 90),
            'Defect_Rate': np.random.normal(1.2, 0.5, 90),
            'Customer_Satisfaction': np.random.normal(4.6, 0.3, 90),
            'Process_Efficiency': np.random.normal(88, 4, 90),
            'Cost_of_Quality': np.random.normal(2.5, 0.8, 90)
        })
        
        # Quality correlation matrix
        st.markdown("### 🔍 Quality Correlation Matrix")
        
        correlation_matrix = quality_metrics[['Quality_Score', 'Defect_Rate', 'Customer_Satisfaction', 'Process_Efficiency', 'Cost_of_Quality']].corr()
        
        fig = px.imshow(
            correlation_matrix,
            labels=dict(x="Metrics", y="Metrics", color="Correlation"),
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig.update_layout(title="Quality Metrics Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)
        
        # Quality improvement trends
        st.markdown("### 📈 Quality Improvement Trends")
        
        fig = go.Figure()
        
        # Add trend lines
        fig.add_trace(go.Scatter(
            x=quality_metrics['Date'],
            y=quality_metrics['Quality_Score'],
            name='Quality Score',
            line=dict(color='green', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=quality_metrics['Date'],
            y=quality_metrics['Customer_Satisfaction'] * 20,  # Scale for visualization
            name='Customer Satisfaction (scaled)',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=quality_metrics['Date'],
            y=quality_metrics['Process_Efficiency'],
            name='Process Efficiency',
            line=dict(color='orange', width=2)
        ))
        
        fig.update_layout(
            title="Quality Improvement Trends",
            xaxis_title="Date",
            yaxis_title="Score",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Quality by product category
        st.markdown("### 📦 Quality by Product Category")
        
        category_quality = pd.DataFrame({
            'Category': ['Electronics', 'Clothing', 'Food', 'Home & Garden', 'Sports'],
            'Quality_Score': [94.2, 96.8, 98.1, 92.5, 95.7],
            'Defect_Rate': [1.5, 0.8, 0.3, 2.1, 1.2],
            'Customer_Rating': [4.5, 4.7, 4.8, 4.3, 4.6],
            'Return_Rate': [2.8, 1.5, 0.8, 3.2, 2.1]
        })
        
        fig = px.bar(
            category_quality,
            x='Category',
            y=['Quality_Score', 'Customer_Rating'],
            title="Quality Metrics by Product Category",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Quality insights
        st.markdown("### 💡 Quality Insights")
        
        insights = [
            {"metric": "Quality Score", "trend": "↗️ Improving", "change": "+2.3%"},
            {"metric": "Defect Rate", "trend": "↘️ Decreasing", "change": "-0.8%"},
            {"metric": "Customer Satisfaction", "trend": "↗️ Improving", "change": "+0.2"},
            {"metric": "Process Efficiency", "trend": "↗️ Improving", "change": "+1.5%"}
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div style="padding: 10px; background-color: rgba(255,255,255,0.1); margin: 5px 0; border-radius: 5px;">
                <strong>{insight['metric']}</strong><br>
                {insight['trend']} {insight['change']}
            </div>
            """, unsafe_allow_html=True)
        
        # Quality predictions
        st.markdown("### 🔮 Quality Predictions")
        
        predictions = {
            "Next Month Quality Score": "96.8%",
            "Expected Defect Rate": "0.7%",
            "Customer Satisfaction": "4.8/5.0",
            "Process Efficiency": "91.2%"
        }
        
        for metric, prediction in predictions.items():
            st.metric(metric, prediction)
        
        # Quality recommendations
        st.markdown("### 🎯 Recommendations")
        
        recommendations = [
            "Focus on Electronics category quality improvement",
            "Implement predictive quality controls",
            "Increase customer feedback collection",
            "Automate quality inspection processes"
        ]
        
        for i, rec in enumerate(recommendations):
            st.markdown(f"{i+1}. {rec}")
        
        # Quality benchmark
        st.markdown("### 📊 Industry Benchmark")
        
        benchmark_data = pd.DataFrame({
            'Metric': ['Quality Score', 'Defect Rate', 'Customer Satisfaction'],
            'Our_Performance': [96.2, 0.8, 4.7],
            'Industry_Average': [92.5, 1.5, 4.3],
            'Best_in_Class': [98.1, 0.3, 4.9]
        })
        
        fig = px.bar(
            benchmark_data,
            x='Metric',
            y=['Our_Performance', 'Industry_Average', 'Best_in_Class'],
            title="Quality Benchmark Comparison",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

# Helper functions
def generate_audit_data():
    """Generate mock audit data"""
    np.random.seed(42)
    
    audit_types = ['Internal', 'External', 'Supplier', 'Customer', 'Regulatory']
    departments = ['Warehouse', 'Delivery', 'Customer Service', 'IT', 'Procurement']
    statuses = ['Planned', 'In Progress', 'Completed', 'Cancelled']
    risk_levels = ['Low', 'Medium', 'High', 'Critical']
    
    audits = []
    for i in range(15):
        audits.append({
            'Audit_ID': f'A{1000 + i}',
            'Type': np.random.choice(audit_types),
            'Department': np.random.choice(departments),
            'Auditor': f'Auditor {i % 5 + 1}',
            'Start_Date': datetime.now() + timedelta(days=np.random.randint(-30, 60)),
            'End_Date': datetime.now() + timedelta(days=np.random.randint(1, 90)),
            'Status': np.random.choice(statuses),
            'Progress': np.random.randint(0, 101),
            'Risk_Level': np.random.choice(risk_levels),
            'Findings_Count': np.random.randint(0, 8),
            'Score': np.random.uniform(70, 100)
        })
    
    return pd.DataFrame(audits)

def generate_issue_data():
    """Generate mock issue data"""
    np.random.seed(42)
    
    categories = ['Quality', 'Process', 'Safety', 'Compliance', 'Customer', 'System']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
    
    issues = []
    for i in range(25):
        issues.append({
            'Issue_ID': f'I{2000 + i}',
            'Category': np.random.choice(categories),
            'Priority': np.random.choice(priorities),
            'Status': np.random.choice(statuses),
            'Description': f'Issue description for {i+1}',
            'Reporter': f'User {i % 10 + 1}',
            'Assignee': f'Team {i % 5 + 1}',
            'Created_Date': datetime.now() - timedelta(days=np.random.randint(1, 60)),
            'Resolution_Time_Hours': np.random.uniform(1, 48),
            'Progress': np.random.randint(0, 101),
            'Impact_Score': np.random.uniform(1, 10)
        })
    
    return pd.DataFrame(issues)
