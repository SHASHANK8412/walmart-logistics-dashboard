import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_url_hero_section(title, subtitle):
    """
    Create a hero section using external image URL instead of local files
    """
    # Use a reliable external image URL for Walmart
    walmart_img_url = "https://www.logodesignlove.com/wp-content/uploads/2019/07/walmart-logo-01.jpg"
    
    # Create HTML with properly escaped curly braces for CSS
    html = f"""
    <div style="
        position: relative;
        padding: 80px 40px;
        border-radius: 24px;
        margin: 20px 0 40px 0;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        overflow: hidden;
        background-image: linear-gradient(rgba(0, 0, 51, 0.7), rgba(0, 0, 51, 0.7)), url('https://corporate.walmart.com/content/dam/corporate/en_us/design-assets/header-meta/corporate-building-minimal.jpg'); 
        background-size: cover; 
        background-position: center;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    ">
        <div style="margin-bottom: 30px;">
            <h2 style="font-size: 2.5rem; font-weight: bold; color: white; margin: 0;">WALMART</h2>
        </div>
        
        <h1 style="
            font-family: 'Poppins', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            margin: 0 0 20px 0;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            line-height: 1.2;
        ">{title}</h1>
        
        <p style="
            font-family: 'Inter', sans-serif;
            font-size: 1.4rem;
            font-weight: 400;
            margin: 0 auto 30px auto;
            opacity: 0.95;
            max-width: 800px;
            line-height: 1.6;
        ">{subtitle}</p>
    </div>
    """
    
    return html
