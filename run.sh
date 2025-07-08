#!/bin/bash

echo "============================================="
echo " 🛒 Walmart Logistics Dashboard - Enhanced"
echo "============================================="
echo

# Check if Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check for virtual environment
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Check if requirements are installed
echo "📦 Checking and installing requirements..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install requirements"
    exit 1
fi

# Create data directory if it doesn't exist
if [ ! -d "data" ]; then
    mkdir -p data
fi

echo
echo "✅ Setup complete!"
echo "🚀 Starting Walmart Logistics Dashboard..."
echo
echo "💻 Access the dashboard at http://localhost:8501"
echo "🔐 Default admin login: username=admin, password=admin123"
echo
echo "📝 Press Ctrl+C to stop the application"
echo "============================================="
echo

streamlit run app.py

# Deactivate virtual environment when done
deactivate
