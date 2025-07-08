import streamlit as st
import os
import base64

def fix_blank_page_css():
    """Add simple CSS to fix blank page issue"""
    st.markdown("""
    <style>
    /* Simple styles to ensure page renders */
    .stApp {
        background: white;
    }
    
    body {
        font-family: sans-serif;
    }
    
    /* Simple gradient background for hero section */
    .hero-section {
        padding: 60px 40px;
        margin: 20px 0 40px 0;
        text-align: center;
        background: linear-gradient(135deg, #6e3ec0 0%, #592b9e 100%);
        color: white;
        border-radius: 15px;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

def create_simple_hero(title, subtitle):
    """Create a simple hero section that will work reliably"""
    hero_html = f"""
    <div class="hero-section">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """
    return hero_html
