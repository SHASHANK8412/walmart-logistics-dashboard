"""
World-Class UI/UX Styling Module for Walmart Logistics Dashboard
Modern design system with glassmorphism, dark mode support, and responsive layouts
"""

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

def inject_custom_css():
    """Inject world-class custom CSS for the entire application"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables for Design System */
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
        
        /* Gradients */
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
    .main .block-container {
        padding: 1rem 2rem 2rem 2rem;
        max-width: 1400px;
    }
    
    /* Hide Streamlit Menu and Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
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
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    .slide-up {
        animation: slideUp 0.5s ease-out;
    }
    
    .bounce-in {
        animation: bounceIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Glassmorphism Components */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        box-shadow: var(--glass-shadow);
        padding: var(--space-lg);
        margin: var(--space-md) 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Modern Buttons */
    .modern-button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 12px 24px;
        font-family: var(--font-primary);
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .modern-button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .modern-button:active {
        transform: translateY(0);
    }
    
    .modern-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .modern-button:hover::before {
        left: 100%;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
        border-left: 4px solid var(--primary-color);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }
    
    /* Status Badges */
    .status-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-success {
        background: var(--gradient-success);
        color: white;
    }
    
    .status-warning {
        background: var(--gradient-warning);
        color: #8b4513;
    }
    
    .status-danger {
        background: var(--gradient-danger);
        color: white;
    }
    
    /* Modern Data Tables */
    .modern-table {
        background: white;
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-md);
        margin: var(--space-md) 0;
    }
    
    .modern-table thead {
        background: var(--gradient-primary);
        color: white;
    }
    
    .modern-table th {
        padding: 16px;
        font-weight: 600;
        text-align: left;
        border: none;
    }
    
    .modern-table td {
        padding: 16px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        transition: background-color 0.2s ease;
    }
    
    .modern-table tr:hover td {
        background-color: rgba(102, 126, 234, 0.05);
    }
    
    /* Progress Bars */
    .modern-progress {
        background: rgba(0,0,0,0.1);
        border-radius: 20px;
        height: 8px;
        overflow: hidden;
        position: relative;
    }
    
    .modern-progress-bar {
        background: var(--gradient-primary);
        height: 100%;
        border-radius: 20px;
        transition: width 0.6s ease;
        position: relative;
    }
    
    .modern-progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-image: linear-gradient(
            -45deg,
            rgba(255, 255, 255, .2) 25%,
            transparent 25%,
            transparent 50%,
            rgba(255, 255, 255, .2) 50%,
            rgba(255, 255, 255, .2) 75%,
            transparent 75%,
            transparent
        );
        background-size: 50px 50px;
        animation: move 2s linear infinite;
    }
    
    @keyframes move {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }
    
    /* Modern Navigation */
    .modern-nav {
        background: white;
        box-shadow: var(--shadow-sm);
        border-radius: var(--radius-lg);
        padding: var(--space-sm);
        margin-bottom: var(--space-lg);
    }
    
    /* Responsive Grid */
    .grid-responsive {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: var(--space-lg);
        margin: var(--space-lg) 0;
    }
    
    /* Dark Mode Support */
    @media (prefers-color-scheme: dark) {
        :root {
            --glass-bg: rgba(0, 0, 0, 0.3);
            --glass-border: rgba(255, 255, 255, 0.1);
        }
        
        .glass-card {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .metric-card {
            background: rgba(0, 0, 0, 0.8);
            color: white;
        }
    }
    
    /* Mobile Optimizations */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .grid-responsive {
            grid-template-columns: 1fr;
            gap: var(--space-md);
        }
        
        .glass-card {
            padding: var(--space-md);
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_hero_section(title, subtitle, gradient_type="primary"):
    """Create a world-class hero section"""
    gradients = {
        "primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "success": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
        "warning": "linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%)",
        "danger": "linear-gradient(135deg, #ff7675 0%, #fd79a8 100%)"
    }
    
    return f"""
    <div class="fade-in" style="
        background: {gradients.get(gradient_type, gradients['primary'])};
        padding: 60px 40px;
        border-radius: 24px;
        margin: 20px 0 40px 0;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: relative; z-index: 2;">
            <h1 style="
                font-family: 'Poppins', sans-serif;
                font-size: 3.5rem;
                font-weight: 700;
                margin: 0 0 20px 0;
                text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                line-height: 1.2;
            ">{title}</h1>
            <p style="
                font-family: 'Inter', sans-serif;
                font-size: 1.25rem;
                font-weight: 400;
                margin: 0;
                opacity: 0.95;
                max-width: 800px;
                margin: 0 auto;
                line-height: 1.6;
            ">{subtitle}</p>
        </div>
        <div style="
            position: absolute;
            top: -50%;
            right: -20%;
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            filter: blur(40px);
        "></div>
        <div style="
            position: absolute;
            bottom: -30%;
            left: -10%;
            width: 150px;
            height: 150px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 50%;
            filter: blur(30px);
        "></div>
    </div>
    """

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

def create_walmart_hero_section(title, subtitle):
    """Create a world-class hero section with Walmart background image and animations"""
    # Get the absolute paths to the images
    walmart_bg_path = get_image_path("walmart.jpg")
    walmart_logo_path = get_image_path("walmart_logo.png")
    
    # Create the background image CSS with inline data URL
    bg_image_base64 = get_base64_encoded_image(walmart_bg_path)
    bg_image_css = f"linear-gradient(rgba(0, 0, 51, 0.7), rgba(0, 0, 51, 0.7)), url('data:image/jpeg;base64,{bg_image_base64}')"
    
    # Create the logo image with inline data URL
    logo_base64 = get_base64_encoded_image(walmart_logo_path)
    
    # Create HTML with properly escaped curly braces for CSS
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
        <!-- Animated Floating Particles -->
        <div class="particle particle1"></div>
        <div class="particle particle2"></div>
        <div class="particle particle3"></div>
        <div class="particle particle4"></div>
        <div class="particle particle5"></div>
        
        <!-- Hero Content -->
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
            
            <!-- Animated Buttons -->
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
            
            <!-- Animated Wave Bottom -->
            <div class="wave-container">
                <div class="wave wave1"></div>
                <div class="wave wave2"></div>
            </div>
        </div>
        
        <!-- Moving Background Effect -->
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
    
    # CSS without f-string interpolation to avoid curly brace issues
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

def create_walmart_hero_section_fixed(title, subtitle):
    """Create a world-class hero section with Walmart background image and animations - fixed version"""
    # Get the absolute paths to the images
    walmart_bg_path = get_image_path("walmart.jpg")
    walmart_logo_path = get_image_path("walmart_logo.png")
    
    # Create the background image CSS with inline data URL
    bg_image_base64 = get_base64_encoded_image(walmart_bg_path)
    bg_image_css = f"linear-gradient(rgba(0, 0, 51, 0.7), rgba(0, 0, 51, 0.7)), url('data:image/jpeg;base64,{bg_image_base64}')"
    
    # Create the logo image with inline data URL
    logo_base64 = get_base64_encoded_image(walmart_logo_path)
    
    # Create HTML with properly escaped curly braces for CSS
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
        <!-- Animated Floating Particles -->
        <div class="particle particle1"></div>
        <div class="particle particle2"></div>
        <div class="particle particle3"></div>
        <div class="particle particle4"></div>
        <div class="particle particle5"></div>
        
        <!-- Hero Content -->
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
            
            <!-- Animated Buttons -->
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
            
            <!-- Animated Wave Bottom -->
            <div class="wave-container">
                <div class="wave wave1"></div>
                <div class="wave wave2"></div>
            </div>
        </div>
        
        <!-- Moving Background Effect -->
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
    
    # CSS without f-string interpolation to avoid curly brace issues
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

def create_glassmorphism_card(content, title=None, icon=None):
    """Create a modern glassmorphism card"""
    title_html = f"""
    <div style="
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    ">
        {f'<span style="font-size: 24px; margin-right: 12px;">{icon}</span>' if icon else ''}
        <h3 style="
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 0;
            color: #2c3e50;
        ">{title}</h3>
    </div>
    """ if title else ""
    
    return f"""
    <div class="glass-card slide-up">
        {title_html}
        <div style="font-family: 'Inter', sans-serif; line-height: 1.6;">
            {content}
        </div>
    </div>
    """

def create_modern_metric_card(title, value, change=None, icon=None, color="primary"):
    """Create a modern metric card with animations"""
    colors = {
        "primary": "#0066cc",
        "success": "#10b981", 
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#3b82f6"
    }
    
    color_value = colors.get(color, colors['primary'])
    
    change_html = ""
    if change:
        change_color = "#10b981" if change.startswith('+') else "#ef4444"
        change_html = f"""
        <div style="
            color: {change_color};
            font-size: 0.875rem;
            font-weight: 600;
            margin-top: 8px;
            display: flex;
            align-items: center;
        ">
            <span style="margin-right: 4px;">
                {'↗️' if change.startswith('+') else '↘️'}
            </span>
            {change}
        </div>
        """
    
    return f"""
    <div class="metric-card bounce-in" style="border-left-color: {color_value};">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <div style="
                    font-family: 'Inter', sans-serif;
                    font-size: 0.875rem;
                    font-weight: 500;
                    color: #6b7280;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 8px;
                ">{title}</div>
                <div style="
                    font-family: 'Poppins', sans-serif;
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #1f2937;
                    line-height: 1;
                ">{value}</div>
                {change_html}
            </div>
            {f'<div style="font-size: 2rem; opacity: 0.7;">{icon}</div>' if icon else ''}
        </div>
    </div>
    """

def create_modern_button(text, key=None, type="primary", size="medium", full_width=False):
    """Create a modern animated button"""
    sizes = {
        "small": "padding: 8px 16px; font-size: 0.875rem;",
        "medium": "padding: 12px 24px; font-size: 1rem;",
        "large": "padding: 16px 32px; font-size: 1.125rem;"
    }
    
    width_style = "width: 100%;" if full_width else ""
    
    button_html = f"""
    <button class="modern-button" style="
        {sizes.get(size, sizes['medium'])}
        {width_style}
    " onclick="document.getElementById('{key or "btn"}').click();">
        {text}
    </button>
    """
    
    return button_html

def create_status_badge(text, status="success"):
    """Create a modern status badge"""
    return f'<span class="status-badge status-{status}">{text}</span>'

def create_modern_progress_bar(percentage, color="primary", height="8px"):
    """Create a modern animated progress bar"""
    return f"""
    <div class="modern-progress" style="height: {height};">
        <div class="modern-progress-bar" style="width: {percentage}%;"></div>
    </div>
    """

def create_feature_grid(features):
    """Create a responsive feature grid"""
    feature_cards = ""
    for feature in features:
        feature_cards += f"""
        <div class="glass-card">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 3rem; margin-bottom: 16px;">
                    {feature.get('icon', '✨')}
                </div>
                <h3 style="
                    font-family: 'Poppins', sans-serif;
                    font-size: 1.25rem;
                    font-weight: 600;
                    margin: 0 0 12px 0;
                    color: #1f2937;
                ">{feature.get('title', 'Feature')}</h3>
                <p style="
                    font-family: 'Inter', sans-serif;
                    color: #6b7280;
                    line-height: 1.6;
                    margin: 0;
                ">{feature.get('description', 'Feature description')}</p>
            </div>
        </div>
        """
    
    return f'<div class="grid-responsive">{feature_cards}</div>'

def create_navigation_pills(tabs, selected_tab=0):
    """Create modern navigation pills"""
    pills = ""
    for i, tab in enumerate(tabs):
        active_style = """
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        """ if i == selected_tab else """
            background: white;
            color: #6b7280;
            border: 1px solid #e5e7eb;
        """
        
        pills += f"""
        <div style="
            {active_style}
            padding: 12px 24px;
            border-radius: 25px;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 0 8px;
            display: inline-block;
        ">{tab}</div>
        """
    
    return f'<div style="text-align: center; margin: 30px 0;">{pills}</div>'
    """Get grid container styling"""
    return """
    display: grid; 
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
    gap: 15px; 
    margin: 20px 0;
    """

def get_button_style(color="#007bff"):
    """Get button styling"""
    return f"""
    background: {color};
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s ease;
    """

def get_metric_style(color="#28a745"):
    """Get metric display styling"""
    return f"""
    background: {color};
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    text-align: center;
    """

def create_clean_inventory_card(product_name, sku, quantity, min_stock, price, product_info):
    """Create a clean inventory card without visible styling"""
    stock_status = "🔴 Low Stock" if quantity < min_stock else "🟢 In Stock"
    status_color = "#dc3545" if quantity < min_stock else "#28a745"
    border_color = "#dc3545" if quantity < min_stock else "#ddd"
    
    card_style = f"""
    <div style="{get_inventory_card_style(quantity < min_stock)}">
        <img src="{product_info['image_url']}" 
             alt="{product_name}" 
             style="{get_image_style()}; width: 100%; height: 120px; margin-bottom: 10px;">
        
        <h5 style="margin: 5px 0; color: {COMMON_STYLES['text_color']}; font-size: 14px;">{product_name}</h5>
        <p style="margin: 2px 0; color: {COMMON_STYLES['secondary_color']}; font-size: 12px;"><strong>SKU:</strong> {sku}</p>
        
        <div style="{get_metric_style(status_color)}; margin: 5px 0;">
            <strong>{stock_status}</strong>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 8px; font-size: 11px;">
            <div style="background: {COMMON_STYLES['light_bg']}; padding: 4px; border-radius: 4px; text-align: center;">
                <strong>Stock: {quantity}</strong>
            </div>
            <div style="background: {COMMON_STYLES['light_bg']}; padding: 4px; border-radius: 4px; text-align: center;">
                <strong>Min: {min_stock}</strong>
            </div>
        </div>
        
        <div style="background: #e9ecef; padding: 4px; border-radius: 4px; text-align: center; margin-top: 5px; font-size: 11px;">
            <strong>Price: ${price:.2f}</strong>
        </div>
    </div>
    """
    return card_style

def create_simple_inventory_display(inventory_items, max_items=9):
    """Create a simple inventory display without visible styling code"""
    display_html = ""
    
    for i, item in enumerate(inventory_items[:max_items]):
        product_name = item.get('product_name', item.get('name', 'Unknown Product'))
        sku = item.get('sku', 'N/A')
        quantity = item.get('stock_quantity', item.get('quantity', 0))
        min_stock = item.get('min_stock_level', 10)
        price = item.get('price', 0.0)
        
        # Simple text display instead of complex HTML
        stock_status = "🔴 Low Stock" if quantity < min_stock else "🟢 In Stock"
        
        simple_card = f"""
        **{product_name}**  
        SKU: {sku} | Stock: {quantity} | Min: {min_stock} | Price: ${price:.2f}  
        Status: {stock_status}
        
        ---
        """
        display_html += simple_card
    
    return display_html

# Common styling constants
COMMON_STYLES = {
    'text_color': '#2c3e50',
    'secondary_color': '#7f8c8d',
    'success_color': '#28a745',
    'warning_color': '#ffc107',
    'danger_color': '#dc3545',
    'primary_color': '#007bff',
    'light_bg': '#f8f9fa',
    'white_bg': '#ffffff'
}
