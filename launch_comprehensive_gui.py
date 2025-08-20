#!/usr/bin/env python3
"""
Launcher for Comprehensive Automatic Pentesting GUI
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))

# Check for required packages
required_packages = []
try:
    from PyQt6.QtWidgets import QApplication
except ImportError:
    required_packages.append("PyQt6")

if required_packages:
    print("⚠️  Missing required packages:")
    for pkg in required_packages:
        print(f"  - {pkg}")
    print("\n📦 Install with: pip install " + " ".join(required_packages))
    print("\nOr install all requirements: pip install -r requirements.txt")
    sys.exit(1)

# Import and run the GUI
try:
    from comprehensive_gui import main
    
    print("🚀 Launching Comprehensive Pentesting GUI...")
    print("=" * 50)
    print("✅ REAL CAPABILITIES:")
    print("  • Network Penetration Testing (Nmap, Service Enum)")
    print("  • Web Application Testing (Nuclei, Nikto, SQLMap)")
    print("  • Mobile App Analysis (MobSF, Frida, Drozer)")
    print("  • Wireless Testing (Aircrack-ng suite)")
    print("  • Exploitation (FTP, SSH, Web exploits)")
    print("  • AI-Powered Assistant")
    print("=" * 50)
    print("⚠️  Use only on authorized targets!")
    print()
    
    main()
    
except ImportError as e:
    print(f"❌ Error importing GUI: {e}")
    print("\nTrying alternative import...")
    
    # Try direct execution
    import subprocess
    gui_file = project_root / "comprehensive_gui.py"
    if gui_file.exists():
        subprocess.run([sys.executable, str(gui_file)])
    else:
        print("❌ Could not find comprehensive_gui.py")
        print("Please ensure the file exists in the project directory")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
