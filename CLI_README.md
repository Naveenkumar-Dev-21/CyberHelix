# AutoPenTest Enhanced CLI Interface

## 🚀 Overview

The AutoPenTest Enhanced CLI provides a comprehensive, interactive command-line interface for automated penetration testing with advanced features including:

- **Interactive Menu System**: Navigate through all modules with an intuitive menu
- **Path Traversal File Browser**: Advanced file selection with directory navigation
- **Dynamic Module Loading**: All pentesting modules accessible through a unified interface
- **Session Management**: Track your actions and results throughout the session
- **Smart Parameter Input**: Automatic file browser for file/path parameters

## 📦 Installation

### Prerequisites

```bash
# Install required Python packages
pip install --break-system-packages questionary rich click pyfiglet
```

### Make Executable

```bash
chmod +x cli_main.py
```

## 🎯 Usage

### Interactive Mode (Default)

Launch the full interactive CLI interface:

```bash
python cli_main.py
# or
./cli_main.py
```

### Command Line Options

```bash
# List all available modules
python cli_main.py --list-modules

# Check tool availability
python cli_main.py --check-tools

# Direct module execution
python cli_main.py --module recon

# Quick scan
python cli_main.py scan target.com

# Launch file browser
python cli_main.py browser

# Browse modules by category
python cli_main.py modules --category assessment
```

## 🎮 Interactive Menu Features

### Main Menu Options

1. **🎯 Quick Scan** - Wizard-guided scanning with automatic module selection
2. **📊 Module Browser** - Browse and execute modules by category
3. **🔍 Reconnaissance** - Information gathering modules
4. **🛡️ Vulnerability Scanning** - Security scanning tools
5. **💣 Exploitation** - Exploit and payload modules
6. **📁 Web/API Testing** - Web application security testing
7. **📱 Mobile Testing** - Mobile app security assessment
8. **📡 Wireless Testing** - Wi-Fi security testing
9. **☁️ Cloud Assessment** - Cloud infrastructure security
10. **🤖 AI-Powered Analysis** - AI and ML-based modules
11. **📝 Report Generation** - Generate comprehensive reports
12. **⚙️ Settings** - Configure API keys and output directories
13. **📂 File Browser** - Advanced file selection with path traversal
14. **📜 Session History** - View command history

### File Browser Features

The integrated file browser provides:

- **Path Traversal**: Navigate directories with arrow keys
- **Bookmarks**: Quick access to common directories
- **Manual Path Entry**: Type paths directly
- **Multi-Select**: Select multiple files at once
- **Directory Tree View**: Visualize folder structure
- **File Type Icons**: Visual indicators for different file types
- **File Size Display**: See file sizes at a glance

#### File Browser Navigation

- **Arrow Keys**: Navigate up/down
- **Enter**: Select file/enter directory
- **Parent Directory**: Go up one level
- **Home**: Jump to home directory
- **Bookmarks**: Quick access to saved locations
- **Manual Entry**: Type path directly

## 📋 Module Categories

### Discovery
- Reconnaissance - Comprehensive information gathering

### Scanning
- Vulnerability Scanner - Multi-tool vulnerability detection

### Analysis
- Service Analyzer - Service identification and analysis
- Target Classifier - Target characteristic analysis

### Assessment
- Network Assessor - Network security testing
- Web Assessor - Web application testing
- Mobile Assessor - Mobile app security
- Wireless Assessor - Wi-Fi security
- Cloud Assessor - Cloud infrastructure
- IoT Assessor - IoT and firmware analysis
- Social Engineering - Social engineering campaigns

### Exploitation
- Exploit Module - Vulnerability exploitation
- Payload Generator - Custom payload creation

### AI & Automation
- AI Agent - Reasoning-based pentesting
- Agentic AI - Learning and adaptation
- Copilot - Natural language assistant

### Advanced
- Autonomous Orchestrator - Fully autonomous operations
- Continuous Learning - ML-based improvement
- Red Team Planner - Engagement planning
- Self-Healing System - Error recovery

### Reporting
- Report Generator - Comprehensive reporting

## 🔧 Module Execution

When executing a module through the CLI:

1. **Module Information**: View description, requirements, and available methods
2. **Requirements Check**: Automatic verification of dependencies
3. **Method Selection**: Choose from available module methods
4. **Parameter Input**: 
   - Text parameters: Direct input with defaults
   - File parameters: Automatic file browser launch
   - Path parameters: Directory selection interface
5. **Execution**: Real-time status updates
6. **Results**: Summary display and session storage

## 💾 Session Management

The CLI maintains a session throughout your interaction:

- **Target Tracking**: Current target is remembered
- **Results Storage**: All module outputs are saved
- **History Tracking**: Complete command history
- **Report Generation**: Generate reports from session data
- **Output Directory**: Configurable output location

## ⚙️ Configuration

### API Keys

Configure API keys through Settings menu:
- Shodan API Key
- VirusTotal API Key
- AWS Credentials (for cloud assessment)

### Output Directory

Set custom output directory for:
- Scan results
- Generated reports
- Payload files
- Log files

## 🎯 Quick Start Examples

### Basic Reconnaissance

1. Launch CLI: `python cli_main.py`
2. Select "Quick Scan"
3. Enter target domain
4. Choose "Basic Reconnaissance"
5. View results and generate report

### File Analysis

1. Launch CLI: `python cli_main.py`
2. Select "File Browser"
3. Navigate to file (e.g., .apk, .pcap, firmware)
4. Select "Analyze"
5. View analysis results

### Module Browsing

1. Launch CLI: `python cli_main.py`
2. Select "Module Browser"
3. Choose category (e.g., "Assessment")
4. Select module (e.g., "Web Assessor")
5. Choose method to execute
6. Provide parameters (file browser opens automatically for files)
7. View results

## 🔍 Search Features

- **Module Search**: Find modules by name or description
- **Category Filtering**: Browse modules by category
- **Quick Access**: Direct module execution from command line

## 📊 Reporting

Generate comprehensive reports including:
- Session timestamp
- Target information
- All module results
- Command history
- Execution status

Reports are saved in JSON format and can be converted to other formats.

## 🛡️ Security Notes

- Some modules require root privileges (marked with 🔐)
- API keys are stored in environment variables
- Session data is stored locally
- Always ensure you have permission to test targets

## 🐛 Troubleshooting

### Missing Dependencies

```bash
# Install all required packages
pip install --break-system-packages questionary rich click pyfiglet pathlib
```

### Module Import Errors

Ensure all module files are in the `src/` directory and properly structured.

### Permission Errors

Some modules require root access. Run with sudo if needed:
```bash
sudo python cli_main.py
```

## 🎨 Customization

The CLI interface can be customized by modifying:
- `src/cli_interface.py` - Main interface logic
- `src/file_browser.py` - File browser behavior
- `src/module_manager.py` - Module registration and loading

## 📝 License

This tool is for authorized security testing only. Always obtain proper permission before testing any systems.

## 🤝 Contributing

To add new modules:
1. Create module in `src/` directory
2. Register in `module_manager.py`
3. Module will automatically appear in CLI

## 📞 Support

For issues or questions about the CLI interface:
- Check existing modules with `--list-modules`
- Verify tool availability with `--check-tools`
- Review session history in interactive mode
