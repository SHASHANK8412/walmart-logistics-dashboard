@echo off
echo.
echo =====================================================
echo Walmart Logistics Dashboard - Simple Test Application
echo =====================================================
echo.
echo This batch file will run a simple Streamlit application 
echo to verify if Streamlit is working correctly.
echo.

cd /d "%~dp0"
echo Running from directory: %cd%
echo.
echo Press any key to continue...
pause > nul

echo.
echo Creating simple test file...
echo import streamlit as st > simple.py
echo st.title("Walmart Logistics Dashboard Test") >> simple.py
echo st.write("If you can see this text, Streamlit is working correctly!") >> simple.py
echo st.success("Success! The application is running.") >> simple.py
echo if st.button("Click Me"): >> simple.py
echo     st.balloons() >> simple.py
echo     st.write("Button clicked!") >> simple.py

echo.
echo Running simple Streamlit application...
streamlit run simple.py

echo.
echo Press any key to exit...
pause > nul
del simple.py
