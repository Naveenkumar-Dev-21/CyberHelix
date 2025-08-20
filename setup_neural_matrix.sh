#!/bin/bash

# Neural Command Center Setup Script
# Automated installation for the Matrix Pentesting Framework

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  🔴 THE MATRIX SETUP 🔴                     ║"
echo "║              Neural Command Center Installation              ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "Don't run this script as root! Neural links require user privileges."
   exit 1
fi

print_info "Initializing Matrix neural link setup..."

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python $PYTHON_VERSION detected (requirement: $REQUIRED_VERSION+)"
else
    print_error "Python $REQUIRED_VERSION+ required, found $PYTHON_VERSION"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 not found. Install python3-pip first."
    exit 1
fi

print_status "pip3 is available"

# Install Python dependencies
print_info "Installing Python dependencies for Neural Command Center..."

if pip3 install -r requirements.txt; then
    print_status "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Check for system tools
print_info "Checking for penetration testing tools..."

# Array of tools to check
tools=("nmap" "curl" "wget" "git")
missing_tools=()

for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        print_status "$tool is installed"
    else
        print_warning "$tool is not installed"
        missing_tools+=("$tool")
    fi
done

# Optional tools
optional_tools=("nuclei" "nikto" "sqlmap" "amass" "subfinder" "gobuster" "msfconsole")
print_info "Checking optional penetration testing tools..."

for tool in "${optional_tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        print_status "$tool is available"
    else
        print_warning "$tool is not installed (optional)"
    fi
done

# Install missing essential tools
if [ ${#missing_tools[@]} -ne 0 ]; then
    print_warning "Some essential tools are missing: ${missing_tools[*]}"
    
    # Detect package manager and suggest installation
    if command -v apt-get &> /dev/null; then
        print_info "Detected apt package manager. To install missing tools:"
        echo "sudo apt-get update && sudo apt-get install ${missing_tools[*]}"
    elif command -v yum &> /dev/null; then
        print_info "Detected yum package manager. To install missing tools:"
        echo "sudo yum install ${missing_tools[*]}"
    elif command -v pacman &> /dev/null; then
        print_info "Detected pacman package manager. To install missing tools:"
        echo "sudo pacman -S ${missing_tools[*]}"
    else
        print_info "Please install these tools using your system's package manager"
    fi
fi

# Setup directories
print_info "Setting up Matrix directory structure..."

DIRS=("reports" "logs" "payloads" "wordlists")
for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_status "Created directory: $dir"
    else
        print_status "Directory exists: $dir"
    fi
done

# Check .env file
if [ ! -f ".env" ]; then
    print_warning ".env file not found, creating template..."
    cat > .env << 'EOF'
# API Keys - Add your actual keys here
SHODAN_API_KEY=your_shodan_api_key_here
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here

# Tool Paths (optional - tools will be searched in PATH)
NMAP_PATH=/usr/bin/nmap
NUCLEI_PATH=/usr/bin/nuclei
NIKTO_PATH=/usr/bin/nikto
SQLMAP_PATH=/usr/bin/sqlmap
AMASS_PATH=/usr/bin/amass
THEHARVESTER_PATH=/usr/bin/theHarvester
MSFVENOM_PATH=/usr/bin/msfvenom

# Output Settings
OUTPUT_DIR=./reports
LOG_LEVEL=INFO

# Neural Command Center Settings
NEURAL_AI_MODEL=gpt-3.5-turbo
MAX_CONVERSATION_HISTORY=50
EXPLOITATION_MODE=enabled
STEALTH_MODE=disabled
EOF
    print_status "Created .env template file"
    print_warning "Edit .env file to add your API keys"
else
    print_status ".env file exists"
fi

# Make scripts executable
print_info "Making scripts executable..."
chmod +x launch_neural_command.py
chmod +x *.sh 2>/dev/null || true
print_status "Scripts are now executable"

# Test the neural command launcher
print_info "Testing Neural Command Center launcher..."
if python3 -c "import sys; sys.path.insert(0, 'src'); from neural_command_ai import NeuralCommandAI; print('Neural AI import successful')"; then
    print_status "Neural Command AI components loaded successfully"
else
    print_warning "Neural Command AI components may have issues"
fi

# Final setup message
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🔴 SETUP COMPLETE 🔴                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
print_status "Matrix Neural Command Center is ready!"
echo ""
print_info "To launch the Neural Command Center:"
echo -e "${CYAN}./launch_neural_command.py${NC}"
echo ""
print_info "To launch the basic Matrix GUI:"
echo -e "${CYAN}python3 src/gui/matrix_gui.py${NC}"
echo ""
print_warning "IMPORTANT:"
echo "1. Edit .env file to add your API keys"
echo "2. Install optional tools for full functionality"
echo "3. Ensure you have permission to test target systems"
echo ""
echo -e "${RED}🔴 Remember: With great power comes great responsibility.${NC}"
echo -e "${CYAN}💊 Use the Neural Command Center ethically and legally.${NC}"
echo ""
