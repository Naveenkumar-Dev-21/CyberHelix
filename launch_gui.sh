#!/bin/bash
# Launcher script for Automatic Pentesting Tool GUI

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║  Starting Automatic Pentesting Tool GUI                          ║"
echo "║  Professional Automated Penetration Testing Framework            ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if running with display
if [ -z "$DISPLAY" ]; then
    echo "⚠️  Warning: No display detected. Setting DISPLAY=:0"
    export DISPLAY=:0
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check tkinter availability
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: tkinter is not installed"
    echo "Install with: sudo apt-get install python3-tk"
    exit 1
fi

# Set the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
fi

# Launch the GUI
echo "🚀 Launching GUI..."
echo ""
python3 pentesting_gui.py "$@"
