# 🔒 Automatic Pentesting Tool - GUI Interface

## Professional Automated Penetration Testing Framework with Beginner-Friendly GUI

### 🚀 Features

The GUI provides a comprehensive, user-friendly interface for automated penetration testing with the following features:

#### 📱 Five Main Tabs:

1. **🚀 Quick Scan**
   - Simple one-click scanning for beginners
   - Target input (URL, IP, or Domain)
   - File upload support for multiple targets
   - Configurable scan options:
     - Reconnaissance & Discovery
     - Vulnerability Scanning
     - Service Analysis
     - Payload Generation
     - Stealth Mode
   - Real-time output display
   - Progress tracking

2. **⚙️ Advanced Scan**
   - Full control over scanning parameters
   - Multiple target support
   - Custom port ranges
   - Module selection (Nmap, Nuclei, Nikto, SQLMap, Metasploit)
   - Timing control (Paranoid to Insane)
   - Command preview
   - Detailed output logging

3. **🤖 AI Assistant**
   - Natural language command interface
   - Chat-style interaction
   - Intelligent command interpretation
   - Automated task execution
   - Example commands provided
   - Real-time AI responses

4. **💣 Payload Generator**
   - Multiple payload types (reverse_shell, bind_shell, web_shell, meterpreter)
   - Platform selection (Windows, Linux, Android, Web)
   - Configurable LHOST/LPORT
   - Evasion options:
     - Encoding
     - Encryption
     - Obfuscation
     - Sandbox bypass
   - Generated payload display

5. **📊 Results & Reports**
   - Hierarchical results tree view
   - Severity-based vulnerability display
   - Export options:
     - JSON format
     - HTML reports
     - PDF reports (if supported)
   - Results refresh capability

### 🛠️ Installation

1. **Install Dependencies:**
   ```bash
   # Install Python 3 and Tkinter
   sudo apt-get update
   sudo apt-get install python3 python3-tk python3-pip

   # Install required Python packages
   pip3 install -r requirements.txt
   ```

2. **Install Pentesting Tools (Optional but recommended):**
   ```bash
   # Nmap
   sudo apt-get install nmap

   # Nuclei
   GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

   # Other tools as needed...
   ```

### 🎯 Usage

#### Method 1: Using the Launcher Script
```bash
./launch_gui.sh
```

#### Method 2: Direct Python Execution
```bash
python3 pentesting_gui.py
```

#### Method 3: From Virtual Environment
```bash
source .venv/bin/activate
python pentesting_gui.py
```

### 📝 How to Use Each Tab

#### Quick Scan (Beginners)
1. Enter target (example.com, 192.168.1.1, https://site.com)
2. Or click "📁 Load from File" to load multiple targets
3. Select desired scan options
4. Click "🚀 START SCAN"
5. View real-time results in the output window
6. Results are automatically saved to the output directory

#### Advanced Scan (Experienced Users)
1. Enter multiple targets (one per line)
2. Specify port range (e.g., 1-1000, 80,443,8080)
3. Select scanning modules
4. Choose scan speed/timing
5. Preview generated commands
6. Click "⚡ EXECUTE ADVANCED SCAN"
7. Monitor detailed output

#### AI Assistant
1. Type natural language commands like:
   - "Scan example.com for vulnerabilities"
   - "Find open ports on 192.168.1.1"
   - "Check if target is vulnerable to SQL injection"
2. Press Enter or click Send
3. AI will interpret and execute appropriate actions
4. View responses in chat interface

#### Payload Generator
1. Select payload type (reverse_shell, bind_shell, etc.)
2. Choose target platform
3. Enter LHOST (your IP) and LPORT
4. Enable evasion options if needed
5. Click "🔨 GENERATE PAYLOAD"
6. Copy generated payload from output

#### Results & Reports
1. View all scan results in tree structure
2. Expand items to see details
3. Export results as:
   - JSON for data processing
   - HTML for web viewing
   - PDF for documentation
4. Refresh to update display

### 🔐 Real Output vs Simulated

**This GUI provides REAL output from actual pentesting tools:**
- ✅ Real Nmap scans with actual port detection
- ✅ Real vulnerability scanning with Nuclei
- ✅ Real service analysis and fingerprinting
- ✅ Real payload generation (if tools installed)
- ✅ Real AI-powered command interpretation
- ✅ Results saved to actual files

### 📁 Output Directory Structure

```
output/
├── scans/
│   ├── scan_example_com_20240819_120000.json
│   └── scan_192_168_1_1_20240819_130000.json
├── reports/
│   ├── report_example_com.html
│   └── report_example_com.pdf
└── payloads/
    └── payload_windows_reverse_shell.exe
```

### ⚠️ Important Notes

1. **Legal Use Only**: Only scan targets you own or have permission to test
2. **Network Impact**: Scans can generate significant network traffic
3. **Root Privileges**: Some scans (SYN scan) require sudo/root access
4. **Tool Availability**: Install pentesting tools for full functionality
5. **Display Required**: GUI requires X11 display (use X forwarding for remote)

### 🐛 Troubleshooting

#### "No module named tkinter"
```bash
sudo apt-get install python3-tk
```

#### "Display not found"
```bash
export DISPLAY=:0
# Or use X forwarding: ssh -X user@host
```

#### "Permission denied" for scans
```bash
# Run with sudo for privileged scans
sudo python3 pentesting_gui.py
```

#### Import errors
```bash
# Ensure you're in the project directory
cd /path/to/automatic-pentesting
python3 pentesting_gui.py
```

### 🎨 GUI Customization

The GUI uses a dark theme by default. Colors can be customized in the `__init__` method:

```python
self.bg_color = "#1e1e1e"      # Background
self.fg_color = "#ffffff"      # Foreground
self.accent_color = "#00ff41"  # Accent (Matrix green)
self.button_bg = "#2d2d2d"     # Button background
```

### 📸 Features at a Glance

- **Multi-threaded**: Non-blocking UI during scans
- **Real-time Updates**: Live output streaming
- **File Support**: Load targets from files
- **Export Options**: Multiple report formats
- **AI Integration**: Natural language processing
- **Error Handling**: Graceful error messages
- **Progress Tracking**: Visual progress indicators
- **Result Storage**: Automatic result saving

### 🤝 Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

### 📄 License

This tool is for educational and authorized testing purposes only.

---

**Remember**: Always obtain proper authorization before testing any system you don't own!
