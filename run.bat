@echo off
echo =============================================
echo  🛒 Walmart Logistics Dashboard - Enhanced
echo =============================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

REM Check for virtual environment
if not exist .venv (
    echo 🔧 Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if requirements are installed
echo 📦 Checking and installing requirements...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

REM Create data directory if it doesn't exist
if not exist data mkdir data

echo.
echo ✅ Setup complete!
echo 🚀 Starting Walmart Logistics Dashboard...
echo.
echo 💻 Access the dashboard at http://localhost:8501
echo 🔐 Default admin login: username=admin, password=admin123
echo.
echo 📝 Press Ctrl+C to stop the application
echo =============================================
echo.

streamlit run app.py

REM Deactivate virtual environment when done
call deactivate
