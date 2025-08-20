#!/bin/bash

# Matrix Pentesting Desktop Application Launcher
# Ensures all dependencies are installed and starts the application

echo "╔══════════════════════════════════════════════════════╗"
echo "║     MATRIX PENTESTING SUITE - DESKTOP LAUNCHER      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo -e "${GREEN}✓ Python $python_version detected${NC}"
else
    echo -e "${RED}✗ Python 3.8+ required. Current version: $python_version${NC}"
    exit 1
fi

# Function to check if package is installed
check_package() {
    python3 -c "import $1" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 installed${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ $1 not installed${NC}"
        return 1
    fi
}

# Check required packages
echo ""
echo "Checking required packages..."
packages=("fastapi" "uvicorn" "aiohttp" "websockets" "customtkinter" "pywebview" "requests")
missing_packages=()

for package in "${packages[@]}"; do
    if ! check_package "$package"; then
        missing_packages+=("$package")
    fi
done

# Install missing packages
if [ ${#missing_packages[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Installing missing packages...${NC}"
    pip install --break-system-packages ${missing_packages[@]}
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install packages. Please install manually:${NC}"
        echo "pip install --break-system-packages ${missing_packages[@]}"
        exit 1
    fi
fi

# Check if backend dependencies are available
echo ""
echo "Checking backend modules..."
if [ -d "src" ]; then
    echo -e "${GREEN}✓ Backend modules found${NC}"
else
    echo -e "${RED}✗ Backend modules not found. Please ensure src/ directory exists${NC}"
    exit 1
fi

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p output logs reports assets src/gui
echo -e "${GREEN}✓ Directories created${NC}"

# Check for existing backend process
echo ""
echo "Checking for existing backend processes..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Port 8000 is already in use${NC}"
    read -p "Kill existing process? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill $(lsof -t -i:8000) 2>/dev/null
        sleep 2
        echo -e "${GREEN}✓ Existing process terminated${NC}"
    fi
fi

# Launch the application
echo ""
echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}Launching Matrix Pentesting Desktop Application...${NC}"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to exit"
echo ""

# Start the desktop application
python3 desktop_app.py

# Cleanup on exit
echo ""
echo -e "${YELLOW}Shutting down...${NC}"
echo -e "${GREEN}Thank you for using Matrix Pentesting Suite!${NC}"
