# 🔒 PentestGPT Ultimate - AI-Powered Penetration Testing Suite

## 🌟 Overview

PentestGPT Ultimate is a comprehensive, AI-powered penetration testing framework that combines natural language processing with automated security testing tools. It provides a modern ChatGPT-style interface for conducting professional security assessments.

## ✨ Key Features

### 🤖 AI-Powered Intelligence
- **Natural Language Processing**: Understands security commands in plain English
- **Smart Command Generation**: Automatically generates appropriate pentesting commands
- **Context-Aware Responses**: Maintains conversation history for better assistance
- **Pattern Recognition**: Advanced NLP using spaCy for intent analysis

### 🎨 Modern User Interface
- **Split Interface Design**: Chat assistant on the left, terminal on the right
- **Dark Theme**: Professional VS Code-inspired dark theme
- **Multi-Tab Layout**: Organized tabs for different testing aspects
- **Real-Time Output**: Live command execution with colored terminal output
- **Status Indicators**: Visual feedback for system components

### 🛠️ Comprehensive Testing Capabilities

#### Network Security
- Port scanning and service enumeration
- Network mapping and discovery
- Vulnerability detection
- Stealth scanning options

#### Web Application Testing
- SQL injection detection
- Cross-site scripting (XSS) testing
- Directory enumeration
- WordPress vulnerability scanning
- Web server misconfiguration detection

#### Exploitation & Post-Exploitation
- Payload generation (reverse/bind shells)
- Multiple platform support (Windows, Linux, Android, Web)
- Metasploit integration
- Privilege escalation assistance

#### Password Security
- Hash cracking (MD5, SHA1, SHA256, etc.)
- Brute force attacks (SSH, FTP, HTTP, etc.)
- Dictionary attacks
- Password spray testing

#### Additional Features
- Mobile application (APK) analysis
- Cloud security assessment
- SMB enumeration
- DNS reconnaissance
- Wireless network testing

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/automatic-pentesting.git
cd automatic-pentesting
```

2. **Run the launcher**:
```bash
./launch_ultimate.sh
```

Or directly:
```bash
python pentestgpt_ultimate.py
```

### System Requirements

- **OS**: Linux (Kali, Parrot, Ubuntu, Arch/Garuda)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Display**: 1600x900 resolution or higher

### Dependencies

#### Required
- Python 3.8+
- tkinter (usually included with Python)
- Basic networking tools

#### Optional (for full functionality)
```bash
# Arch/Garuda Linux
sudo pacman -S nmap nikto gobuster sqlmap metasploit hydra john hashcat aircrack-ng
yay -S whatweb dirb wpscan

# Debian/Ubuntu/Kali
sudo apt install nmap nikto gobuster sqlmap metasploit-framework hydra john hashcat aircrack-ng whatweb dirb wpscan

# Install Python packages
pip install spacy
python -m spacy download en_core_web_sm
```

## 💬 Usage Guide

### Natural Language Commands

Simply type what you want to do in plain English:

- **Network Scanning**:
  - "Scan the network 192.168.1.0/24"
  - "Find all open ports on target"
  - "Perform a stealth scan"
  - "Check for vulnerabilities"

- **Web Testing**:
  - "Test the website for vulnerabilities"
  - "Check https://example.com for SQL injection"
  - "Find hidden directories on the web server"
  - "Scan WordPress site for issues"

- **Exploitation**:
  - "Generate a reverse shell for Windows"
  - "Create PHP web shell"
  - "Generate Android payload"

- **Password Attacks**:
  - "Crack SSH password for target"
  - "Brute force the web login"
  - "Crack this hash: 5f4dcc3b5aa765d61d8327deb882cf99"

### Direct Terminal Commands

Use the `$` prefix for direct terminal commands:
```
$ nmap -sV -sC 192.168.1.1
$ nikto -h http://example.com
$ sqlmap -u "http://target.com/page?id=1" --dbs
```

### Quick Actions

Use the quick action buttons at the bottom:
- 🔍 **Quick Scan**: Fast port scan
- 🌐 **Web Scan**: Web vulnerability assessment
- 📡 **Network Map**: Network discovery
- 🛡️ **Vuln Scan**: Comprehensive vulnerability scan
- 📱 **Mobile Test**: APK analysis
- ☁️ **Cloud Assess**: Cloud security testing
- 🔐 **Crack Hash**: Password hash cracking
- 🎯 **Exploit**: Exploitation framework

## 🏗️ Architecture

### Project Structure
```
automatic-pentesting/
├── pentestgpt_ultimate.py      # Main GUI application
├── launch_ultimate.sh           # Launcher script
├── src/                        # Core modules
│   ├── chat_ai_backend.py     # AI/NLP processing
│   ├── payload_generator.py    # Payload generation
│   ├── vulnerability_scanner.py # Vulnerability detection
│   ├── reconnaissance.py       # Recon modules
│   ├── exploit_module.py       # Exploitation tools
│   ├── report_generator.py     # Report generation
│   └── ...                    # Additional modules
├── data/                       # Training data and configs
├── reports/                    # Generated reports
└── models/                     # AI models
```

### Key Components

1. **AI Backend**: Natural language processing and command generation
2. **GUI Framework**: Tkinter-based interface with modern styling
3. **Tool Integration**: Seamless integration with pentesting tools
4. **Report Generator**: Comprehensive report generation in multiple formats
5. **Exploit Framework**: Payload generation and exploitation modules

## 🔧 Advanced Features

### AI Capabilities
- **Intent Recognition**: Understands user intent from natural language
- **Context Awareness**: Maintains conversation context
- **Tool Suggestion**: Recommends appropriate tools for tasks
- **Result Analysis**: Analyzes scan results and provides insights

### Security Features
- **No Sudo Required**: Runs without elevated privileges (where possible)
- **Safe Command Execution**: Validates and sanitizes commands
- **Permission Checks**: Ensures authorized testing only
- **Audit Logging**: Logs all activities for compliance

### Customization
- **Extensible Framework**: Easy to add new modules
- **Custom Payloads**: Create custom exploitation payloads
- **Theme Customization**: Modify colors and styling
- **Tool Integration**: Add support for new tools

## 📊 Testing Workflow

### 1. Reconnaissance
```
User: "Scan 192.168.1.100"
AI: Executes comprehensive port scan and service enumeration
```

### 2. Vulnerability Assessment
```
User: "Find vulnerabilities"
AI: Runs vulnerability scanners and identifies weaknesses
```

### 3. Exploitation
```
User: "Generate payload for Windows"
AI: Creates custom payload based on target architecture
```

### 4. Reporting
```
User: "Generate report"
AI: Creates comprehensive penetration test report
```

## ⚠️ Legal & Ethical Use

**IMPORTANT**: This tool is for authorized security testing only!

- ✅ Only test systems you own or have explicit permission to test
- ✅ Follow responsible disclosure practices
- ✅ Comply with local laws and regulations
- ✅ Document all testing activities
- ❌ Never use for unauthorized access
- ❌ Do not test production systems without approval
- ❌ Avoid causing service disruptions

## 🐛 Troubleshooting

### Common Issues

1. **"spaCy not available"**
   - Install spaCy: `pip install spacy`
   - Download model: `python -m spacy download en_core_web_sm`

2. **"Tool not found"**
   - Install missing tools using your package manager
   - Tools are optional - core functionality works without them

3. **GUI not starting**
   - Ensure tkinter is installed: `python -m tkinter`
   - Check display settings if using SSH: `export DISPLAY=:0`

4. **Permission errors**
   - Some scans require root (use sudo carefully)
   - Check file permissions in project directory

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- Additional AI response patterns
- Support for more pentesting tools
- Enhanced file analysis capabilities
- Improved vulnerability detection
- Multi-language support
- Cloud-native testing features
- Container security assessment
- API testing modules

## 📈 Performance

- **Startup Time**: ~2-3 seconds
- **Command Execution**: Real-time
- **AI Response**: <1 second for most queries
- **Memory Usage**: ~200MB base, varies with operations

## 🔄 Updates & Maintenance

Check for updates regularly:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📚 Documentation

- [User Guide](docs/USER_GUIDE.md)
- [API Documentation](docs/API.md)
- [Module Development](docs/DEVELOPMENT.md)
- [Security Best Practices](docs/SECURITY.md)

## 📝 License

This project is provided for educational and authorized testing purposes only. Users are responsible for complying with all applicable laws and regulations.

## 🚨 Disclaimer

The developers assume no liability for misuse or damage caused by this tool. Always obtain proper authorization before testing any system. Use at your own risk.

## 🙏 Acknowledgments

- Security community for tool development
- Open source contributors
- Penetration testing frameworks
- AI/ML libraries and frameworks

## 📞 Support

- Create an issue on GitHub
- Check documentation and FAQs
- Join our community Discord

---

**Created with ❤️ for the security community**

*Remember: With great power comes great responsibility. Use ethically!*
