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

def create_clean_walmart_hero(title, subtitle):
    """Create a clean hero section with Walmart branding - without HTML comments"""
    # Get the absolute paths to the images
    walmart_bg_path = get_image_path("walmart.jpg")
    walmart_logo_path = get_image_path("walmart_logo.png")
    
    # Create the background image CSS with inline data URL
    bg_image_base64 = get_base64_encoded_image(walmart_bg_path)
    bg_image_css = f"linear-gradient(rgba(0, 0, 51, 0.7), rgba(0, 0, 51, 0.7)), url('data:image/jpeg;base64,{bg_image_base64}')"
    
    # Create the logo image with inline data URL
    logo_base64 = get_base64_encoded_image(walmart_logo_path)
    
    # Create HTML without comments
    html = f"""
    <div class="walmart-hero fade-in" style="
        position: relative;
        padding: 100px 40px;
        border-radius: 24px;
        margin: 20px 0 40px 0;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        overflow: hidden;
        background-image: {bg_image_css};
        background-size: cover;
        background-position: center;
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    ">
        <div class="particle particle1"></div>
        <div class="particle particle2"></div>
        <div class="particle particle3"></div>
        <div class="particle particle4"></div>
        <div class="particle particle5"></div>
        
        <div style="position: relative; z-index: 2; max-width: 900px; margin: 0 auto;">
            <div class="hero-logo bounce-in">
                <img src="data:image/png;base64,{logo_base64}" alt="Walmart Logo" style="width: 180px; margin-bottom: 30px;">
            </div>
            
            <h1 class="hero-title" style="
                font-family: 'Poppins', sans-serif;
                font-size: 3.8rem;
                font-weight: 800;
                margin: 0 0 20px 0;
                text-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
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
            
            <div class="wave-container">
                <div class="wave wave1"></div>
                <div class="wave wave2"></div>
            </div>
        </div>
        
        <div class="animated-bg" style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: {bg_image_css};
            background-size: 120% 120%;
            filter: blur(10px) opacity(0.1);
            animation: bgZoom 20s infinite alternate;
        "></div>
    </div>
    """
    
    # CSS without comments
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
        
        .walmart-hero .particle {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            pointer-events: none;
        }
        
        .walmart-hero .particle1 {
            width: 80px;
            height: 80px;
            left: 10%;
            top: 20%;
            animation: floating 8s infinite ease-in-out;
        }
        
        .walmart-hero .particle2 {
            width: 60px;
            height: 60px;
            right: 15%;
            top: 15%;
            animation: floating 10s infinite ease-in-out;
        }
        
        .walmart-hero .particle3 {
            width: 45px;
            height: 45px;
            left: 30%;
            bottom: 25%;
            animation: floating 7s infinite ease-in-out;
        }
        
        .walmart-hero .particle4 {
            width: 90px;
            height: 90px;
            right: 20%;
            bottom: 20%;
            animation: floating 12s infinite ease-in-out;
        }
        
        .walmart-hero .particle5 {
            width: 70px;
            height: 70px;
            left: 50%;
            top: 50%;
            animation: floating 9s infinite ease-in-out;
        }
        
        .walmart-hero .wave-container {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            overflow: hidden;
            line-height: 0;
            transform: rotate(180deg);
        }
        
        .walmart-hero .wave {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 200%;
            height: 40px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none"><path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" fill="%23ffffff" opacity=".25"></path></svg>');
            background-size: 1200px 100%;
        }
        
        .walmart-hero .wave1 {
            opacity: 0.5;
            animation: wave 25s linear infinite;
            z-index: 1;
        }
        
        .walmart-hero .wave2 {
            opacity: 0.3;
            animation: wave 15s linear infinite reverse;
            z-index: 0;
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
        
        @keyframes floating {
            0% { transform: translateY(0) translateX(0); }
            50% { transform: translateY(-20px) translateX(10px); }
            100% { transform: translateY(0) translateX(0); }
        }
        
        @keyframes wave {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        
        @keyframes bgZoom {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }
    </style>
    """
    
    # Return combined HTML and CSS
    return html + css
