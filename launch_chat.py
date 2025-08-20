#!/usr/bin/env python3
"""
AutoPenTest Chat Interface Launcher
Launch the ChatGPT-style conversational interface for NLP pentesting
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def check_dependencies():
    """Check if all required dependencies are installed."""
    missing = []
    
    try:
        import PyQt6
        print("✅ PyQt6 found")
    except ImportError:
        missing.append("PyQt6")
    
    if missing:
        print("❌ Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n💡 Install missing dependencies:")
        print("   pip install PyQt6")
        return False
    
    return True

def main():
    """Main entry point for chat GUI launcher."""
    print("💬 AutoPenTest Chat Interface - Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("🚀 Starting ChatGPT-style pentesting interface...")
    print("📝 Type natural language requests to interact with the AI")
    print("🔍 Example: 'Find vulnerabilities in example.com'")
    print()
    
    try:
        # Import and run chat GUI
        sys.path.insert(0, str(src_path))
        from gui.chat_window import main as chat_main
        chat_main()
    except ImportError as e:
        print(f"❌ Failed to import chat interface: {e}")
        print("💡 Make sure PyQt6 is installed and src/gui/chat_window.py exists")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to launch chat interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
