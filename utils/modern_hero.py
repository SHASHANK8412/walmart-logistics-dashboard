import streamlit as st
import os
import base64
from pathlib import Path

def get_base64_encoded_image(image_path):
    """Get base64 encoded image for use in CSS backgrounds"""
    if not os.path.isfile(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def get_image_path(image_name):
    """Get the full path to an image in the assets folder"""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Navigate to the assets folder
    assets_dir = os.path.join(current_dir, "assets")
    # Create the full path to the image
    image_path = os.path.join(assets_dir, image_name)
    return image_path

def create_modern_walmart_hero(title, subtitle):
    """Create a modern hero section with colorful abstract background inspired by screenshot"""
    # Get the absolute paths to the images
    walmart_logo_path = get_image_path("walmart_logo.png")
    
    # Create the logo image with inline data URL
    logo_base64 = get_base64_encoded_image(walmart_logo_path)
    
    # Modern gradient background with colorful design like the screenshot
    html = f"""
    <div class="walmart-hero fade-in" style="
        position: relative;
        padding: 80px 40px;
        border-radius: 24px;
        margin: 20px 0 40px 0;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        overflow: hidden;
        background: linear-gradient(135deg, #6e3ec0 0%, #592b9e 100%);
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    ">
        <!-- Abstract Shapes for Modern Design -->
        <div style="
            position: absolute;
            top: -50px;
            left: -50px;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            z-index: 1;
        "></div>
        
        <div style="
            position: absolute;
            bottom: -80px;
            right: 10%;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            z-index: 1;
        "></div>
        
        <div style="
            position: absolute;
            top: 30%;
            right: -50px;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            z-index: 1;
        "></div>
        
        <!-- Wave Element -->
        <div style="
            position: absolute;
            bottom: 50px;
            left: 0;
            right: 0;
            height: 50px;
            background: rgba(255, 255, 255, 0.1);
            transform: skewY(-3deg);
            z-index: 1;
        "></div>
        
        <!-- Main Content -->
        <div style="position: relative; z-index: 2; max-width: 900px; margin: 0 auto;">
            <div class="hero-logo bounce-in">
                <img src="data:image/png;base64,{logo_base64}" alt="Walmart Logo" style="width: 180px; margin-bottom: 30px;">
            </div>
            
            <h1 class="hero-title" style="
                font-family: 'Poppins', sans-serif;
                font-size: 3.8rem;
                font-weight: 800;
                margin: 0 0 20px 0;
                text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                line-height: 1.2;
                background: linear-gradient(90deg, #fff, #f0f0f0);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
            ">{title}</h1>
            
            <p class="hero-subtitle slide-up" style="
                font-family: 'Inter', sans-serif;
                font-size: 1.4rem;
                font-weight: 400;
                margin: 0 auto 30px auto;
                opacity: 0.95;
                max-width: 800px;
                line-height: 1.6;
            ">{subtitle}</p>
            
            <div class="hero-buttons" style="display: flex; gap: 20px; justify-content: center; margin-top: 20px;">
                <button class="modern-button pulse-effect" style="
                    background: #0071dc;
                    box-shadow: 0 10px 25px rgba(0, 113, 220, 0.5);
                    padding: 15px 35px;
                    border-radius: 50px;
                    font-size: 16px;
                ">Get Started</button>
                
                <button class="modern-button glow-effect" style="
                    background: transparent;
                    border: 2px solid white;
                    box-shadow: 0 10px 25px rgba(255, 255, 255, 0.2);
                    padding: 15px 35px;
                    border-radius: 50px;
                    font-size: 16px;
                ">Learn More</button>
            </div>
        </div>
        
        <!-- Modern abstract shapes like in the screenshot -->
        <div style="
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 5px;
        ">
            <div style="width: 10px; height: 10px; background-color: rgba(255,255,255,0.5); border-radius: 50%;"></div>
            <div style="width: 10px; height: 10px; background-color: rgba(255,255,255,0.5); border-radius: 50%;"></div>
            <div style="width: 10px; height: 10px; background-color: rgba(255,255,255,0.5); border-radius: 50%;"></div>
        </div>
        
        <div style="
            position: absolute;
            bottom: 20%;
            left: 10%;
            width: 50px;
            height: 5px;
            background-color: rgba(255,255,255,0.5);
            border-radius: 5px;
            transform: rotate(-45deg);
        "></div>
        
        <div style="
            position: absolute;
            top: 30%;
            right: 10%;
            width: 100px;
            height: 100px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
        "></div>
    </div>
    """
    
    # CSS for animations
    css = """
    <style>
        .walmart-hero .hero-title {
            animation: fadeInDown 1s ease-out forwards;
        }
        
        .walmart-hero .hero-subtitle {
            animation: fadeInUp 1.2s ease-out forwards;
        }
        
        .walmart-hero .hero-buttons {
            animation: fadeIn 1.5s ease-out forwards;
        }
        
        .walmart-hero .pulse-effect {
            animation: pulse 2s infinite;
        }
        
        .walmart-hero .glow-effect {
            animation: glow 3s infinite;
        }
        
        @keyframes fadeInDown {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes fadeInUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes glow {
            0% { box-shadow: 0 0 5px rgba(255,255,255,0.5); }
            50% { box-shadow: 0 0 20px rgba(255,255,255,0.8); }
            100% { box-shadow: 0 0 5px rgba(255,255,255,0.5); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
    """
    
    # Return combined HTML and CSS
    return html + css
