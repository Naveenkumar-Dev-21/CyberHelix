# AutoPenTest - Automated Penetration Testing Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](README.md)

A comprehensive automated penetration testing framework that combines multiple security tools and frameworks to provide end-to-end security assessments. AutoPenTest streamlines the entire penetration testing process from reconnaissance to reporting.

## 🚀 Features

### Phase 1: Intelligent Reconnaissance & Mapping
- **🧠 Smart Target Classification**: Automatically determines if target is web application, network host, or mixed environment
- **🔒 Root-Privileged Scanning**: Automatically uses sudo for comprehensive nmap scans (SYN scan, OS detection)
- **📊 Optimized Scan Strategy**: Adapts scanning approach based on target type (web vs network vs mixed)
- **🌐 Advanced Port Scanning**: Intelligent port selection based on target classification
- **🔍 Internet-wide Intelligence**: Shodan API integration for passive reconnaissance
- **🏗️ Subdomain Enumeration**: Amass integration with DNS brute-force fallback
- **📧 OSINT Gathering**: theHarvester integration for email and domain intelligence
- **🌍 DNS Analysis**: Complete DNS record enumeration

### Phase 2: Vulnerability Scanning
- **Template-based Scanning**: Nuclei integration with extensive CVE and misconfiguration templates
- **Web Application Testing**: Nikto integration for web server vulnerability assessment
- **SQL Injection Detection**: SQLMap integration for automated SQL injection testing
- **Custom Vulnerability Checks**: Extensible framework for custom security checks

### Phase 3: Payload Generation & Exploitation
- **Multi-Platform Payloads**: Metasploit Framework (msfvenom) integration
- **Custom Payload Generation**: Platform-specific reverse shells and bind shells
- **Web Shell Generation**: PHP, JSP, and ASPX web shells
- **Evasion Techniques**: Multiple payload formats and encoding options

### Phase 4: Comprehensive Reporting
- **Multiple Formats**: HTML, Markdown, JSON, and plain text reports
- **Executive Summaries**: Risk assessment and executive-level summaries
- **Detailed Technical Reports**: Complete vulnerability details and remediation steps
- **Custom Templates**: Jinja2-powered templating system for custom reports

## 📋 Requirements

### System Requirements
- Python 3.8+
- Linux, Windows, or macOS
- 4GB+ RAM recommended
- 2GB+ disk space for tools and reports

### External Tools
The framework integrates with several security tools. Install the following tools for full functionality:

#### Essential Tools
```bash
# Nmap
sudo apt install nmap                    # Ubuntu/Debian
brew install nmap                        # macOS
# Windows: Download from https://nmap.org/

# Nuclei
GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Nikto
sudo apt install nikto                   # Ubuntu/Debian
brew install nikto                       # macOS

# SQLMap
sudo apt install sqlmap                  # Ubuntu/Debian
brew install sqlmap                      # macOS
```

#### Optional Tools
```bash
# Amass
sudo apt install amass                   # Ubuntu/Debian
brew install amass                       # macOS

# theHarvester
pip3 install theHarvester

# Metasploit Framework
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall
```

## 🔧 Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/autopentest.git
cd autopentest
```

### 2. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

### 4. Make Executable
```bash
chmod +x autopentest.py
```

### 5. Verify Installation
```bash
python3 autopentest.py --config-check
```

## ⚙️ Configuration

### API Keys
Add your API keys to the `.env` file:

```bash
# Shodan API (for passive reconnaissance)
SHODAN_API_KEY=your_shodan_api_key_here

# VirusTotal API (optional)
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
```

### Tool Paths
If tools are not in your PATH, specify full paths in `.env`:

```bash
NMAP_PATH=/usr/bin/nmap
NUCLEI_PATH=/home/user/go/bin/nuclei
NIKTO_PATH=/usr/bin/nikto
# ... etc
```

## 🎯 Usage

### Quick Start
```bash
# Full automated scan
python3 autopentest.py scan example.com

# Quick scan (reduced scope)
python3 autopentest.py scan example.com --quick

# Comprehensive scan (full scope)
python3 autopentest.py scan example.com --comprehensive
```

### Modular Scanning
```bash
# Reconnaissance only
python3 autopentest.py scan example.com --recon-only

# Vulnerability scanning only
python3 autopentest.py scan example.com --vuln-only

# Payload generation only
python3 autopentest.py scan example.com --payload-only
```

### Individual Modules
```bash
# Reconnaissance
python3 autopentest.py recon example.com

# Vulnerability scanning
python3 autopentest.py vuln https://example.com

# Custom payload generation
python3 autopentest.py payload reverse_shell linux --lhost 192.168.1.100 --lport 4444
```

### Report Generation
```bash
# Generate HTML report (default)
python3 autopentest.py scan example.com --report-format html

# Generate Markdown report
python3 autopentest.py scan example.com --report-format markdown

# Generate from existing scan files
python3 autopentest.py report recon_*.json vulnscan_*.json --format html
```

## 📊 Output Structure

```
reports/
├── scans/
│   ├── recon_example_com_2024-01-15T10-30-00.json
│   ├── vulnscan_example_com_2024-01-15T10-45-00.json
│   └── payloads_example_com_2024-01-15T11-00-00.json
├── reports/
│   ├── pentest_report_example_com_2024-01-15T11-15-00.html
│   ├── pentest_report_example_com_2024-01-15T11-15-00.md
│   └── pentest_data_example_com_2024-01-15T11-15-00.json
├── payloads/
│   ├── payload_linux_elf.elf
│   ├── payload_windows_exe.exe
│   └── webshell.php
└── pentesting.log
```

## 🛡️ Ethical Usage

**⚠️ IMPORTANT DISCLAIMER**

This tool is designed for **authorized security testing only**. Users are responsible for ensuring they have proper authorization before testing any systems.

### Legal Usage Guidelines:
- ✅ Only test systems you own or have explicit written permission to test
- ✅ Comply with all applicable laws and regulations in your jurisdiction
- ✅ Use for educational purposes in controlled lab environments
- ✅ Responsible disclosure of any vulnerabilities found

### Prohibited Usage:
- ❌ Testing systems without authorization
- ❌ Malicious activities or actual exploitation
- ❌ Any illegal or unauthorized access attempts
- ❌ Violating terms of service or acceptable use policies

## 🔧 Advanced Usage

### Custom Tool Paths
```bash
export NMAP_PATH="/custom/path/to/nmap"
export NUCLEI_PATH="/custom/path/to/nuclei"
python3 autopentest.py scan example.com
```

### Custom Output Directory
```bash
python3 autopentest.py scan example.com --output /custom/output/path
```

### Verbose Logging
```bash
python3 autopentest.py --verbose scan example.com
```

### Configuration Check
```bash
python3 autopentest.py --config-check
```

## 🐛 Troubleshooting

### Common Issues

**Tool Not Found Errors**
```bash
# Check tool availability
python3 autopentest.py --config-check

# Install missing tools or update paths in .env
```

**Permission Errors**
```bash
# Make sure you have execute permissions
chmod +x autopentest.py

# Some tools may require sudo
sudo python3 autopentest.py scan example.com
```

**API Errors**
```bash
# Verify API keys in .env file
# Check API rate limits and quotas
```

### Debug Mode
```bash
python3 autopentest.py --verbose scan example.com
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yourusername/autopentest.git
cd autopentest
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt  # Development dependencies
```

### Running Tests
```bash
python3 -m pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Nmap Project** - Network discovery and security auditing
- **ProjectDiscovery** - Nuclei vulnerability scanner
- **NIKTOV** - Web server scanner
- **SQLMap** - SQL injection detection
- **OWASP** - Security guidelines and methodologies
- **Metasploit Framework** - Penetration testing platform
- **Shodan** - Internet-connected device search engine

## 📬 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/autopentest/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/autopentest/discussions)
- 📧 **Email**: security@yourorg.com

---

**Remember: Use responsibly and only on systems you own or have explicit permission to test.**
