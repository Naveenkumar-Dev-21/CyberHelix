#!/usr/bin/env python3
"""
CLI Test for AI-Powered Pentesting System
Test the system with real commands to verify functionality
"""

import sys
import subprocess
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from ai_model import IntentClassifierModel
    from enhanced_nlp_processor import EnhancedNLPProcessor
    from copilot import copilot_run
    AI_AVAILABLE = True
except ImportError as e:
    print(f"AI modules not available: {e}")
    AI_AVAILABLE = False

def convert_to_system_command(user_input):
    """Convert natural language to system commands"""
    
    user_lower = user_input.lower()
    
    # System information commands
    system_commands = {
        "services": "systemctl list-units --type=service --state=running | head -10",
        "running services": "systemctl list-units --type=service --state=running | head -10",
        "processes": "ps aux | head -15",
        "running processes": "ps aux | head -15",
        "network": "netstat -tulpn | head -15",
        "open ports": "ss -tulpn | head -10",
        "listening ports": "ss -tulpn | grep LISTEN | head -10",
        "disk usage": "df -h",
        "memory usage": "free -h",
        "system info": "uname -a",
        "users": "who && last | head -5",
        "load": "uptime && top -bn1 | head -10",
        "environment": "env | head -10",
        "path": "echo $PATH",
    }
    
    # Check for exact matches or keywords
    for key, cmd in system_commands.items():
        if key in user_lower:
            return cmd
    
    # Network scanning commands
    if any(word in user_lower for word in ['scan', 'nmap']):
        return "nmap -sS localhost"
    
    # File system commands
    if any(word in user_lower for word in ['list', 'ls', 'directory']):
        return "ls -la"
    
    # Default: try to execute as shell command
    return user_input

def execute_command(command):
    """Execute a system command and return output"""
    try:
        print(f"❯ {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ai_system(user_input):
    """Test the AI system with a user input"""
    print(f"\n🔍 Processing: '{user_input}'")
    print("="*60)
    
    if AI_AVAILABLE:
        try:
            # Test AI model
            model = IntentClassifierModel()
            if model.load_model():
                ai_result = model.predict(user_input)
                print(f"🧠 AI Intent: {ai_result['intent']} (confidence: {ai_result['confidence']:.2f})")
            
            # Test NLP processor
            nlp = EnhancedNLPProcessor()
            nlp_result = nlp.process_request(user_input)
            print(f"🔤 NLP Command: {nlp_result.primary_command.value}")
            if nlp_result.targets:
                print(f"🎯 Targets: {nlp_result.targets}")
            
        except Exception as e:
            print(f"❌ AI processing error: {e}")
    
    # Convert to system command
    system_cmd = convert_to_system_command(user_input)
    print(f"⚙️ System Command: {system_cmd}")
    
    # Execute command
    print(f"\n📟 Executing command...")
    success = execute_command(system_cmd)
    
    status = "✅ Success" if success else "❌ Failed"
    print(f"\n{status}")
    print("="*60)

def main():
    """Main CLI test function"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           🤖 AI PENTESTING SYSTEM CLI TEST 🤖                ║
║                 Testing Real Command Execution                ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Test cases
    test_cases = [
        "show running services",
        "list all processes", 
        "check network connections",
        "show disk usage",
        "display memory usage",
        "who is logged in",
        "show system information",
        "list current directory"
    ]
    
    print("🔬 Running automated tests...")
    
    for test_case in test_cases:
        test_ai_system(test_case)
        input("\nPress Enter to continue to next test...")
    
    # Interactive mode
    print("\n🎮 Interactive Mode - Enter your own commands!")
    print("Type 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("🔍 Enter command: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                break
            
            if not user_input:
                continue
            
            test_ai_system(user_input)
            
        except KeyboardInterrupt:
            break
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
