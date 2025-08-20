#!/bin/bash
#
# REAL-TIME PENTESTING CHATBOT LAUNCHER
# WARNING: This executes REAL hacking tools!
#

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       REAL-TIME PENETRATION TESTING CHATBOT LAUNCHER        ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  ⚠️  WARNING: This tool executes REAL hacking commands!      ║"
echo "║  ⚠️  Use ONLY on systems you own or have permission to test! ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Not running as root. Some features may be limited."
    echo "   For full functionality, run: sudo ./launch_chatbot.sh"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

# Navigate to script directory
cd "$(dirname "$0")"

# Launch the chatbot
echo "🚀 Launching Real-Time Pentesting Chatbot..."
echo "=" * 70
python3 realtime_pentest_chatbot.py

# If GUI fails, try with system python
if [ $? -ne 0 ]; then
    echo "Trying alternative Python..."
    /usr/bin/python3 realtime_pentest_chatbot.py
fi
