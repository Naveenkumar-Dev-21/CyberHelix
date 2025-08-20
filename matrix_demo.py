#!/usr/bin/env python3
"""
Matrix GUI Demo - Showcase the cyberpunk features
"""

import sys
import time
from pathlib import Path

def display_matrix_banner():
    """Display Matrix-style banner"""
    banner = """
🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

        ████████ ██   ██ ███████     ███    ███  █████  ████████ ██████  ██ ██   ██ 
           ██    ██   ██ ██          ████  ████ ██   ██    ██    ██   ██ ██  ██ ██  
           ██    ███████ █████       ██ ████ ██ ███████    ██    ██████  ██   ███   
           ██    ██   ██ ██          ██  ██  ██ ██   ██    ██    ██   ██ ██  ██ ██  
           ██    ██   ██ ███████     ██      ██ ██   ██    ██    ██   ██ ██ ██   ██ 

                    NEURAL PENETRATION INTERFACE v3.0
                         Powered by Zion Resistance

🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴

"""
    print(banner)

def simulate_boot_sequence():
    """Simulate Matrix boot sequence"""
    messages = [
        "🔴 Initializing neural pathways...",
        "🧠 Loading quantum encryption protocols...", 
        "📡 Establishing connection to Zion mainframe...",
        "⚡ Activating digital rain generators...",
        "🎯 Calibrating penetration testing modules...",
        "🖥️ Starting Matrix terminal interface...",
        "✅ SYSTEM READY - WELCOME TO THE MATRIX"
    ]
    
    for msg in messages:
        print(f"\n{msg}")
        time.sleep(0.8)

def show_features():
    """Show Matrix GUI features"""
    features = {
        "🌧️ Digital Rain Effect": "Animated Matrix-style falling characters (Japanese katakana)",
        "🎨 Cyberpunk Aesthetics": "Dark theme with neon green/red colors and glow effects",
        "🖥️ Matrix Terminal": "Terminal with typing animation and syntax highlighting",
        "🔴 Red Pill Interface": "Execute pentesting missions with Matrix-themed commands",
        "📊 Neural Statistics": "Real-time stats with cyberpunk terminology",
        "🎯 Mission Control": "Natural language pentesting with Matrix references",
        "⚡ Quick Missions": "Pre-configured hacking scenarios",
        "🧠 Neural Knowledge": "AI learning system with Matrix terminology",
        "🔊 Matrix Language": "All interface text uses Matrix/cyberpunk themes"
    }
    
    print("\n" + "="*70)
    print("🔴 MATRIX GUI FEATURES:")
    print("="*70)
    
    for feature, description in features.items():
        print(f"\n{feature}")
        print(f"   {description}")
    
    print("\n" + "="*70)

def show_demo_commands():
    """Show example Matrix commands"""
    commands = [
        "🔍 Infiltrate the mainframe at target.matrix and extract all vulnerabilities",
        "📡 Deploy reconnaissance drones on network 192.168.1.0/24 with stealth mode",
        "📱 Analyze mobile construct banking_app.apk for security breaches", 
        "🕳️ Perform deep vulnerability scan on oracle.zion with neural enhancement",
        "📶 Scan for wireless access points and capture authentication handshakes",
        "🎯 Execute complete penetration test on example.com with Agent Smith evasion"
    ]
    
    print("\n🎯 EXAMPLE NEURAL COMMANDS:")
    print("-" * 50)
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n{i}. {cmd}")
    
    print("\n💡 The Matrix GUI translates natural language into technical pentesting operations!")

def show_matrix_terminology():
    """Show Matrix-themed terminology mapping"""
    terms = {
        "User Input": "Neural Command",
        "Enhanced AI": "Enhanced Neural Link", 
        "System Processes": "Neural Pathways",
        "Target Environment": "The Construct",
        "Security Defenses": "Agent Smith",
        "Execute Button": "Red Pill",
        "Target System": "The Matrix",
        "Safe Systems": "Zion Network",
        "Warnings": "Sentinel Alerts",
        "Vulnerabilities": "Security Breaches",
        "Discovered Targets": "Infiltrated Systems",
        "Progress": "Neural Link Strength"
    }
    
    print("\n🧠 MATRIX TERMINOLOGY MAPPING:")
    print("-" * 50)
    
    for normal, matrix in terms.items():
        print(f"  {normal:<20} → {matrix}")

def main():
    """Main demo function"""
    display_matrix_banner()
    
    print("🔴 Welcome to The Matrix - Neural Penetration Interface Demo")
    print("🧠 This showcases our Matrix-themed GUI for the AutoPenTest Framework\n")
    
    # Boot sequence
    print("Initiating boot sequence...")
    simulate_boot_sequence()
    
    # Show features
    show_features()
    
    # Show commands
    show_demo_commands()
    
    # Show terminology
    show_matrix_terminology()
    
    print(f"\n{'='*70}")
    print("🚀 TO LAUNCH THE MATRIX GUI:")
    print("="*70)
    print("   python3 launch_matrix.py")
    print("\n📋 REQUIREMENTS:")
    print("   • PyQt6 (pip install PyQt6)")
    print("   • Python 3.7+")
    print("\n🎬 DEMO MODE:")
    print("   • GUI works in demo mode without core framework")
    print("   • Simulates realistic pentesting operations")
    print("   • Full visual effects and Matrix theming")
    
    print(f"\n{'='*70}")
    print("🔴 Remember: There is no spoon... but there are vulnerabilities to find!")
    print("💊 Take the red pill and see how deep the rabbit hole goes...")
    print("='*70")

if __name__ == "__main__":
    main()
