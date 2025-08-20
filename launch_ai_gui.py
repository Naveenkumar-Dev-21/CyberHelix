#!/usr/bin/env python3
"""
AI-Powered AutoPenTest GUI Launcher
Launch the Matrix-style GUI with integrated AI and NLP capabilities
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def check_system():
    """Check if the AI system is properly trained and ready."""
    print("🔍 Checking AI System Status...")
    
    checks = {
        "PyQt6": False,
        "AI Model": False,
        "NLP Processor": False,
        "Config": False
    }
    
    # Check PyQt6
    try:
        import PyQt6
        checks["PyQt6"] = True
        print("✅ PyQt6 installed")
    except ImportError:
        print("❌ PyQt6 not found")
    
    # Check AI Model
    try:
        from ai_model import IntentClassifierModel
        model = IntentClassifierModel()
        if model.load_model():
            checks["AI Model"] = True
            print("✅ AI Model loaded")
        else:
            print("❌ AI Model not trained - run train_system.py first")
    except Exception as e:
        print(f"❌ AI Model error: {e}")
    
    # Check NLP Processor
    try:
        from enhanced_nlp_processor import EnhancedNLPProcessor
        nlp = EnhancedNLPProcessor()
        checks["NLP Processor"] = True
        print("✅ NLP Processor ready")
    except Exception as e:
        print(f"❌ NLP Processor error: {e}")
    
    # Check Config
    try:
        from config import Config
        checks["Config"] = True
        print("✅ Configuration loaded")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    return all(checks.values()), checks

def launch_standard_gui():
    """Launch the standard modern GUI."""
    print("\n🚀 Launching Standard GUI...")
    
    try:
        from gui.main_window import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Failed to launch standard GUI: {e}")
        return False
    return True

def launch_matrix_gui():
    """Launch the Matrix-themed GUI."""
    print("\n🎬 Launching Matrix GUI...")
    
    try:
        from gui.matrix_gui import MatrixGUI
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        
        # Dark theme
        app.setStyle("Fusion")
        
        window = MatrixGUI()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"❌ Failed to launch Matrix GUI: {e}")
        return False
    return True

def main():
    """Main entry point for AI-powered GUI launcher."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        🤖 AI-POWERED AUTOMATIC PENTESTING SYSTEM 🤖          ║
║                    GUI LAUNCHER v2.0                         ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check system status
    system_ready, checks = check_system()
    
    if not system_ready:
        print("\n⚠️ System not fully ready!")
        print("Please ensure:")
        print("  1. Run 'python train_system.py' to train the AI model")
        print("  2. Install PyQt6: pip install PyQt6")
        print("  3. Check configuration files")
        
        response = input("\nTry to launch anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("\n✅ All systems operational!")
    
    # Choose GUI mode
    print("\n📋 Select GUI Mode:")
    print("  1. Standard Modern GUI (Clean, professional)")
    print("  2. Matrix GUI (Cyberpunk theme with digital rain)")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        launch_standard_gui()
    elif choice == "2":
        launch_matrix_gui()
    elif choice == "3":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice")
        sys.exit(1)

if __name__ == "__main__":
    main()
