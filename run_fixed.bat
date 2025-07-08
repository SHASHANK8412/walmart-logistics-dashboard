@echo off
echo Starting Fixed Walmart Logistics Dashboard...
echo.
echo This script runs a simplified version of the dashboard
echo that doesn't rely on loading image files
echo.

cd /d "%~dp0"
streamlit run fixed_app.py

pause
