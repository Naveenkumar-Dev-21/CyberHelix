# Matrix Pentesting Suite - Desktop Application

## 🎯 Overview

A comprehensive desktop application that integrates the Matrix UI with a powerful backend to provide a complete cybersecurity pentesting platform. The application features a modern GUI, real-time backend integration, and support for all 8 major pentesting categories.

## 🚀 Quick Start

### One-Click Launch

```bash
# Make launcher executable
chmod +x launch_app.sh

# Run the application
./launch_app.sh
```

### Manual Launch

```bash
# Install dependencies
pip install --break-system-packages -r desktop_requirements.txt

# Start the application
python desktop_app.py
```

## 📋 System Architecture

```
┌─────────────────────────────────────────┐
│         Desktop Application GUI         │
│  (CustomTkinter + WebView + Matrix UI)  │
└────────────────┬────────────────────────┘
                 │
     ┌───────────▼───────────┐
     │   Backend Process     │
     │  (FastAPI + WebSocket) │
     └───────────┬───────────┘
                 │
┌────────────────▼────────────────────────┐
│         21+ Pentesting Modules          │
│ (Network, Web, Mobile, Wireless, etc.)  │
└─────────────────────────────────────────┘
```

## 🎨 Features

### Desktop Application Features

- **Modern GUI Interface** - Built with CustomTkinter
- **Integrated Matrix UI** - WebView with Matrix-style interface
- **Real-time Updates** - WebSocket connection for live results
- **Multi-tab Interface** - Dashboard, Active Scans, Results, Console
- **Quick Actions Sidebar** - Fast access to common operations
- **Task Management** - Monitor and control running scans
- **Export Capabilities** - Save results in multiple formats

### Backend Integration

- **Embedded Backend Server** - Automatically starts with application
- **RESTful API** - Full API access at `http://localhost:8000`
- **WebSocket Support** - Real-time task updates
- **Asynchronous Execution** - Non-blocking operations
- **Smart Result Filtering** - Returns only relevant data

### Supported Pentesting Types

1. **Network Scanning & Reconnaissance**
   - Port scanning
   - Service enumeration
   - DNS reconnaissance
   - OSINT gathering

2. **Web Application Testing**
   - Vulnerability scanning
   - SQL injection testing
   - XSS detection
   - Security header analysis

3. **Exploitation & Security**
   - Exploit execution
   - Payload generation
   - Privilege escalation
   - Post-exploitation

4. **Mobile Application Testing**
   - APK analysis
   - Static/dynamic testing
   - Permission analysis
   - Code review

5. **Wireless Network Testing**
   - Wi-Fi scanning
   - WPA handshake capture
   - Deauth attacks
   - Password cracking

6. **Cloud Infrastructure Assessment**
   - AWS security audit
   - Configuration review
   - Compliance checking
   - Resource analysis

7. **IoT & Firmware Analysis**
   - Firmware extraction
   - Binary analysis
   - Vulnerability identification
   - Protocol testing

8. **AI/ML Automation**
   - Intelligent target analysis
   - Automated vulnerability prioritization
   - Pattern recognition
   - Predictive modeling

## 🖥️ User Interface

### Main Window Components

1. **Menu Bar**
   - File: New Scan, Import/Export, Exit
   - Tools: Quick access to scanners
   - View: UI options and themes
   - Help: Documentation and support

2. **Sidebar**
   - Target input field
   - Scan type selector
   - Quick scan button
   - Module buttons
   - Matrix UI launcher

3. **Content Area (Tabs)**
   - **Dashboard**: Statistics and activity
   - **Active Scans**: Running task monitor
   - **Results**: Scan output viewer
   - **Console**: Command-line interface

4. **Status Bar**
   - Current status message
   - Backend connection indicator

### Matrix UI Integration

The embedded Matrix UI provides:
- Matrix rain animation
- Green-on-black terminal aesthetic
- Real-time scan visualization
- Interactive control panel

## 🔧 Configuration

### Application Settings

Create `.env` file for configuration:

```env
# Backend Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

# API Keys
SHODAN_API_KEY=your-key-here
VIRUSTOTAL_API_KEY=your-key-here

# Output Settings
OUTPUT_DIR=./output
LOG_LEVEL=INFO

# UI Settings
THEME=dark
AUTO_CONNECT=true
```

### Module Configuration

Modules are automatically loaded from the `src/` directory. Each module can be configured individually through the GUI or API.

## 📡 API Integration

### JavaScript Integration (for custom UI)

```javascript
// Connect to backend from custom web UI
const API_URL = 'http://localhost:8000';

async function runScan(target, type) {
    const response = await fetch(`${API_URL}/execute`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            test_type: type,
            target: target,
            async_execution: true
        })
    });
    return await response.json();
}

// WebSocket for real-time updates
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
};
```

### Python Integration

```python
from matrix_frontend_integration import MatrixBackendClient

async def run_scan():
    client = MatrixBackendClient()
    await client.connect()
    
    result = await client.execute_scan(
        test_type="vulnerability_scan",
        target="example.com"
    )
    return result
```

## 🎮 Usage Examples

### Quick Scan via GUI

1. Enter target in sidebar
2. Select scan type
3. Click "Start Scan"
4. View results in Results tab

### Console Commands

Available commands in Console tab:
- `scan <target>` - Start quick scan
- `status` - Show backend status
- `tasks` - List active tasks
- `clear` - Clear console
- `help` - Show help

### Batch Operations

```python
# Execute multiple scans
targets = ["192.168.1.1", "example.com", "10.0.0.1"]
for target in targets:
    # Each scan runs asynchronously
    execute_scan("network_scan", target)
```

## 🔍 Troubleshooting

### Common Issues

1. **Backend won't start**
   ```bash
   # Check if port 8000 is in use
   lsof -i :8000
   # Kill existing process
   kill -9 $(lsof -t -i:8000)
   ```

2. **GUI doesn't launch**
   ```bash
   # Install GUI dependencies
   pip install --break-system-packages customtkinter pywebview
   ```

3. **Module import errors**
   ```bash
   # Ensure src directory exists
   ls -la src/
   # Check Python path
   echo $PYTHONPATH
   ```

4. **WebSocket connection failed**
   - Ensure backend is running
   - Check firewall settings
   - Verify localhost connectivity

### Debug Mode

```bash
# Run with debug logging
python desktop_app.py --debug

# Check logs
tail -f desktop_app.log
tail -f backend_server.log
```

## 📦 Deployment

### Standalone Executable

Create standalone executable with PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed \
    --add-data "src:src" \
    --add-data "assets:assets" \
    --name "MatrixPentest" \
    desktop_app.py

# Executable will be in dist/MatrixPentest
```

### Docker Container

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r desktop_requirements.txt
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox

ENV DISPLAY=:99
CMD Xvfb :99 -screen 0 1024x768x16 & \
    fluxbox & \
    x11vnc -display :99 -forever & \
    python desktop_app.py
```

### System Service

Create systemd service for auto-start:

```ini
[Unit]
Description=Matrix Pentesting Desktop App
After=graphical.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/python3 /path/to/app/desktop_app.py
Restart=always

[Install]
WantedBy=default.target
```

## 🔐 Security Considerations

1. **Local Only by Default** - Backend binds to 127.0.0.1
2. **API Authentication** - Optional API key support
3. **Process Isolation** - Backend runs in separate process
4. **Input Validation** - All inputs sanitized
5. **Secure Communication** - HTTPS/WSS support available

## 📊 Performance

- **Concurrent Scans**: Up to 10 simultaneous operations
- **Memory Usage**: ~200MB baseline, scales with tasks
- **Response Time**: <100ms for API calls
- **WebSocket Latency**: <50ms for updates

## 🎨 Customization

### Theme Customization

```python
# In desktop_app.py
ctk.set_appearance_mode("dark")  # or "light"
ctk.set_default_color_theme("blue")  # or "green", "dark-blue"
```

### Adding Custom Modules

1. Create module in `src/` directory
2. Register in `module_manager.py`
3. Module appears automatically in GUI

### Custom Matrix UI

Edit `src/gui/matrix_gui.html` to customize:
- Animation effects
- Color schemes
- Control panels
- Display formats

## 🔗 Integration Points

- **CLI Interface**: Full CLI available via `cli_main.py`
- **API Endpoint**: REST API at port 8000
- **WebSocket**: Real-time updates at ws://localhost:8000/ws
- **Module System**: Extensible module architecture
- **Export Formats**: JSON, HTML, TXT, PDF

## 📈 Monitoring

### Application Metrics

- Active tasks counter
- Memory usage monitor
- API response times
- WebSocket connections
- Module execution stats

### Logging

All operations logged to:
- `desktop_app.log` - Application events
- `backend_server.log` - Backend operations
- `output/` - Scan results
- `reports/` - Generated reports

## 🆘 Support

### Resources

- API Documentation: http://localhost:8000/docs
- Module Documentation: See individual module READMEs
- Issue Tracker: GitHub Issues
- Community: Discord/Slack

### Contact

For bugs, features, or questions:
1. Check existing documentation
2. Review application logs
3. Test with debug mode
4. Submit detailed issue report

## 📝 License

This tool is for authorized security testing only. Users are responsible for complying with all applicable laws and obtaining proper authorization before testing any systems.

---

**Note**: The desktop application integrates all pentesting capabilities into a unified, user-friendly interface while maintaining the power and flexibility of the command-line tools and API backend.
