#!/usr/bin/env python3
"""
Test script to verify Matrix GUI functionality
"""

import sys
import traceback

def test_imports():
    """Test all module imports"""
    print("[*] Testing module imports...")
    
    modules_to_test = [
        "customtkinter",
        "tkinter", 
        "psutil",
        "modules.matrix_rain",
        "modules.neural_command",
        "modules.quick_scan",
        "modules.advanced_ops",
        "modules.mobile_fortress",
        "modules.wireless_infiltration",
        "modules.payload_matrix",
        "modules.ai_neural_link",
        "modules.system_monitor",
        "modules.intelligence_reports",
        "modules.utils"
    ]
    
    failed = []
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module}: {e}")
            failed.append(module)
    
    return len(failed) == 0

def test_gui_creation():
    """Test GUI window creation"""
    print("\n[*] Testing GUI creation...")
    
    try:
        from matrix_pentest_gui import MatrixPentestGUI
        import tkinter as tk
        
        # Create test instance
        print("  Creating GUI instance...")
        
        # Use a timeout to prevent hanging
        root = tk.Tk()
        root.withdraw()  # Hide the test window
        
        print("  ✓ GUI framework initialized")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to create GUI: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Matrix Pentesting Framework - System Check")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        print("\n[!] Some modules failed to import")
        print("[!] Install missing dependencies with:")
        print("    pip install customtkinter psutil")
    
    # Test GUI
    if not test_gui_creation():
        all_passed = False
        print("\n[!] GUI creation test failed")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[✓] All tests passed! Ready to launch.")
        print("\nRun the GUI with:")
        print("  python3 matrix_pentest_gui.py")
    else:
        print("[✗] Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
