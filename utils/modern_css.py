import streamlit as st
import os
import base64

def inject_modern_css():
    """Inject modern custom CSS with abstract background for the entire application"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables for Modern Design System */
    :root {
        --primary-color: #0066cc;
        --primary-light: #4d94ff;
        --primary-dark: #004499;
        --secondary-color: #6c757d;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --info-color: #3b82f6;
        
        /* Glassmorphism Colors */
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        
        /* Modern Gradient Palette */
        --gradient-primary: linear-gradient(135deg, #6e3ec0 0%, #592b9e 100%);
        --gradient-secondary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-success: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        --gradient-warning: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        --gradient-danger: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%);
        --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        
        /* Typography */
        --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-heading: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        
        /* Spacing */
        --space-xs: 0.25rem;
        --space-sm: 0.5rem;
        --space-md: 1rem;
        --space-lg: 1.5rem;
        --space-xl: 2rem;
        --space-2xl: 3rem;
        
        /* Border Radius */
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --radius-xl: 24px;
        
        /* Shadows */
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.15);
        --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.2);
        --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Global Styles */
    body {
        background: #f5f7fa;
        font-family: var(--font-primary);
    }
    
    /* Modern Abstract Background */
    .stApp {
        background: linear-gradient(135deg, #f6f9fc 0%, #eef2f9 100%);
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(circle at 10% 20%, rgba(110, 62, 192, 0.03) 0%, rgba(89, 43, 158, 0.03) 90%),
                          radial-gradient(circle at 90% 80%, rgba(102, 126, 234, 0.03) 0%, rgba(118, 75, 162, 0.03) 90%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
    
    /* Main Content Area */
    .main .block-container {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 1400px;
    }
    
    /* Hide Streamlit Menu and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Streamlit Elements Styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Card Styling */
    .css-1r6slb0, .css-1nlng10 {
        background: white;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .css-1r6slb0:hover, .css-1nlng10:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: white;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: var(--radius-md);
        padding: 0.5rem 1rem;
        box-shadow: var(--shadow-sm);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary);
        color: white;
    }
    
    /* Input Fields */
    .stTextInput > div > div, .stNumberInput > div > div {
        background: white;
        border-radius: var(--radius-md);
        border: 1px solid #eaeaea;
    }
    
    /* Metrics */
    .css-1xarl3l {
        background: white;
        padding: 1rem;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .css-1xarl3l:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    </style>
    """, unsafe_allow_html=True)
