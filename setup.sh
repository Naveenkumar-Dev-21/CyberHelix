#!/bin/bash

# AutoPenTest Setup Script
# Installs dependencies and configures the automated penetration testing tool

set -e

echo "🔧 Setting up AutoPenTest - Automated Penetration Testing Framework"
echo "=================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root for some operations
check_root() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${YELLOW}Warning: Running as root. Some tools will be installed system-wide.${NC}"
    fi
}

# Install Python dependencies
install_python_deps() {
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    pip3 install -r requirements.txt
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
}

# Install system tools (Ubuntu/Debian)
install_system_tools_debian() {
    echo -e "${BLUE}🔧 Installing system tools (Debian/Ubuntu)...${NC}"
    
    sudo apt update
    
    # Essential tools
    sudo apt install -y nmap nikto sqlmap amass curl wget git
    
    # Install Nuclei
    if ! command -v nuclei &> /dev/null; then
        echo -e "${BLUE}Installing Nuclei...${NC}"
        GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
        # Add Go bin to PATH if not already there
        if [[ ":$PATH:" != *":$HOME/go/bin:"* ]]; then
            echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
            export PATH=$PATH:$HOME/go/bin
        fi
    fi
    
    # Install theHarvester
    if ! command -v theHarvester &> /dev/null; then
        echo -e "${BLUE}Installing theHarvester...${NC}"
        pip3 install theHarvester
    fi
    
    # Check for Metasploit Framework
    if ! command -v msfvenom &> /dev/null; then
        echo -e "${YELLOW}⚠️  Metasploit Framework not found. Install manually if needed for payload generation.${NC}"
        echo -e "${BLUE}   Installation command: curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall${NC}"
    fi
    
    echo -e "${GREEN}✅ System tools installation complete${NC}"
}

# Install system tools (Arch Linux)
install_system_tools_arch() {
    echo -e "${BLUE}🔧 Installing system tools (Arch Linux)...${NC}"
    
    sudo pacman -Syu --noconfirm
    sudo pacman -S --noconfirm nmap nikto sqlmap git curl wget
    
    # Install from AUR if needed
    if command -v yay &> /dev/null; then
        yay -S --noconfirm nuclei amass
    elif command -v paru &> /dev/null; then
        paru -S --noconfirm nuclei amass
    else
        echo -e "${YELLOW}⚠️  AUR helper not found. Install nuclei and amass manually.${NC}"
    fi
    
    echo -e "${GREEN}✅ System tools installation complete${NC}"
}

# Setup environment file
setup_environment() {
    echo -e "${BLUE}🔐 Setting up environment configuration...${NC}"
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env file from template${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env file and add your API keys${NC}"
    else
        echo -e "${YELLOW}⚠️  .env file already exists${NC}"
    fi
}

# Make scripts executable
setup_permissions() {
    echo -e "${BLUE}🔑 Setting up permissions...${NC}"
    chmod +x autopentest.py
    chmod +x setup.sh
    echo -e "${GREEN}✅ Permissions set${NC}"
}

# Create directories
create_directories() {
    echo -e "${BLUE}📁 Creating output directories...${NC}"
    mkdir -p reports/{scans,reports,payloads}
    echo -e "${GREEN}✅ Output directories created${NC}"
}

# Main installation function
main() {
    echo -e "${BLUE}Starting AutoPenTest setup...${NC}"
    
    check_root
    
    # Detect OS
    if [ -f /etc/debian_version ]; then
        DISTRO="debian"
    elif [ -f /etc/arch-release ]; then
        DISTRO="arch"
    else
        DISTRO="unknown"
        echo -e "${YELLOW}⚠️  Unknown distribution. You may need to install tools manually.${NC}"
    fi
    
    # Install Python dependencies
    install_python_deps
    
    # Install system tools based on distro
    case $DISTRO in
        debian)
            install_system_tools_debian
            ;;
        arch)
            install_system_tools_arch
            ;;
        *)
            echo -e "${YELLOW}⚠️  Please install system tools manually:${NC}"
            echo -e "${BLUE}   Required: nmap, nikto, sqlmap, nuclei, amass, theHarvester${NC}"
            echo -e "${BLUE}   Optional: msfvenom (Metasploit Framework)${NC}"
            ;;
    esac
    
    # Setup environment and permissions
    setup_environment
    setup_permissions
    create_directories
    
    echo ""
    echo -e "${GREEN}🎉 AutoPenTest setup complete!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo -e "${YELLOW}1. Edit .env file and add your API keys (optional)${NC}"
    echo -e "${YELLOW}2. Test the installation: python3 autopentest.py --config-check${NC}"
    echo -e "${YELLOW}3. Run your first scan: python3 autopentest.py scan example.com${NC}"
    echo ""
    echo -e "${RED}⚠️  IMPORTANT: Only use this tool on systems you own or have explicit permission to test!${NC}"
    echo ""
}

# Run main function
main "$@"
