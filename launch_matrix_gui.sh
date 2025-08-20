#!/bin/bash

# Matrix Pentesting Framework - Launch Script
# This script ensures all dependencies are installed and launches the GUI

echo "═══════════════════════════════════════════════════════════════"
echo "           MATRIX PENTESTING FRAMEWORK v3.0                    "
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "[*] Checking Python installation..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "[✓] Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "[*] Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install requirements
echo "[*] Installing requirements..."
pip install customtkinter psutil > /dev/null 2>&1

# Check if running as root (optional for some features)
if [ "$EUID" -ne 0 ]; then 
    echo "[!] Warning: Not running as root. Some features may be limited."
    echo "[!] For full functionality, run: sudo $0"
fi

echo ""
echo "[*] Launching Matrix Pentesting Framework..."
echo "[*] Wake up, Neo... The Matrix has you..."
echo ""

# Launch the GUI
python3 matrix_pentest_gui.py

# Deactivate virtual environment when done
deactivate
