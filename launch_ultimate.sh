#!/bin/bash

# PentestGPT Ultimate Launcher Script
# Comprehensive AI Penetration Testing Suite

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🔒 PentestGPT Ultimate - AI Pentesting Suite       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Starting comprehensive penetration testing assistant..."
echo ""

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi

# Check for tkinter
python -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Tkinter not found. Installing..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm tk
    elif command -v apt &> /dev/null; then
        sudo apt-get install -y python3-tk
    fi
fi

# Optional: Check for common pentesting tools
echo "🔍 Checking available tools..."
tools=("nmap" "nikto" "gobuster" "sqlmap" "hydra" "john" "hashcat" "metasploit")
available_tools=()
missing_tools=()

for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        available_tools+=($tool)
    else
        missing_tools+=($tool)
    fi
done

echo "✅ Available tools: ${available_tools[@]}"
if [ ${#missing_tools[@]} -gt 0 ]; then
    echo "⚠️  Missing tools: ${missing_tools[@]}"
    echo "   Install missing tools for full functionality"
fi
echo ""

# Check for spaCy
python -c "import spacy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing spaCy for enhanced NLP..."
    pip install spacy --break-system-packages 2>/dev/null || pip install spacy
    python -m spacy download en_core_web_sm 2>/dev/null || true
fi

# Create reports directory if it doesn't exist
mkdir -p reports 2>/dev/null

# Launch PentestGPT Ultimate
echo "🚀 Launching PentestGPT Ultimate..."
echo ""
python pentestgpt_ultimate.py

# Check exit status
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application exited with an error"
    echo "   Please check the error messages above"
    exit 1
fi

echo ""
echo "👋 Thank you for using PentestGPT Ultimate!"
