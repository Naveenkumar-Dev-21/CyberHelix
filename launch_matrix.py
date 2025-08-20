#!/usr/bin/env python3
"""
Launch script for The Matrix - Neural Penetration Interface
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

try:
    from gui.matrix_gui import main
    
    if __name__ == "__main__":
        print("🔴 Initializing The Matrix...")
        print("🧠 Loading neural pathways...")
        print("⚡ Activating digital rain...")
        print("🎯 Ready for infiltration!\n")
        
        main()
        
except ImportError as e:
    print(f"❌ Error: Could not import Matrix GUI: {e}")
    print("📦 Please ensure PyQt6 is installed:")
    print("   pip install PyQt6")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
