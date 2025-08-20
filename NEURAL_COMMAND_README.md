# 🔴 Neural Command Center - The Matrix Pentesting Suite

## Advanced AI-Powered Penetration Testing Framework

The Neural Command Center is a revolutionary AI-powered pentesting assistant that transforms natural language commands into sophisticated security assessments. Built with a Matrix-themed interface, it combines cutting-edge artificial intelligence with real-world exploitation capabilities.

## 🎯 Key Features

### 🧠 Neural Command AI
- **Natural Language Processing**: Communicate with the AI using plain English
- **Intelligent Target Analysis**: Automatically identifies target types (IP, domain, URL, network)
- **Smart Tool Selection**: Chooses appropriate tools based on target and intent
- **Real Exploitation Engine**: Integrates with Metasploit for actual penetration testing
- **Adaptive Learning**: Learns from conversations and improves recommendations

### 🔴 Matrix Interface
- **Cyberpunk Aesthetic**: Digital rain effects and Matrix-themed UI
- **Real-time Terminal**: Live command execution with typing effects
- **Interactive Chatbot**: ChatGPT-style conversation interface
- **Comprehensive Reporting**: Detailed vulnerability assessments and findings

### ⚡ Advanced Capabilities
- **Multi-Target Support**: Scan networks, domains, IPs, and mobile apps
- **Exploitation Integration**: Generate payloads and start listeners
- **Stealth Mode**: Careful, undetected reconnaissance and testing
- **Mobile Security**: APK analysis and dynamic testing
- **Wireless Testing**: WiFi penetration and handshake capture

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd automatic-pentesting
   ```

2. **Run the setup script**:
   ```bash
   ./setup_neural_matrix.sh
   ```

3. **Configure API keys** (edit `.env` file):
   ```
   SHODAN_API_KEY=your_shodan_api_key_here
   VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
   ```

4. **Launch the Neural Command Center**:
   ```bash
   ./launch_neural_command.py
   ```

### Manual Installation

If you prefer manual installation:

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install system tools (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install nmap nuclei nikto sqlmap

# Make launcher executable
chmod +x launch_neural_command.py

# Launch
./launch_neural_command.py
```

## 💬 Neural Command Examples

The Neural Command Center understands natural language. Here are example commands:

### Reconnaissance
```
"Scan example.com for subdomains and gather intelligence"
"Perform deep reconnaissance on 192.168.1.0/24 network"
"Find all subdomains of target.com using passive methods"
```

### Vulnerability Scanning
```
"Scan https://example.com for web vulnerabilities"
"Find security flaws in 192.168.1.100"
"Test example.com for SQL injection vulnerabilities"
```

### Exploitation
```
"Generate a reverse shell payload for 192.168.1.100"
"Exploit the SSH service on target.com"
"Start a Metasploit listener on port 4444"
```

### Mobile Testing
```
"Analyze mobile.apk for security vulnerabilities"
"Perform static analysis on the Android app"
"Check app.apk for hardcoded secrets"
```

### Wireless Testing
```
"Scan for nearby WiFi networks"
"Capture WPA handshakes from wireless networks"
"Test wireless security in the area"
```

## 🛠️ Architecture

### Core Components

1. **NeuralCommandAI**: Main AI processor with NLP capabilities
2. **AdvancedTargetAnalyzer**: Intelligent target analysis and classification
3. **IntelligentCommandProcessor**: Natural language to command mapping
4. **RealExploitationEngine**: Metasploit integration and payload generation
5. **MatrixGUI**: PyQt6-based cyberpunk interface

### AI Features

- **Intent Classification**: Determines user intent from natural language
- **Target Recognition**: Automatically identifies and analyzes targets
- **Tool Selection**: Chooses optimal tools for each task
- **Parameter Extraction**: Extracts timing, depth, and stealth preferences
- **Context Awareness**: Maintains conversation context and memory

## 🔧 Configuration

### Environment Variables (.env)

```env
# API Keys
SHODAN_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here

# Tool Paths
NMAP_PATH=/usr/bin/nmap
NUCLEI_PATH=/usr/bin/nuclei
NIKTO_PATH=/usr/bin/nikto
SQLMAP_PATH=/usr/bin/sqlmap
MSFVENOM_PATH=/usr/bin/msfvenom

# Neural AI Settings
NEURAL_AI_MODEL=gpt-3.5-turbo
MAX_CONVERSATION_HISTORY=50
EXPLOITATION_MODE=enabled
STEALTH_MODE=disabled

# Output Settings
OUTPUT_DIR=./reports
LOG_LEVEL=INFO
```

### Required Tools

**Essential**:
- `nmap` - Network scanning
- `python3` - Runtime environment
- `pip3` - Package management

**Recommended**:
- `nuclei` - Vulnerability scanning
- `nikto` - Web server scanning
- `sqlmap` - SQL injection testing
- `amass` - Subdomain enumeration
- `gobuster` - Directory/file enumeration

**Optional** (for full functionality):
- `msfconsole` - Metasploit Framework
- `frida` - Mobile dynamic analysis
- `aircrack-ng` - Wireless testing
- `hashcat` - Password cracking

## 🎮 Interface Guide

### Matrix GUI Layout

1. **Neural Command Center Tab**: AI chatbot interface
2. **Matrix Terminal**: Traditional command execution
3. **Infiltration Results**: Formatted vulnerability reports
4. **Neural Knowledge**: Learning and knowledge base

### Chatbot Interface

- **Natural Input**: Type commands in plain English
- **Smart Responses**: AI provides context-aware feedback
- **Real-time Execution**: Commands execute immediately
- **Progress Tracking**: Visual progress indicators
- **Results Integration**: Findings appear in results tab

## 🔒 Security & Ethics

### Important Disclaimers

⚠️ **AUTHORIZATION REQUIRED**: Only test systems you own or have explicit permission to test.

⚠️ **LEGAL COMPLIANCE**: Ensure compliance with local laws and regulations.

⚠️ **RESPONSIBLE DISCLOSURE**: Report vulnerabilities responsibly to system owners.

### Built-in Safeguards

- **Authorization Warnings**: Prompts for exploitation commands
- **Stealth Options**: Careful, minimal-footprint scanning modes
- **Rate Limiting**: Prevents overwhelming target systems
- **Logging**: Comprehensive activity logging for accountability

## 🐛 Troubleshooting

### Common Issues

**"Neural Command AI not available"**:
```bash
pip3 install PyQt6 python-nmap scapy dnspython
```

**"Metasploit not found"**:
```bash
# Install Metasploit Framework
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall
```

**GUI not launching**:
```bash
# Install GUI dependencies
sudo apt-get install python3-pyqt6 python3-pyqt6.qtcore python3-pyqt6.qtgui python3-pyqt6.qtwidgets
```

**Permission errors**:
```bash
# Don't run as root, fix permissions instead
chmod +x launch_neural_command.py
chown -R $USER:$USER .
```

### Debug Mode

Launch with debug output:
```bash
export LOG_LEVEL=DEBUG
./launch_neural_command.py
```

## 🤝 Contributing

We welcome contributions to the Neural Command Center! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd automatic-pentesting

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by The Matrix trilogy
- Built with PyQt6 for the cyberpunk interface
- Integrates with industry-standard security tools
- AI-powered natural language processing

## 📞 Support

For support, questions, or feature requests:

- 📧 Email: [support@neuralcommand.matrix]
- 💬 Discord: [Matrix Pentesting Community]
- 🐛 Issues: [GitHub Issues]

---

## 🔴 "Welcome to the Real World"

*The Neural Command Center represents the evolution of penetration testing - where artificial intelligence meets cybersecurity expertise. Take the red pill and discover how deep the rabbit hole goes.*

```
"Unfortunately, no one can be told what the Matrix is. 
 You have to see it for yourself."
                                    - Morpheus
```

🔴 **Remember**: Use your powers responsibly. The Matrix has you, but you also have the Matrix.
