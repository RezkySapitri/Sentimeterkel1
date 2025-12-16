#!/bin/bash
# ====================================================
# E-Learning Recommendation System - Startup Script
# ====================================================

echo ""
echo "========================================"
echo " E-Learning Recommendation System"
echo " Powered by Q-Learning"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Python is installed"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip --quiet

# Check if requirements are installed
echo "Checking dependencies..."
if ! pip show streamlit &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo -e "${GREEN}[OK]${NC} Dependencies installed"
else
    echo -e "${GREEN}[OK]${NC} Dependencies already installed"
fi
echo ""

# Check if data file exists
if [ ! -f "student_info.csv" ]; then
    echo -e "${YELLOW}WARNING:${NC} student_info.csv not found"
    echo "You will need to upload the CSV file through the web interface"
    echo ""
fi

# Run the application
echo "Starting Streamlit application..."
echo ""
echo "========================================"
echo " Application will open in your browser"
echo " URL: http://localhost:8501"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run elearning_recommendation_app.py

# Deactivate virtual environment on exit
deactivate
