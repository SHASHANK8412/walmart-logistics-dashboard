@echo off
echo Starting Walmart Logistics Dashboard...
echo.
echo This script uses a direct path to run the application to avoid blank page issues
echo.

cd /d "%~dp0"
streamlit run app.py

pause
