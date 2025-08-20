#!/bin/bash

# MobSF (Mobile Security Framework) Setup Script
# This script sets up MobSF for static and dynamic mobile app testing

set -e

echo "========================================"
echo "MobSF Setup for Mobile App Testing"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}This script should not be run as root!${NC}"
   exit 1
fi

# Function to print colored output
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check system requirements
print_status "Checking system requirements..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_success "Python3 found: $(python3 --version)"
else
    print_error "Python3 is not installed!"
    exit 1
fi

# Check Docker (optional but recommended for dynamic analysis)
if command -v docker &> /dev/null; then
    print_success "Docker found: $(docker --version)"
    DOCKER_AVAILABLE=true
else
    print_warning "Docker not found. Dynamic analysis features will be limited."
    DOCKER_AVAILABLE=false
fi

# Check Git
if command -v git &> /dev/null; then
    print_success "Git found"
else
    print_error "Git is not installed!"
    exit 1
fi

# Create MobSF directory
MOBSF_DIR="$HOME/tools/MobSF"
print_status "Setting up MobSF in $MOBSF_DIR..."

mkdir -p "$HOME/tools"

# Clone or update MobSF
if [ -d "$MOBSF_DIR" ]; then
    print_status "MobSF directory exists, updating..."
    cd "$MOBSF_DIR"
    git pull origin master
else
    print_status "Cloning MobSF repository..."
    git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF.git "$MOBSF_DIR"
    cd "$MOBSF_DIR"
fi

# Install dependencies
print_status "Installing MobSF dependencies..."

# Install system dependencies
print_status "Installing system packages..."
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    sudo apt-get update
    sudo apt-get install -y \
        python3-pip \
        python3-venv \
        openjdk-11-jdk \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        libjpeg-dev \
        zlib1g-dev \
        wkhtmltopdf
elif command -v pacman &> /dev/null; then
    # Arch/Garuda Linux
    sudo pacman -S --needed --noconfirm \
        python-pip \
        jdk11-openjdk \
        openssl \
        libffi \
        libxml2 \
        libxslt \
        libjpeg-turbo \
        zlib \
        wkhtmltopdf
elif command -v dnf &> /dev/null; then
    # Fedora
    sudo dnf install -y \
        python3-pip \
        java-11-openjdk \
        openssl-devel \
        libffi-devel \
        libxml2-devel \
        libxslt-devel \
        libjpeg-devel \
        zlib-devel \
        wkhtmltopdf
fi

# Set up Python virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d "$MOBSF_DIR/venv" ]; then
    python3 -m venv "$MOBSF_DIR/venv"
fi

# Activate virtual environment and install requirements
source "$MOBSF_DIR/venv/bin/activate"
pip install --upgrade pip setuptools wheel
pip install -r "$MOBSF_DIR/requirements.txt"

# Additional tools for enhanced mobile testing
print_status "Installing additional mobile testing tools..."

# Install Frida for dynamic instrumentation
pip install frida-tools

# Install Objection for runtime mobile exploration
pip install objection

# Create MobSF configuration
print_status "Creating MobSF configuration..."

# Generate a secure API key
API_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')

# Create .env file for the pentesting project
ENV_FILE="$HOME/Documents/Projects/automatic-pentesting/.env"
if [ -f "$ENV_FILE" ]; then
    print_status "Updating existing .env file..."
    # Remove old MobSF entries if they exist
    sed -i '/^MOBSF_/d' "$ENV_FILE"
else
    print_status "Creating new .env file..."
fi

# Add MobSF configuration to .env
cat >> "$ENV_FILE" << EOF

# MobSF Configuration
MOBSF_URL=http://127.0.0.1:8000
MOBSF_API_KEY=$API_KEY
MOBSF_DIR=$MOBSF_DIR

EOF

print_success "MobSF API Key generated: $API_KEY"

# Create MobSF settings file
MOBSF_SETTINGS="$MOBSF_DIR/MobSF/settings.py"
print_status "Configuring MobSF settings..."

# Create a local settings override
cat > "$MOBSF_DIR/local_settings.py" << EOF
# MobSF Local Settings
import os

# API Key for authentication
API_KEY = '$API_KEY'

# Enable API mode
API_ONLY = False

# Allow remote connections (set to False for security in production)
ALLOWED_HOSTS = ['*']

# Upload size limit (in MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 512 * 1024 * 1024  # 512MB

# Enable all analyzers
ANDROID_DYNAMIC_ANALYZER = True
IOS_DYNAMIC_ANALYZER = True

# Configure for better performance
ASYNC_ANALYSIS = True
PARALLEL_ANALYSIS = True

# Enable additional security checks
NIAP_ANALYSIS = True
PRIVACY_ANALYSIS = True

EOF

# Create systemd service for MobSF (optional)
print_status "Creating systemd service for MobSF..."
sudo tee /etc/systemd/system/mobsf.service > /dev/null << EOF
[Unit]
Description=Mobile Security Framework (MobSF)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$MOBSF_DIR
Environment="PATH=$MOBSF_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=$MOBSF_DIR/venv/bin/python $MOBSF_DIR/manage.py runserver 0.0.0.0:8000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create helper scripts
print_status "Creating helper scripts..."

# Start script
cat > "$HOME/tools/start_mobsf.sh" << 'EOF'
#!/bin/bash
MOBSF_DIR="$HOME/tools/MobSF"
cd "$MOBSF_DIR"
source venv/bin/activate
python manage.py makemigrations
python manage.py makemigrations StaticAnalyzer
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
EOF

chmod +x "$HOME/tools/start_mobsf.sh"

# Stop script
cat > "$HOME/tools/stop_mobsf.sh" << 'EOF'
#!/bin/bash
pkill -f "manage.py runserver"
echo "MobSF stopped"
EOF

chmod +x "$HOME/tools/stop_mobsf.sh"

# Docker setup for dynamic analysis (if Docker is available)
if [ "$DOCKER_AVAILABLE" = true ]; then
    print_status "Setting up Docker for dynamic analysis..."
    
    # Pull MobSF Docker image
    docker pull opensecurity/mobile-security-framework-mobsf:latest
    
    # Create docker-compose file
    cat > "$HOME/tools/docker-compose-mobsf.yml" << 'EOF'
version: '3.7'

services:
  mobsf:
    image: opensecurity/mobile-security-framework-mobsf:latest
    container_name: mobsf
    ports:
      - "8000:8000"
      - "1337:1337"  # Frida server port
    volumes:
      - mobsf-data:/root/.MobSF
      - ./uploads:/root/Mobile-Security-Framework-MobSF/uploads
    environment:
      - MOBSF_API_KEY=${MOBSF_API_KEY}
      - MOBSF_ASYNC_ANALYSIS=1
      - MOBSF_PARALLEL_ANALYSIS=1
    restart: unless-stopped

  # Android Emulator for Dynamic Analysis
  android-emulator:
    image: budtmo/docker-android-x86-11.0:latest
    container_name: android-emulator
    privileged: true
    ports:
      - "6080:6080"  # noVNC port
      - "5554:5554"  # ADB port
      - "5555:5555"  # ADB port
    environment:
      - DEVICE=Samsung Galaxy S10
      - DATAPARTITION=2g
    restart: unless-stopped

volumes:
  mobsf-data:
EOF
    
    print_success "Docker setup complete for dynamic analysis"
fi

# Install Android tools for dynamic analysis
print_status "Setting up Android tools..."

# Check if Android SDK is installed
if [ -z "$ANDROID_HOME" ]; then
    print_warning "ANDROID_HOME not set. Installing Android SDK..."
    
    # Download and install Android command line tools
    ANDROID_SDK_DIR="$HOME/Android/Sdk"
    mkdir -p "$ANDROID_SDK_DIR"
    
    # Download command line tools
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O /tmp/cmdline-tools.zip
    unzip -q /tmp/cmdline-tools.zip -d "$ANDROID_SDK_DIR"
    rm /tmp/cmdline-tools.zip
    
    # Set up environment variables
    echo "export ANDROID_HOME=$ANDROID_SDK_DIR" >> ~/.bashrc
    echo "export PATH=\$PATH:\$ANDROID_HOME/cmdline-tools/latest/bin:\$ANDROID_HOME/platform-tools" >> ~/.bashrc
    
    # Install essential Android SDK components
    yes | "$ANDROID_SDK_DIR/cmdline-tools/bin/sdkmanager" --sdk_root="$ANDROID_SDK_DIR" \
        "platform-tools" \
        "platforms;android-33" \
        "build-tools;33.0.0"
fi

# Install ADB if not present
if ! command -v adb &> /dev/null; then
    print_status "Installing ADB..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y android-tools-adb
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --needed --noconfirm android-tools
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y android-tools
    fi
fi

# Install additional mobile testing tools
print_status "Installing additional mobile pentesting tools..."

# APKTool for decompiling
if ! command -v apktool &> /dev/null; then
    print_status "Installing APKTool..."
    wget -q https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O "$HOME/tools/apktool"
    wget -q https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.8.1.jar -O "$HOME/tools/apktool.jar"
    chmod +x "$HOME/tools/apktool"
    echo "alias apktool='$HOME/tools/apktool'" >> ~/.bashrc
fi

# JADX for Java decompilation
if ! command -v jadx &> /dev/null; then
    print_status "Installing JADX..."
    wget -q https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip -O /tmp/jadx.zip
    unzip -q /tmp/jadx.zip -d "$HOME/tools/jadx"
    chmod +x "$HOME/tools/jadx/bin/jadx"
    chmod +x "$HOME/tools/jadx/bin/jadx-gui"
    echo "export PATH=\$PATH:$HOME/tools/jadx/bin" >> ~/.bashrc
    rm /tmp/jadx.zip
fi

# Create test script
print_status "Creating MobSF test script..."

cat > "$HOME/tools/test_mobsf.py" << 'EOF'
#!/usr/bin/env python3
"""
MobSF API Test Script
Tests MobSF installation and API functionality
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

# Load configuration from .env
def load_env():
    env_file = Path.home() / "Documents/Projects/automatic-pentesting/.env"
    config = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value.strip('"').strip("'")
    return config

def test_mobsf_connection(base_url, api_key):
    """Test MobSF API connection"""
    headers = {'Authorization': api_key}
    try:
        response = requests.get(f"{base_url}/api/v1/scans", headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"✅ MobSF API is accessible at {base_url}")
            return True
        else:
            print(f"❌ MobSF API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to MobSF: {e}")
        return False

def test_static_analysis(base_url, api_key, sample_apk):
    """Test static analysis capability"""
    headers = {'Authorization': api_key}
    
    # Upload APK
    print("📤 Uploading sample APK for static analysis...")
    with open(sample_apk, 'rb') as f:
        files = {'file': (os.path.basename(sample_apk), f, 'application/vnd.android.package-archive')}
        response = requests.post(f"{base_url}/api/v1/upload", headers=headers, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ APK uploaded successfully. Hash: {result.get('hash', 'N/A')}")
        
        # Start static scan
        scan_data = {
            'hash': result['hash'],
            'scan_type': result.get('scan_type', 'apk'),
            'file_name': result.get('file_name', os.path.basename(sample_apk))
        }
        
        print("🔍 Starting static analysis...")
        scan_response = requests.post(f"{base_url}/api/v1/scan", headers=headers, data=scan_data)
        
        if scan_response.status_code == 200:
            print("✅ Static analysis completed successfully")
            return True
        else:
            print(f"❌ Static analysis failed: {scan_response.text}")
            return False
    else:
        print(f"❌ Failed to upload APK: {response.text}")
        return False

def check_dynamic_analysis_setup(base_url, api_key):
    """Check if dynamic analysis is properly configured"""
    headers = {'Authorization': api_key}
    
    print("🔧 Checking dynamic analysis setup...")
    
    # Check for connected devices
    try:
        import subprocess
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = [line for line in result.stdout.split('\n') if '\tdevice' in line]
        
        if devices:
            print(f"✅ Found {len(devices)} connected device(s)")
            for device in devices:
                print(f"   📱 {device.split()[0]}")
            return True
        else:
            print("⚠️  No Android devices found for dynamic analysis")
            print("   Tip: Connect a device or start an emulator")
            return False
    except FileNotFoundError:
        print("❌ ADB not found. Dynamic analysis requires Android SDK")
        return False

def main():
    print("="*50)
    print("MobSF Installation Test")
    print("="*50)
    
    # Load configuration
    config = load_env()
    base_url = config.get('MOBSF_URL', 'http://127.0.0.1:8000')
    api_key = config.get('MOBSF_API_KEY', '')
    
    if not api_key:
        print("❌ MOBSF_API_KEY not found in .env file")
        sys.exit(1)
    
    print(f"🔗 MobSF URL: {base_url}")
    print(f"🔑 API Key: {api_key[:10]}..." if len(api_key) > 10 else api_key)
    print()
    
    # Test connection
    if not test_mobsf_connection(base_url, api_key):
        print("\n⚠️  Make sure MobSF is running:")
        print("   Run: ~/tools/start_mobsf.sh")
        sys.exit(1)
    
    # Check dynamic analysis
    check_dynamic_analysis_setup(base_url, api_key)
    
    print("\n✅ MobSF is properly configured and ready for mobile app testing!")
    print("\nUsage:")
    print("  Start MobSF: ~/tools/start_mobsf.sh")
    print("  Stop MobSF:  ~/tools/stop_mobsf.sh")
    print("  Web UI:      http://127.0.0.1:8000")
    print(f"  API Key:     {api_key}")

if __name__ == "__main__":
    main()
EOF

chmod +x "$HOME/tools/test_mobsf.py"

# Initialize MobSF database
print_status "Initializing MobSF database..."
cd "$MOBSF_DIR"
source venv/bin/activate
python manage.py makemigrations
python manage.py makemigrations StaticAnalyzer
python manage.py migrate

# Summary
echo ""
echo "========================================"
echo -e "${GREEN}MobSF Setup Complete!${NC}"
echo "========================================"
echo ""
echo "📍 Installation Directory: $MOBSF_DIR"
echo "🔑 API Key: $API_KEY"
echo "🌐 URL: http://127.0.0.1:8000"
echo ""
echo "📝 Configuration saved to: $ENV_FILE"
echo ""
echo "🚀 Quick Start Commands:"
echo "   Start MobSF:    ~/tools/start_mobsf.sh"
echo "   Stop MobSF:     ~/tools/stop_mobsf.sh"
echo "   Test MobSF:     python3 ~/tools/test_mobsf.py"
echo ""
echo "🐳 Docker Commands (if available):"
echo "   Start with Docker: docker-compose -f ~/tools/docker-compose-mobsf.yml up -d"
echo "   Stop Docker:       docker-compose -f ~/tools/docker-compose-mobsf.yml down"
echo ""
echo "📱 For Dynamic Analysis:"
echo "   1. Connect an Android device via USB with debugging enabled"
echo "   2. Or start an Android emulator"
echo "   3. Run: adb devices (to verify connection)"
echo ""
echo "⚠️  Note: Remember to source ~/.bashrc or restart terminal for PATH updates"
echo ""
print_warning "To start using MobSF now, run: ~/tools/start_mobsf.sh"
