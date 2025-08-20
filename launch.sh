#!/bin/bash

# Automatic Pentesting System Launcher
# This script starts the backend server and PyQt6 GUI

echo "==============================================="
echo "🚀 AUTOMATIC PENTESTING SYSTEM LAUNCHER"
echo "==============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓ Virtual environment found${NC}"
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo -e "${GREEN}✓ Virtual environment found${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠ No virtual environment found, using system Python${NC}"
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down...${NC}"
    
    # Kill backend server if running
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo -e "${GREEN}✓ Backend server stopped${NC}"
    fi
    
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Check if backend is already running
if check_port 8000; then
    echo -e "${YELLOW}⚠ Backend server already running on port 8000${NC}"
    BACKEND_RUNNING=true
else
    # Start backend server
    echo -e "${YELLOW}🔧 Starting backend server...${NC}"
    python backend_server.py > backend.log 2>&1 &
    BACKEND_PID=$!
    
    # Wait for backend to start
    sleep 3
    
    if check_port 8000; then
        echo -e "${GREEN}✓ Backend server started on port 8000${NC}"
        BACKEND_RUNNING=true
    else
        echo -e "${RED}❌ Failed to start backend server${NC}"
        echo "Check backend.log for errors"
        exit 1
    fi
fi

# Check PyQt6
echo -e "${YELLOW}🔍 Checking PyQt6...${NC}"
if python -c "from PyQt6.QtWidgets import QApplication" 2>/dev/null; then
    echo -e "${GREEN}✓ PyQt6 is installed${NC}"
else
    echo -e "${RED}❌ PyQt6 is not installed${NC}"
    echo "Install with: pip install PyQt6"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    exit 1
fi

echo ""
echo "==============================================="
echo -e "${GREEN}✨ SYSTEM READY${NC}"
echo "==============================================="
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "🖥️  Starting GUI..."
echo ""
echo "💡 TIP: Use natural language commands like:"
echo '   "Test example.com for vulnerabilities"'
echo '   "Scan 192.168.1.0/24 network"'
echo '   "Analyze mobile app.apk"'
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start GUI
python src/gui.py

# Cleanup will be triggered when GUI closes
cleanup
