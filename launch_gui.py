#!/usr/bin/env python3
"""
AutoPenTest GUI Launcher
Launch the modern GUI interface for the NLP-driven pentesting framework
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
    """Main entry point for GUI launcher."""
    print("🔥 AutoPenTest Framework - GUI Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies found")
    print("🚀 Launching GUI interface...")
    
    try:
        # Import and run GUI
        sys.path.insert(0, str(src_path))
        from gui.main_window import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Failed to import GUI module: {e}")
        print("💡 Make sure all dependencies are installed and src/gui/main_window.py exists")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to launch GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
