# 🔥 **AutoPenTest: ChatGPT-Style NLP Pentesting Interface**

## **🎯 Overview**

Your AutoPenTest framework now features a **ChatGPT-style conversational interface** that makes NLP-driven penetration testing as easy as having a conversation with an AI assistant!

![Chat Interface Preview](docs/chat-preview.png)

## **✨ Key Features**

### **💬 Conversational Interface**
- **ChatGPT-style UI** with speech bubbles and smooth animations
- **Real-time typing indicators** and loading animations
- **Message history** with timestamps
- **Auto-scroll** and responsive design

### **🧠 Natural Language Processing**
- **3-tier intelligence system** (Heuristic → LLM → Enhanced Agent)
- **Intent recognition** and context awareness
- **Smart target extraction** and tool selection
- **Learning capabilities** with persistent knowledge base

### **🛠️ Comprehensive Pentesting**
- **25+ integrated tools** (Nmap, Nuclei, SQLMap, Metasploit, etc.)
- **Multi-domain coverage** (Web, Mobile, Network, Wireless, Cloud)
- **Intelligent automation** with adaptive workflows
- **Professional reporting** in multiple formats

## **🚀 Quick Start**

### **1. Installation**
```bash
# Clone the repository
git clone <your-repo-url>
cd automatic-pentesting

# Install dependencies
pip install -r requirements.txt

# Install GUI dependencies
pip install PyQt6

# Optional: Enhanced NLP capabilities
pip install spacy numpy scipy
python -m spacy download en_core_web_sm
```

### **2. Launch Chat Interface**
```bash
# Start the ChatGPT-style interface
python launch_chat.py
```

### **3. Start Chatting!**
Just type natural language requests like:
- *"Find vulnerabilities in example.com"*
- *"Scan 192.168.1.0/24 for open services"*  
- *"Test banking_app.apk with dynamic analysis"*
- *"Audit WiFi security and capture handshakes"*

## **💡 Example Conversations**

### **Web Application Security**
```
👤 User: I need to test the security of my company website https://mycompany.com

🤖 AI: I'll perform a comprehensive web security assessment for mycompany.com. Let me start with reconnaissance and vulnerability scanning.

🔍 **Analysis Complete**

🚨 **Vulnerabilities Detected:**
  • SQL Injection in login form
  • XSS vulnerability in search functionality
  • Outdated SSL/TLS configuration

🎯 **Targets Discovered:**
  • admin.mycompany.com
  • api.mycompany.com
  • mail.mycompany.com

📊 **Success Rate:** 95.0%
✅ Analysis completed successfully!
```

### **Network Reconnaissance** 
```
👤 User: Perform stealthy reconnaissance on 192.168.1.0/24 without triggering IDS

🤖 AI: I'll conduct a careful, low-noise scan of your network range to avoid detection by intrusion detection systems.

🧠 **Enhanced Analysis Complete**

🚨 **Vulnerabilities:** 3
  • SMB signing disabled on 192.168.1.105
  • Default credentials on 192.168.1.110
  • Unpatched SSH service on 192.168.1.120

🎯 **New Targets:** 8
  • 192.168.1.100 (Windows Server)
  • 192.168.1.105 (Domain Controller)
  • 192.168.1.110 (Network Printer)

📚 **Knowledge Gained:** 24 facts
📈 **Success Rate:** 97.2%
```

## **🎨 Interface Features**

### **Modern Chat Design**
- **Clean, modern aesthetic** inspired by ChatGPT
- **Dark header** with gradient background
- **Message bubbles** with proper alignment (user right, AI left)
- **Rounded corners** and smooth animations
- **Professional color scheme** (blues and grays)

### **Interactive Elements**
- **Quick suggestion buttons** for common tasks
- **Real-time status updates** in header
- **Loading animations** with thinking dots
- **Auto-focus** input field after responses
- **Keyboard shortcuts** (Enter to send)

### **Smart Message Formatting**
- **Monospace fonts** for technical output
- **Emoji indicators** for different content types
- **Markdown-style** bold text support
- **Selectable text** for copying results
- **Timestamps** on all messages

## **🔧 Architecture**

### **Intelligence Layers**
```
┌─────────────────────────────────────────────────┐
│        🖥️ ChatGPT-Style Interface               │
├─────────────────────────────────────────────────┤
│        🧠 Enhanced NLP Agent (Learning)         │
├─────────────────────────────────────────────────┤
│        🤖 LLM Integration (Ollama/OpenAI)       │
├─────────────────────────────────────────────────┤
│        🔍 Heuristic Pattern Matching            │
├─────────────────────────────────────────────────┤
│        🛠️ Core Pentesting Tools & Modules      │
└─────────────────────────────────────────────────┘
```

### **Request Processing Flow**
1. **User Input** → Natural language message
2. **NLP Analysis** → Intent classification and parsing
3. **Plan Generation** → Tool selection and workflow
4. **Execution** → Background processing with progress
5. **Response** → Formatted results in chat bubble
6. **Learning** → Knowledge base updates

## **🌟 Advanced Features**

### **Demo Mode**
- **No setup required** - works out of the box
- **Simulated responses** with realistic pentesting output
- **Perfect for demonstrations** and learning
- **Automatic fallback** when tools aren't installed

### **Real Mode**
- **Full tool integration** with 25+ security tools
- **Live command execution** with real results
- **Professional reporting** and result storage
- **Learning and adaptation** over time

### **Multi-Modal Operation**
```bash
# ChatGPT-style interface (Recommended)
python launch_chat.py

# Traditional dashboard interface  
python launch_gui.py

# Command-line interface
python autopentest.py smart-agent "your request" --learning

# Interactive terminal mode
python autopentest.py assistant
```

## **💬 Supported Request Types**

### **Reconnaissance**
- *"Discover subdomains of target.com"*
- *"Map the network topology of 192.168.1.0/24"*
- *"Gather OSINT on company.com"*
- *"Enumerate services on this IP range"*

### **Vulnerability Assessment**
- *"Find security flaws in myapp.com"*
- *"Check for common web vulnerabilities"*
- *"Scan for CVEs and misconfigurations"*
- *"Test for SQL injection and XSS"*

### **Mobile Security**
- *"Analyze banking_app.apk for security issues"*
- *"Test this Android app with static analysis"*
- *"Use Frida to perform dynamic testing"*
- *"Check for hardcoded secrets in APK"*

### **Network Security** 
- *"Audit wireless networks nearby"*
- *"Capture WPA handshakes and crack them"*
- *"Test network segmentation and access controls"*
- *"Scan for rogue access points"*

### **Cloud Security**
- *"Assess AWS security posture"*
- *"Check cloud misconfigurations"*
- *"Audit IAM policies and permissions"*
- *"Test container security"*

## **🎛️ Configuration**

### **Environment Variables**
```bash
# API Keys
export SHODAN_API_KEY="your_key_here"
export VIRUSTOTAL_API_KEY="your_key_here"

# LLM Configuration  
export LLM_PROVIDER="ollama"  # or "openai" or "heuristic"
export OLLAMA_URL="http://localhost:11434"
export OPENAI_API_KEY="your_key_here"

# Tool Paths (if not in PATH)
export NMAP_PATH="/usr/bin/nmap"
export NUCLEI_PATH="/usr/local/bin/nuclei"
```

### **Tool Installation**
```bash
# Essential tools
sudo apt install nmap nikto sqlmap

# Advanced tools
GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Optional AI enhancement
pip install spacy
python -m spacy download en_core_web_sm
```

## **📊 Output Formats**

### **Chat Responses**
- **Structured summaries** with emoji indicators
- **Key findings** highlighted with icons
- **Statistics** and success rates
- **Next steps** and recommendations

### **Generated Reports**
- **HTML** - Interactive web reports
- **Markdown** - Documentation-friendly
- **JSON** - Machine-readable data
- **PDF** - Executive summaries

### **Data Storage**
```
reports/
├── chat_history.json          # Conversation logs
├── agent_knowledge.json       # Learned facts
├── scans/                     # Raw scan data
│   ├── recon_*.json
│   ├── vulnscan_*.json
│   └── payloads_*.json
└── reports/                   # Final reports
    ├── pentest_report_*.html
    └── executive_summary_*.pdf
```

## **🔐 Security & Ethics**

### **Responsible Use**
- **Authorization required** - Only test systems you own
- **Legal compliance** - Follow local laws and regulations
- **Responsible disclosure** - Report vulnerabilities properly
- **Educational purpose** - Use for learning and improvement

### **Built-in Safeguards**
- **Demo mode default** - Safe for exploration
- **Authorization prompts** for destructive operations
- **Rate limiting** to prevent abuse
- **Audit logging** of all activities

## **🚀 What Makes This Special**

### **1. True Conversational AI**
Unlike traditional pentesting tools that require command-line expertise, you can now:
- **Chat naturally** about security testing needs
- **Ask follow-up questions** and get contextual responses  
- **Learn from the AI** as it explains findings
- **Iterate quickly** on testing strategies

### **2. Intelligent Automation**
- **Context-aware planning** based on discovered information
- **Adaptive workflows** that change based on results
- **Learning system** that improves over time
- **Smart tool selection** optimized for each scenario

### **3. Professional User Experience**
- **Modern, intuitive interface** anyone can use
- **Real-time feedback** and progress indicators
- **Comprehensive reporting** for stakeholders
- **Seamless workflow** from chat to report

This makes your AutoPenTest framework the **most advanced NLP-driven security testing platform** available - combining the power of professional pentesting tools with the ease of conversational AI!

## **📞 Support & Community**

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides and tutorials
- **Community**: Join discussions and share knowledge
- **Updates**: Regular improvements and new features

---

**Ready to revolutionize your security testing? Start chatting with your AI pentesting assistant today!** 🚀
