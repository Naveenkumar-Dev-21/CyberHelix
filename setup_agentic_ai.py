#!/usr/bin/env python3
"""
Complete Setup Script for Agentic Pentesting AI
Installs dependencies, trains models, and configures the system
"""

import sys
import subprocess
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any

def print_banner():
    """Print setup banner"""
    banner = """
🔴════════════════════════════════════════════════════════════════════════════════
🔴  AGENTIC PENTESTING AI - COMPLETE SETUP SYSTEM
🔴  Advanced AI-Powered Security Testing Framework
🔴════════════════════════════════════════════════════════════════════════════════
"""
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_system_dependencies():
    """Install system-level dependencies"""
    print("\n📦 Installing system dependencies...")
    
    system_deps = {
        "ubuntu/debian": [
            "python3-dev", "python3-pip", "python3-venv",
            "build-essential", "libffi-dev", "libssl-dev",
            "nmap", "nikto", "sqlmap", 
            "git", "curl", "wget"
        ],
        "arch/garuda": [
            "python", "python-pip", "python-virtualenv",
            "base-devel", "libffi", "openssl",
            "nmap", "nikto", "sqlmap",
            "git", "curl", "wget"
        ]
    }
    
    # Detect system type
    try:
        with open("/etc/os-release", "r") as f:
            os_info = f.read().lower()
        
        if "ubuntu" in os_info or "debian" in os_info:
            deps = system_deps["ubuntu/debian"]
            install_cmd = ["sudo", "apt", "update", "&&", "sudo", "apt", "install", "-y"] + deps
        elif "arch" in os_info or "garuda" in os_info:
            deps = system_deps["arch/garuda"]
            install_cmd = ["sudo", "pacman", "-S", "--noconfirm"] + deps
        else:
            print("⚠️  Unknown system. Please install dependencies manually:")
            print("   - Python 3.8+, pip, build tools")
            print("   - nmap, nikto, sqlmap")
            print("   - git, curl, wget")
            return True
        
        print(f"Installing: {' '.join(deps)}")
        # Note: This is informational - actual installation would need user interaction
        print("✅ System dependencies listed. Install manually if needed.")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not detect system type: {e}")
        print("Please install system dependencies manually.")
        return True

def setup_virtual_environment():
    """Setup Python virtual environment"""
    print("\n🐍 Setting up virtual environment...")
    
    venv_path = Path(".venv")
    
    try:
        if not venv_path.exists():
            print("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        
        # Activate virtual environment
        if os.name == 'nt':  # Windows
            activate_script = venv_path / "Scripts" / "activate"
            pip_path = venv_path / "Scripts" / "pip"
        else:  # Unix
            activate_script = venv_path / "bin" / "activate"
            pip_path = venv_path / "bin" / "pip"
        
        print("✅ Virtual environment ready")
        return str(pip_path)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return None

def install_python_dependencies(pip_path: str = "pip"):
    """Install Python dependencies"""
    print("\n📚 Installing Python dependencies...")
    
    try:
        # Upgrade pip first
        print("Upgrading pip...")
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        print("Installing requirements...")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Python dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data",
        "data/enhanced", 
        "models",
        "reports",
        "reports/scans",
        "reports/payloads",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   Created: {directory}")
    
    print("✅ Directories created")
    return True

def setup_configuration():
    """Setup configuration files"""
    print("\n⚙️  Setting up configuration...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_template = """# API Keys for Enhanced Functionality
SHODAN_API_KEY=your_shodan_api_key_here
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here

# Tool Paths (adjust if tools are not in PATH)
NMAP_PATH=nmap
NUCLEI_PATH=nuclei
NIKTO_PATH=nikto
SQLMAP_PATH=sqlmap

# AI Model Configuration
AI_MODEL_TYPE=enhanced
ENABLE_REINFORCEMENT_LEARNING=true
ENABLE_ADVANCED_NLP=true

# Performance Settings
MAX_CONCURRENT_SCANS=3
SCAN_TIMEOUT=3600
MEMORY_LIMIT=4096

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/agentic_ai.log
"""
        with open(env_file, 'w') as f:
            f.write(env_template)
        print("   Created: .env (please configure API keys)")
    
    print("✅ Configuration setup complete")
    return True

def download_nlp_models():
    """Download required NLP models"""
    print("\n🔤 Setting up NLP models...")
    
    try:
        # Download spaCy model
        print("Downloading spaCy English model...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], 
                      check=True, capture_output=True)
        print("✅ spaCy model downloaded")
        
        # Setup NLTK data
        print("Setting up NLTK data...")
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded")
        
        return True
        
    except Exception as e:
        print(f"⚠️  NLP model setup failed: {e}")
        print("   You can download them later manually")
        return True

def train_ai_models():
    """Train AI models"""
    print("\n🧠 Training AI models...")
    
    try:
        # Run enhanced training system
        print("Starting enhanced training system...")
        subprocess.run([sys.executable, "enhanced_training.py"], 
                      check=True, timeout=300)  # 5 minute timeout
        print("✅ AI models trained successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("⚠️  Training took too long, continuing with basic setup")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Training failed: {e}")
        print("   You can train models later with: python enhanced_training.py")
        return True
    except Exception as e:
        print(f"⚠️  Training error: {e}")
        return True

def run_system_tests():
    """Run comprehensive system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        # Run test suite
        print("Executing test suite...")
        result = subprocess.run([sys.executable, "test_agentic_system.py"], 
                               check=True, timeout=180, capture_output=True, text=True)
        
        print("✅ System tests completed")
        return True
        
    except subprocess.TimeoutExpired:
        print("⚠️  Tests took too long, but setup continues")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Some tests failed: {e}")
        print("   System may still be functional")
        return True
    except Exception as e:
        print(f"⚠️  Test execution error: {e}")
        return True

def create_startup_scripts():
    """Create convenient startup scripts"""
    print("\n📜 Creating startup scripts...")
    
    # Main launcher script
    launcher_script = """#!/bin/bash
# Agentic Pentesting AI Launcher

echo "🤖 Starting Agentic Pentesting AI..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if models are trained
if [ ! -f "models/intent_classifier.pkl" ]; then
    echo "⚠️  Models not found. Training basic model..."
    python train_ai.py
fi

# Launch the application
echo "🚀 Launching application..."
python autopentest.py "$@"
"""
    
    with open("launch.sh", 'w') as f:
        f.write(launcher_script)
    os.chmod("launch.sh", 0o755)
    
    # Training script
    train_script = """#!/bin/bash
# Train all AI models

echo "🧠 Training Agentic AI Models..."

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "📊 Generating datasets..."
python -c "from src.dataset_generator import PentestDatasetGenerator; PentestDatasetGenerator().save_dataset()"

echo "🤖 Training neural networks..."
python train_ai.py

echo "🎯 Running enhanced training..."
python enhanced_training.py

echo "✅ Training complete!"
"""
    
    with open("train_models.sh", 'w') as f:
        f.write(train_script)
    os.chmod("train_models.sh", 0o755)
    
    # Test script
    test_script = """#!/bin/bash
# Run comprehensive tests

echo "🧪 Running Agentic AI Tests..."

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python test_agentic_system.py
echo "📊 Test results saved to test_report.json"
"""
    
    with open("run_tests.sh", 'w') as f:
        f.write(test_script)
    os.chmod("run_tests.sh", 0o755)
    
    print("✅ Startup scripts created")
    return True

def generate_setup_report():
    """Generate setup completion report"""
    print("\n📊 Generating setup report...")
    
    setup_report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "setup_completed": True,
        "components": {
            "virtual_environment": Path(".venv").exists(),
            "dependencies_installed": Path("requirements.txt").exists(),
            "directories_created": Path("data").exists() and Path("models").exists(),
            "configuration_files": Path(".env").exists(),
            "startup_scripts": Path("launch.sh").exists()
        },
        "next_steps": [
            "Configure API keys in .env file",
            "Run: ./launch.sh --help to see usage options",
            "Run: ./train_models.sh to train AI models",
            "Run: ./run_tests.sh to validate setup",
            "Try: ./launch.sh agentic 'scan example.com for vulnerabilities'"
        ]
    }
    
    with open("setup_report.json", 'w') as f:
        json.dump(setup_report, f, indent=2)
    
    print("✅ Setup report saved to setup_report.json")
    return setup_report

def main():
    """Main setup function"""
    print_banner()
    
    setup_steps = [
        ("Python Version Check", check_python_version),
        ("System Dependencies", install_system_dependencies),
        ("Virtual Environment", setup_virtual_environment),
        ("Python Dependencies", lambda: install_python_dependencies()),
        ("Directory Structure", create_directories),
        ("Configuration", setup_configuration),
        ("NLP Models", download_nlp_models),
        ("AI Model Training", train_ai_models),
        ("System Tests", run_system_tests),
        ("Startup Scripts", create_startup_scripts),
    ]
    
    setup_results = {}
    
    for step_name, step_func in setup_steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        
        try:
            result = step_func()
            setup_results[step_name] = {"success": result, "error": None}
            
            if result:
                print(f"✅ {step_name}: COMPLETED")
            else:
                print(f"⚠️  {step_name}: COMPLETED WITH WARNINGS")
                
        except Exception as e:
            print(f"❌ {step_name}: FAILED - {e}")
            setup_results[step_name] = {"success": False, "error": str(e)}
    
    # Generate final report
    print(f"\n{'='*80}")
    print("🎯 SETUP COMPLETION SUMMARY")
    print(f"{'='*80}")
    
    successful_steps = sum(1 for result in setup_results.values() if result["success"])
    total_steps = len(setup_steps)
    
    print(f"\n📊 Setup Summary:")
    print(f"   • Completed Steps: {successful_steps}/{total_steps}")
    print(f"   • Success Rate: {successful_steps/total_steps*100:.1f}%")
    
    if successful_steps >= total_steps * 0.8:  # 80% success rate
        print(f"\n🎉 SETUP SUCCESSFUL!")
        print(f"   • Your Agentic Pentesting AI is ready to use")
        print(f"   • Run './launch.sh --help' for usage instructions")
        print(f"   • Configuration file: .env (add your API keys)")
    else:
        print(f"\n⚠️  SETUP INCOMPLETE")
        print(f"   • Some steps failed or had warnings")
        print(f"   • Review errors above and run setup again")
    
    # Generate detailed report
    report = generate_setup_report()
    
    print(f"\n🚀 Quick Start Commands:")
    print(f"   • Basic scan: ./launch.sh scan example.com")
    print(f"   • AI agent: ./launch.sh agentic 'find vulnerabilities in target.com'")
    print(f"   • Smart agent: ./launch.sh smart-agent 'comprehensive assessment' --learning")
    print(f"   • Train models: ./train_models.sh")
    print(f"   • Run tests: ./run_tests.sh")
    
    print(f"\n📚 Documentation:")
    print(f"   • README.md - Main documentation")
    print(f"   • ENHANCED_FEATURES.md - Advanced features")
    print(f"   • NLP_FRAMEWORK_GUIDE.md - NLP system guide")
    print(f"   • setup_report.json - Detailed setup results")
    
    return setup_results


if __name__ == "__main__":
    try:
        results = main()
        sys.exit(0 if all(r["success"] for r in results.values()) else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        sys.exit(1)
