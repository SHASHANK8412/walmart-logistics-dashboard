import streamlit as st
import os
import base64
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_image_url(image_name):
    """
    Get a URL for an image that works in CSS backgrounds.
    Falls back to a direct path if base64 encoding fails.
    """
    try:
        # Get the full path to the image
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_dir = os.path.join(current_dir, "assets")
        image_path = os.path.join(assets_dir, image_name)
        
        logger.info(f"Looking for image at: {image_path}")
        logger.info(f"Current directory: {current_dir}")
        logger.info(f"Assets directory: {assets_dir}")
        
        # Check if file exists
        if not os.path.isfile(image_path):
            logger.warning(f"Image file not found: {image_path}")
            return None
        
        # Try to base64 encode the image
        try:
            with open(image_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                if image_name.lower().endswith('.jpg') or image_name.lower().endswith('.jpeg'):
                    return f"data:image/jpeg;base64,{encoded}"
                elif image_name.lower().endswith('.png'):
                    return f"data:image/png;base64,{encoded}"
                else:
                    return f"data:image/;base64,{encoded}"
        except Exception as e:
            logger.warning(f"Failed to encode image {image_name}: {str(e)}")
            # Fall back to direct URL if encoding fails
            relative_path = os.path.join("assets", image_name)
            return relative_path
            
    except Exception as e:
        logger.error(f"Error processing image {image_name}: {str(e)}")
        return None

def create_robust_hero_section(title, subtitle, use_walmart_bg=True):
    """
    Create a hero section with Walmart background that gracefully handles errors
    """
    # Try to get background image URL
    bg_image_url = None
    if use_walmart_bg:
        bg_image_url = get_image_url("walmart.jpg")
    
    # Define background style based on whether image is available
    if bg_image_url and bg_image_url.startswith('data:'):
        # We have a base64 encoded image
        bg_style = f"background-image: linear-gradient(rgba(0, 0, 51, 0.7), rgba(0, 0, 51, 0.7)), url('{bg_image_url}'); background-size: cover; background-position: center;"
    elif bg_image_url:
        # We have a direct URL to the image
        bg_style = f"background-image: linear-gradient(rgba(0, 0, 51, 0.7), rgba(0, 0, 51, 0.7)), url('{bg_image_url}'); background-size: cover; background-position: center;"
    else:
        # Fallback to gradient if no image is available
        bg_style = "background: linear-gradient(135deg, #6e3ec0 0%, #592b9e 100%);"
    
    # Try to get logo image URL
    logo_html = ""
    logo_url = get_image_url("walmart_logo.png")
    if logo_url:
        logo_html = f"""
        <div style="margin-bottom: 30px;">
            <img src="{logo_url}" alt="Walmart Logo" style="width: 180px;">
        </div>
        """
    else:
        # Create text-based logo as fallback
        logo_html = f"""
        <div style="margin-bottom: 30px;">
            <h2 style="font-size: 2.5rem; font-weight: bold; color: white; margin: 0;">WALMART</h2>
        </div>
        """
    
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
        {bg_style}
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    ">
        {logo_html}
        
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
