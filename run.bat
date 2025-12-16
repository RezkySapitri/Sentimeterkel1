@echo off
REM ====================================================
REM E-Learning Recommendation System - Startup Script
REM ====================================================

echo.
echo ========================================
echo  E-Learning Recommendation System
echo  Powered by Q-Learning
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)
echo.

REM Check if data file exists
if not exist "student_info.csv" (
    echo WARNING: student_info.csv not found
    echo You will need to upload the CSV file through the web interface
    echo.
)

REM Run the application
echo Starting Streamlit application...
echo.
echo ========================================
echo  Application will open in your browser
echo  URL: http://localhost:8501
echo ========================================
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run elearning_recommendation_app.py

REM Deactivate virtual environment on exit
deactivate
