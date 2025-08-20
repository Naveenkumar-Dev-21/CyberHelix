#!/usr/bin/env python3
"""
Run the Matrix Attack System
Cyberpunk UI for real penetration testing
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from src.matrix_pentest_ui import main
        main()
    except KeyboardInterrupt:
        print("\n[!] Exiting Matrix...")
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
