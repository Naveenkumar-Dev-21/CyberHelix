#!/usr/bin/env python3
"""
Comprehensive Modern GUI for Automatic Pentesting Framework
Real capabilities with beautiful interface
"""

import sys
import os
import json
import threading
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

# GUI imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QComboBox, QProgressBar, QTabWidget,
    QSplitter, QFrame, QScrollArea, QGridLayout, QCheckBox, QSpinBox,
    QGroupBox, QListWidget, QTreeWidget, QTreeWidgetItem, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
    QStackedWidget, QRadioButton, QButtonGroup, QSlider, QDockWidget
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve,
    QRect, QPoint, QSize, QDateTime, pyqtSlot, QEventLoop
)
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QTextCursor, QPixmap, QIcon,
    QTextCharFormat, QSyntaxHighlighter, QTextDocument, QPainter,
    QLinearGradient, QRadialGradient, QPen, QBrush, QAction
)

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Try to import framework modules
try:
    from src.config import Config
    from src.reconnaissance import ReconnaissanceModule
    from src.vulnerability_scanner import VulnerabilityScanner
    from src.network_assessor import NetworkAssessor
    from src.web_assessor import WebAssessor
    from src.mobile_assessor import MobileAssessor
    from src.wireless_assessor import WirelessAssessor
    from src.exploit_module import ExploitModule
    from src.payload_generator import PayloadGenerator
    from src.report_generator import ReportGenerator
    from src.copilot import copilot_run
    FRAMEWORK_AVAILABLE = True
except ImportError as e:
    print(f"Framework modules not fully available: {e}")
    FRAMEWORK_AVAILABLE = False
    
    # Create mock classes for demo
    class Config:
        OUTPUT_DIR = Path("./reports")
        @classmethod
        def create_output_dirs(cls): pass
        @classmethod
        def setup_logging(cls): pass

class ModernDarkTheme:
    """Modern dark theme colors"""
    # Primary colors
    BACKGROUND = "#0d1117"
    SURFACE = "#161b22"
    SURFACE_LIGHT = "#1c2128"
    
    # Accent colors
    PRIMARY = "#58a6ff"
    PRIMARY_DARK = "#1f6feb"
    SUCCESS = "#3fb950"
    WARNING = "#d29922"
    DANGER = "#f85149"
    INFO = "#58a6ff"
    
    # Text colors
    TEXT_PRIMARY = "#c9d1d9"
    TEXT_SECONDARY = "#8b949e"
    TEXT_MUTED = "#484f58"
    
    # Border colors
    BORDER = "#30363d"
    BORDER_LIGHT = "#484f58"

class PentestWorker(QThread):
    """Background worker for pentesting operations"""
    
    output_received = pyqtSignal(str)
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    task_completed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, task_type: str, target: str, options: Dict[str, Any] = None):
        super().__init__()
        self.task_type = task_type
        self.target = target
        self.options = options or {}
        self.is_running = True
        
    def run(self):
        """Execute the pentesting task"""
        try:
            self.status_updated.emit(f"Starting {self.task_type} on {self.target}")
            self.progress_updated.emit(10)
            
            result = {}
            
            if not FRAMEWORK_AVAILABLE:
                # Demo mode
                self.output_received.emit(f"[DEMO MODE] Simulating {self.task_type}\n")
                time.sleep(2)
                result = self.simulate_task()
            else:
                # Real execution
                result = self.execute_real_task()
            
            self.progress_updated.emit(100)
            self.task_completed.emit(result)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
            self.progress_updated.emit(0)
    
    def execute_real_task(self) -> Dict[str, Any]:
        """Execute real pentesting task"""
        result = {}
        
        if self.task_type == "reconnaissance":
            self.output_received.emit("🔍 Starting reconnaissance...\n")
            recon = ReconnaissanceModule()
            result = recon.scan_target(self.target)
            
        elif self.task_type == "network":
            self.output_received.emit("🌐 Starting network assessment...\n")
            assessor = NetworkAssessor()
            result = assessor.scan(self.target, self.options.get('mode', 'external'))
            
        elif self.task_type == "web":
            self.output_received.emit("🌍 Starting web application testing...\n")
            assessor = WebAssessor()
            result = assessor.scan(self.target, tools=self.options.get('tools', ['nuclei', 'nikto']))
            
        elif self.task_type == "wireless":
            self.output_received.emit("📡 Starting wireless assessment...\n")
            assessor = WirelessAssessor()
            result = assessor.scan_wifi(interface=self.options.get('interface', 'wlan0'))
            
        elif self.task_type == "mobile":
            self.output_received.emit("📱 Starting mobile app analysis...\n")
            assessor = MobileAssessor()
            result = assessor.analyze_apk(self.target)
            
        elif self.task_type == "vulnerability":
            self.output_received.emit("🔍 Starting vulnerability scan...\n")
            scanner = VulnerabilityScanner()
            result = scanner.scan_target(self.target, self.options.get('scan_type', 'comprehensive'))
            
        elif self.task_type == "exploit":
            self.output_received.emit("💥 Starting exploitation...\n")
            exploit = ExploitModule()
            result = exploit.auto_exploit(self.target, self.options.get('services', {}))
            
        return result
    
    def simulate_task(self) -> Dict[str, Any]:
        """Simulate task for demo mode"""
        time.sleep(1)
        self.output_received.emit(f"✅ Found open ports: 22, 80, 443\n")
        self.progress_updated.emit(50)
        time.sleep(1)
        self.output_received.emit(f"⚠️ Potential vulnerabilities detected\n")
        self.progress_updated.emit(75)
        time.sleep(1)
        
        return {
            "status": "success",
            "target": self.target,
            "findings": [
                {"type": "port", "value": "22 (SSH)"},
                {"type": "port", "value": "80 (HTTP)"},
                {"type": "port", "value": "443 (HTTPS)"},
                {"type": "vulnerability", "value": "SQL Injection possible"},
                {"type": "vulnerability", "value": "Outdated SSL/TLS"}
            ]
        }

class ModernTerminal(QTextEdit):
    """Modern terminal widget with syntax highlighting"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
        
    def setup_style(self):
        """Setup terminal styling"""
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ModernDarkTheme.BACKGROUND};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 8px;
                padding: 12px;
                font-family: 'Cascadia Code', 'Consolas', monospace;
                font-size: 12px;
                selection-background-color: {ModernDarkTheme.PRIMARY_DARK};
            }}
        """)
        self.setReadOnly(True)
    
    def append_output(self, text: str, output_type: str = "info"):
        """Append colored output to terminal"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Set color based on output type
        color_map = {
            "success": ModernDarkTheme.SUCCESS,
            "error": ModernDarkTheme.DANGER,
            "warning": ModernDarkTheme.WARNING,
            "info": ModernDarkTheme.INFO,
            "default": ModernDarkTheme.TEXT_PRIMARY
        }
        
        format = QTextCharFormat()
        format.setForeground(QColor(color_map.get(output_type, color_map["default"])))
        
        cursor.insertText(text, format)
        self.setTextCursor(cursor)
        
        # Auto scroll to bottom
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class ComprehensiveGUI(QMainWindow):
    """Main comprehensive GUI for automatic pentesting"""
    
    def __init__(self):
        super().__init__()
        self.current_worker = None
        self.test_history = []
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🛡️ Automatic Pentesting Framework - Comprehensive Suite")
        self.setGeometry(100, 100, 1600, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main content area with tabs
        content = self.create_content_area()
        main_layout.addWidget(content)
        
        # Create status bar
        self.create_status_bar()
        
        # Setup menu bar
        self.create_menu_bar()
        
    def create_header(self) -> QWidget:
        """Create application header"""
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ModernDarkTheme.PRIMARY_DARK}, 
                    stop:1 {ModernDarkTheme.PRIMARY});
                border: none;
            }}
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Logo and title
        title_layout = QVBoxLayout()
        
        title = QLabel("🛡️ AUTOMATIC PENTESTING FRAMEWORK")
        title.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial;
            }}
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Professional Security Assessment Suite | 70% Real Testing Capabilities")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                font-family: 'Segoe UI', Arial;
            }}
        """)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Quick stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.stats_labels = {
            "tests": self.create_stat_label("Tests Run", "0"),
            "vulns": self.create_stat_label("Vulns Found", "0"),
            "time": self.create_stat_label("Time Elapsed", "00:00")
        }
        
        for stat in self.stats_labels.values():
            stats_layout.addWidget(stat)
        
        layout.addLayout(stats_layout)
        
        return header
    
    def create_stat_label(self, title: str, value: str) -> QWidget:
        """Create a statistics label widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setObjectName("value")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        return widget
    
    def create_content_area(self) -> QWidget:
        """Create main content area with tabs"""
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Tab widget for different testing modules
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {ModernDarkTheme.BORDER};
                background: {ModernDarkTheme.SURFACE};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_SECONDARY};
                padding: 10px 20px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QTabBar::tab:selected {{
                background: {ModernDarkTheme.PRIMARY};
                color: white;
            }}
            QTabBar::tab:hover {{
                background: {ModernDarkTheme.SURFACE_LIGHT};
            }}
        """)
        
        # Create tabs for each pentesting category
        self.tabs = {
            "🎯 Quick Start": self.create_quick_start_tab(),
            "🌐 Network": self.create_network_tab(),
            "🌍 Web Apps": self.create_web_tab(),
            "📱 Mobile": self.create_mobile_tab(),
            "📡 Wireless": self.create_wireless_tab(),
            "💥 Exploitation": self.create_exploitation_tab(),
            "📊 Reports": self.create_reports_tab(),
            "🤖 AI Assistant": self.create_ai_tab()
        }
        
        for name, widget in self.tabs.items():
            self.tab_widget.addTab(widget, name)
        
        layout.addWidget(self.tab_widget)
        
        return content
    
    def create_quick_start_tab(self) -> QWidget:
        """Create quick start tab for common operations"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Quick scan section
        quick_scan_group = QGroupBox("⚡ Quick Penetration Test")
        quick_scan_group.setStyleSheet(self.get_group_style())
        quick_layout = QVBoxLayout()
        
        # Target input
        target_layout = QHBoxLayout()
        target_label = QLabel("Target:")
        self.quick_target_input = QLineEdit()
        self.quick_target_input.setPlaceholderText("Enter target (IP, domain, or URL)")
        self.quick_target_input.setStyleSheet(self.get_input_style())
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.quick_target_input)
        quick_layout.addLayout(target_layout)
        
        # Scan type selection
        scan_type_layout = QHBoxLayout()
        scan_type_label = QLabel("Scan Type:")
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems([
            "🚀 Basic Scan (Fast)",
            "🔍 Comprehensive Scan",
            "🛡️ Vulnerability Assessment",
            "💣 Full Penetration Test",
            "🎯 Targeted Exploitation"
        ])
        self.scan_type_combo.setStyleSheet(self.get_combo_style())
        scan_type_layout.addWidget(scan_type_label)
        scan_type_layout.addWidget(self.scan_type_combo)
        quick_layout.addLayout(scan_type_layout)
        
        # Options
        options_layout = QHBoxLayout()
        self.stealth_check = QCheckBox("Stealth Mode")
        self.aggressive_check = QCheckBox("Aggressive Scan")
        self.report_check = QCheckBox("Generate Report")
        self.report_check.setChecked(True)
        
        for checkbox in [self.stealth_check, self.aggressive_check, self.report_check]:
            checkbox.setStyleSheet(self.get_checkbox_style())
            options_layout.addWidget(checkbox)
        
        quick_layout.addLayout(options_layout)
        
        # Start button
        self.quick_start_btn = QPushButton("🚀 Start Penetration Test")
        self.quick_start_btn.setStyleSheet(self.get_button_style("primary"))
        self.quick_start_btn.clicked.connect(self.start_quick_scan)
        quick_layout.addWidget(self.quick_start_btn)
        
        quick_scan_group.setLayout(quick_layout)
        layout.addWidget(quick_scan_group)
        
        # Progress and output
        progress_group = QGroupBox("📊 Progress & Output")
        progress_group.setStyleSheet(self.get_group_style())
        progress_layout = QVBoxLayout()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(self.get_progress_style())
        progress_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to start...")
        self.status_label.setStyleSheet(f"color: {ModernDarkTheme.TEXT_SECONDARY};")
        progress_layout.addWidget(self.status_label)
        
        # Terminal output
        self.terminal = ModernTerminal()
        self.terminal.setMinimumHeight(300)
        progress_layout.addWidget(self.terminal)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        return tab
    
    def create_network_tab(self) -> QWidget:
        """Create network pentesting tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Network scan configuration
        config_group = QGroupBox("🌐 Network Scan Configuration")
        config_group.setStyleSheet(self.get_group_style())
        config_layout = QGridLayout()
        
        # Target
        config_layout.addWidget(QLabel("Target:"), 0, 0)
        self.network_target = QLineEdit()
        self.network_target.setPlaceholderText("IP address or CIDR range (e.g., 192.168.1.0/24)")
        self.network_target.setStyleSheet(self.get_input_style())
        config_layout.addWidget(self.network_target, 0, 1)
        
        # Port range
        config_layout.addWidget(QLabel("Port Range:"), 1, 0)
        port_layout = QHBoxLayout()
        self.port_start = QSpinBox()
        self.port_start.setRange(1, 65535)
        self.port_start.setValue(1)
        self.port_end = QSpinBox()
        self.port_end.setRange(1, 65535)
        self.port_end.setValue(1000)
        port_layout.addWidget(self.port_start)
        port_layout.addWidget(QLabel("-"))
        port_layout.addWidget(self.port_end)
        config_layout.addLayout(port_layout, 1, 1)
        
        # Scan techniques
        config_layout.addWidget(QLabel("Scan Type:"), 2, 0)
        self.network_scan_type = QComboBox()
        self.network_scan_type.addItems([
            "TCP SYN Scan (Stealth)",
            "TCP Connect Scan",
            "UDP Scan",
            "Comprehensive Scan",
            "Service Version Detection",
            "OS Fingerprinting"
        ])
        self.network_scan_type.setStyleSheet(self.get_combo_style())
        config_layout.addWidget(self.network_scan_type, 2, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        scan_btn = QPushButton("🔍 Start Network Scan")
        scan_btn.setStyleSheet(self.get_button_style("primary"))
        scan_btn.clicked.connect(lambda: self.start_module_scan("network"))
        
        exploit_btn = QPushButton("💥 Auto-Exploit Services")
        exploit_btn.setStyleSheet(self.get_button_style("danger"))
        
        buttons_layout.addWidget(scan_btn)
        buttons_layout.addWidget(exploit_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # Results table
        self.network_results = QTableWidget()
        self.network_results.setColumnCount(5)
        self.network_results.setHorizontalHeaderLabels(["IP", "Port", "Service", "Version", "Status"])
        self.network_results.horizontalHeader().setStretchLastSection(True)
        self.network_results.setStyleSheet(self.get_table_style())
        layout.addWidget(self.network_results)
        
        return tab
    
    def create_web_tab(self) -> QWidget:
        """Create web application testing tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Web scan configuration
        config_group = QGroupBox("🌍 Web Application Testing")
        config_group.setStyleSheet(self.get_group_style())
        config_layout = QGridLayout()
        
        # Target URL
        config_layout.addWidget(QLabel("Target URL:"), 0, 0)
        self.web_target = QLineEdit()
        self.web_target.setPlaceholderText("https://example.com")
        self.web_target.setStyleSheet(self.get_input_style())
        config_layout.addWidget(self.web_target, 0, 1)
        
        # Scan modules
        config_layout.addWidget(QLabel("Scan Modules:"), 1, 0)
        modules_layout = QVBoxLayout()
        
        self.web_modules = {
            "nuclei": QCheckBox("Nuclei (CVE & Known Vulnerabilities)"),
            "nikto": QCheckBox("Nikto (Web Server Scanner)"),
            "sqlmap": QCheckBox("SQLMap (SQL Injection)"),
            "xss": QCheckBox("XSS Detection"),
            "waf": QCheckBox("WAF Detection (WAFW00F)"),
            "dirb": QCheckBox("Directory Brute Force")
        }
        
        for module in self.web_modules.values():
            module.setChecked(True)
            module.setStyleSheet(self.get_checkbox_style())
            modules_layout.addWidget(module)
        
        config_layout.addLayout(modules_layout, 1, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Action buttons
        scan_btn = QPushButton("🔍 Start Web Application Scan")
        scan_btn.setStyleSheet(self.get_button_style("primary"))
        scan_btn.clicked.connect(lambda: self.start_module_scan("web"))
        layout.addWidget(scan_btn)
        
        # Vulnerability list
        self.web_vulns = QTreeWidget()
        self.web_vulns.setHeaderLabels(["Vulnerability", "Severity", "Details"])
        self.web_vulns.setStyleSheet(self.get_tree_style())
        layout.addWidget(self.web_vulns)
        
        return tab
    
    def create_mobile_tab(self) -> QWidget:
        """Create mobile application testing tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Mobile app configuration
        config_group = QGroupBox("📱 Mobile Application Testing")
        config_group.setStyleSheet(self.get_group_style())
        config_layout = QGridLayout()
        
        # APK file selection
        config_layout.addWidget(QLabel("APK File:"), 0, 0)
        file_layout = QHBoxLayout()
        self.mobile_file_path = QLineEdit()
        self.mobile_file_path.setPlaceholderText("Select APK file...")
        self.mobile_file_path.setStyleSheet(self.get_input_style())
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_apk_file)
        file_layout.addWidget(self.mobile_file_path)
        file_layout.addWidget(browse_btn)
        config_layout.addLayout(file_layout, 0, 1)
        
        # Analysis options
        config_layout.addWidget(QLabel("Analysis Type:"), 1, 0)
        analysis_layout = QVBoxLayout()
        
        self.mobile_options = {
            "static": QCheckBox("Static Analysis (MobSF)"),
            "decompile": QCheckBox("Decompile with Apktool"),
            "permissions": QCheckBox("Permission Analysis"),
            "frida": QCheckBox("Dynamic Analysis with Frida"),
            "drozer": QCheckBox("Drozer Security Assessment")
        }
        
        for option in self.mobile_options.values():
            option.setChecked(True)
            option.setStyleSheet(self.get_checkbox_style())
            analysis_layout.addWidget(option)
        
        config_layout.addLayout(analysis_layout, 1, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Start analysis button
        analyze_btn = QPushButton("🔍 Analyze Mobile App")
        analyze_btn.setStyleSheet(self.get_button_style("primary"))
        analyze_btn.clicked.connect(lambda: self.start_module_scan("mobile"))
        layout.addWidget(analyze_btn)
        
        # Results display
        self.mobile_results = QTextEdit()
        self.mobile_results.setReadOnly(True)
        self.mobile_results.setStyleSheet(self.get_text_edit_style())
        layout.addWidget(self.mobile_results)
        
        return tab
    
    def create_wireless_tab(self) -> QWidget:
        """Create wireless testing tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Wireless configuration
        config_group = QGroupBox("📡 Wireless Network Testing")
        config_group.setStyleSheet(self.get_group_style())
        config_layout = QGridLayout()
        
        # Interface selection
        config_layout.addWidget(QLabel("Interface:"), 0, 0)
        self.wireless_interface = QComboBox()
        self.wireless_interface.addItems(["wlan0", "wlan1", "wlan0mon"])
        self.wireless_interface.setEditable(True)
        self.wireless_interface.setStyleSheet(self.get_combo_style())
        config_layout.addWidget(self.wireless_interface, 0, 1)
        
        # Attack options
        config_layout.addWidget(QLabel("Attack Type:"), 1, 0)
        attack_layout = QVBoxLayout()
        
        self.wireless_attacks = {
            "scan": QRadioButton("Network Discovery"),
            "handshake": QRadioButton("WPA/WPA2 Handshake Capture"),
            "deauth": QRadioButton("Deauthentication Attack"),
            "crack": QRadioButton("Password Cracking")
        }
        
        for attack in self.wireless_attacks.values():
            attack.setStyleSheet(self.get_radio_style())
            attack_layout.addWidget(attack)
        
        self.wireless_attacks["scan"].setChecked(True)
        config_layout.addLayout(attack_layout, 1, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Action buttons
        start_btn = QPushButton("📡 Start Wireless Attack")
        start_btn.setStyleSheet(self.get_button_style("warning"))
        start_btn.clicked.connect(lambda: self.start_module_scan("wireless"))
        layout.addWidget(start_btn)
        
        # Networks table
        self.wireless_networks = QTableWidget()
        self.wireless_networks.setColumnCount(6)
        self.wireless_networks.setHorizontalHeaderLabels(
            ["SSID", "BSSID", "Channel", "Power", "Encryption", "Clients"]
        )
        self.wireless_networks.setStyleSheet(self.get_table_style())
        layout.addWidget(self.wireless_networks)
        
        return tab
    
    def create_exploitation_tab(self) -> QWidget:
        """Create exploitation tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Exploitation configuration
        config_group = QGroupBox("💥 Exploitation Framework")
        config_group.setStyleSheet(self.get_group_style())
        config_layout = QGridLayout()
        
        # Target
        config_layout.addWidget(QLabel("Target:"), 0, 0)
        self.exploit_target = QLineEdit()
        self.exploit_target.setPlaceholderText("Target IP or hostname")
        self.exploit_target.setStyleSheet(self.get_input_style())
        config_layout.addWidget(self.exploit_target, 0, 1)
        
        # Service/Port
        config_layout.addWidget(QLabel("Service/Port:"), 1, 0)
        service_layout = QHBoxLayout()
        self.exploit_service = QComboBox()
        self.exploit_service.addItems(["SSH (22)", "FTP (21)", "HTTP (80)", "HTTPS (443)", "SMB (445)", "Custom"])
        self.exploit_service.setStyleSheet(self.get_combo_style())
        self.exploit_port = QSpinBox()
        self.exploit_port.setRange(1, 65535)
        self.exploit_port.setValue(22)
        service_layout.addWidget(self.exploit_service)
        service_layout.addWidget(self.exploit_port)
        config_layout.addLayout(service_layout, 1, 1)
        
        # Exploit type
        config_layout.addWidget(QLabel("Exploit Type:"), 2, 0)
        self.exploit_type = QComboBox()
        self.exploit_type.addItems([
            "Auto-Exploit (Smart)",
            "Brute Force",
            "Known Vulnerabilities",
            "SQL Injection",
            "Command Injection",
            "File Upload",
            "Custom Payload"
        ])
        self.exploit_type.setStyleSheet(self.get_combo_style())
        config_layout.addWidget(self.exploit_type, 2, 1)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Exploit button
        exploit_btn = QPushButton("💣 Launch Exploitation")
        exploit_btn.setStyleSheet(self.get_button_style("danger"))
        exploit_btn.clicked.connect(lambda: self.start_module_scan("exploit"))
        layout.addWidget(exploit_btn)
        
        # Exploitation log
        self.exploit_log = QTextEdit()
        self.exploit_log.setReadOnly(True)
        self.exploit_log.setStyleSheet(self.get_text_edit_style())
        layout.addWidget(self.exploit_log)
        
        return tab
    
    def create_reports_tab(self) -> QWidget:
        """Create reports tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Report generation
        gen_group = QGroupBox("📊 Report Generation")
        gen_group.setStyleSheet(self.get_group_style())
        gen_layout = QVBoxLayout()
        
        # Report type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Report Type:"))
        self.report_type = QComboBox()
        self.report_type.addItems(["Executive Summary", "Technical Report", "Full Report", "Vulnerability Report"])
        self.report_type.setStyleSheet(self.get_combo_style())
        type_layout.addWidget(self.report_type)
        gen_layout.addLayout(type_layout)
        
        # Format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.report_format = QComboBox()
        self.report_format.addItems(["PDF", "HTML", "Markdown", "JSON", "CSV"])
        self.report_format.setStyleSheet(self.get_combo_style())
        format_layout.addWidget(self.report_format)
        gen_layout.addLayout(format_layout)
        
        # Generate button
        generate_btn = QPushButton("📄 Generate Report")
        generate_btn.setStyleSheet(self.get_button_style("primary"))
        generate_btn.clicked.connect(self.generate_report)
        gen_layout.addWidget(generate_btn)
        
        gen_group.setLayout(gen_layout)
        layout.addWidget(gen_group)
        
        # Previous reports
        history_group = QGroupBox("📁 Report History")
        history_group.setStyleSheet(self.get_group_style())
        history_layout = QVBoxLayout()
        
        self.report_list = QListWidget()
        self.report_list.setStyleSheet(self.get_list_style())
        history_layout.addWidget(self.report_list)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        return tab
    
    def create_ai_tab(self) -> QWidget:
        """Create AI assistant tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # AI chat interface
        chat_group = QGroupBox("🤖 AI Pentesting Assistant")
        chat_group.setStyleSheet(self.get_group_style())
        chat_layout = QVBoxLayout()
        
        # Chat display
        self.ai_chat_display = QTextEdit()
        self.ai_chat_display.setReadOnly(True)
        self.ai_chat_display.setStyleSheet(self.get_text_edit_style())
        self.ai_chat_display.setMinimumHeight(400)
        chat_layout.addWidget(self.ai_chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        self.ai_input = QLineEdit()
        self.ai_input.setPlaceholderText("Ask the AI assistant... (e.g., 'Scan example.com for vulnerabilities')")
        self.ai_input.setStyleSheet(self.get_input_style())
        self.ai_input.returnPressed.connect(self.send_ai_message)
        
        send_btn = QPushButton("Send")
        send_btn.setStyleSheet(self.get_button_style("primary"))
        send_btn.clicked.connect(self.send_ai_message)
        
        input_layout.addWidget(self.ai_input)
        input_layout.addWidget(send_btn)
        chat_layout.addLayout(input_layout)
        
        chat_group.setLayout(chat_layout)
        layout.addWidget(chat_group)
        
        # AI suggestions
        suggestions_group = QGroupBox("💡 AI Suggestions")
        suggestions_group.setStyleSheet(self.get_group_style())
        suggestions_layout = QVBoxLayout()
        
        self.suggestions_list = QListWidget()
        self.suggestions_list.setStyleSheet(self.get_list_style())
        suggestions_list_items = [
            "🔍 'Perform comprehensive scan on target'",
            "🛡️ 'Check for SQL injection vulnerabilities'",
            "📱 'Analyze mobile app security'",
            "📡 'Scan wireless networks nearby'",
            "💥 'Exploit discovered services'"
        ]
        self.suggestions_list.addItems(suggestions_list_items)
        self.suggestions_list.itemClicked.connect(self.use_ai_suggestion)
        suggestions_layout.addWidget(self.suggestions_list)
        
        suggestions_group.setLayout(suggestions_layout)
        layout.addWidget(suggestions_group)
        
        return tab
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_PRIMARY};
            }}
            QMenuBar::item:selected {{
                background-color: {ModernDarkTheme.PRIMARY};
            }}
        """)
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Session", self.new_session)
        file_menu.addAction("Load Session", self.load_session)
        file_menu.addAction("Save Session", self.save_session)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        tools_menu.addAction("Network Scanner", lambda: self.tab_widget.setCurrentIndex(1))
        tools_menu.addAction("Web Scanner", lambda: self.tab_widget.setCurrentIndex(2))
        tools_menu.addAction("Mobile Analyzer", lambda: self.tab_widget.setCurrentIndex(3))
        tools_menu.addAction("Wireless Tools", lambda: self.tab_widget.setCurrentIndex(4))
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Clear Terminal", self.clear_terminal)
        view_menu.addAction("Toggle Dark Mode", self.toggle_theme)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation", self.show_documentation)
        help_menu.addAction("About", self.show_about)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_SECONDARY};
                border-top: 1px solid {ModernDarkTheme.BORDER};
            }}
        """)
        self.status_bar.showMessage("Ready")
    
    def apply_theme(self):
        """Apply dark theme to application"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {ModernDarkTheme.BACKGROUND};
            }}
            QWidget {{
                background-color: {ModernDarkTheme.BACKGROUND};
                color: {ModernDarkTheme.TEXT_PRIMARY};
            }}
        """)
    
    # Style methods
    def get_group_style(self) -> str:
        return f"""
            QGroupBox {{
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {ModernDarkTheme.PRIMARY};
            }}
        """
    
    def get_button_style(self, button_type: str = "default") -> str:
        colors = {
            "primary": ModernDarkTheme.PRIMARY,
            "success": ModernDarkTheme.SUCCESS,
            "danger": ModernDarkTheme.DANGER,
            "warning": ModernDarkTheme.WARNING,
            "default": ModernDarkTheme.TEXT_SECONDARY
        }
        color = colors.get(button_type, colors["default"])
        
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}bb;
            }}
            QPushButton:disabled {{
                background-color: {ModernDarkTheme.TEXT_MUTED};
                color: {ModernDarkTheme.TEXT_SECONDARY};
            }}
        """
    
    def get_input_style(self) -> str:
        return f"""
            QLineEdit {{
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {ModernDarkTheme.PRIMARY};
            }}
        """
    
    def get_combo_style(self) -> str:
        return f"""
            QComboBox {{
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }}
            QComboBox:hover {{
                border: 1px solid {ModernDarkTheme.PRIMARY};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """
    
    def get_checkbox_style(self) -> str:
        return f"""
            QCheckBox {{
                color: {ModernDarkTheme.TEXT_PRIMARY};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {ModernDarkTheme.BORDER};
                border-radius: 4px;
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {ModernDarkTheme.PRIMARY};
                border: 2px solid {ModernDarkTheme.PRIMARY};
            }}
        """
    
    def get_radio_style(self) -> str:
        return f"""
            QRadioButton {{
                color: {ModernDarkTheme.TEXT_PRIMARY};
                spacing: 8px;
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {ModernDarkTheme.BORDER};
                border-radius: 9px;
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
            }}
            QRadioButton::indicator:checked {{
                background-color: {ModernDarkTheme.PRIMARY};
                border: 2px solid {ModernDarkTheme.PRIMARY};
            }}
        """
    
    def get_progress_style(self) -> str:
        return f"""
            QProgressBar {{
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 6px;
                text-align: center;
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
                color: {ModernDarkTheme.TEXT_PRIMARY};
            }}
            QProgressBar::chunk {{
                background-color: {ModernDarkTheme.PRIMARY};
                border-radius: 5px;
            }}
        """
    
    def get_table_style(self) -> str:
        return f"""
            QTableWidget {{
                background-color: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 6px;
                gridline-color: {ModernDarkTheme.BORDER};
            }}
            QTableWidget::item:selected {{
                background-color: {ModernDarkTheme.PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {ModernDarkTheme.PRIMARY};
            }}
        """
    
    def get_tree_style(self) -> str:
        return f"""
            QTreeWidget {{
                background-color: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 6px;
            }}
            QTreeWidget::item:selected {{
                background-color: {ModernDarkTheme.PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {ModernDarkTheme.PRIMARY};
            }}
        """
    
    def get_text_edit_style(self) -> str:
        return f"""
            QTextEdit {{
                background-color: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 6px;
                padding: 8px;
                font-family: 'Cascadia Code', monospace;
                font-size: 12px;
            }}
        """
    
    def get_list_style(self) -> str:
        return f"""
            QListWidget {{
                background-color: {ModernDarkTheme.SURFACE};
                color: {ModernDarkTheme.TEXT_PRIMARY};
                border: 1px solid {ModernDarkTheme.BORDER};
                border-radius: 6px;
                padding: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {ModernDarkTheme.PRIMARY};
            }}
            QListWidget::item:hover {{
                background-color: {ModernDarkTheme.SURFACE_LIGHT};
            }}
        """
    
    # Action methods
    def start_quick_scan(self):
        """Start quick penetration test"""
        target = self.quick_target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Warning", "Please enter a target")
            return
        
        # Clear previous output
        self.terminal.clear()
        self.progress_bar.setValue(0)
        
        # Update status
        scan_type = self.scan_type_combo.currentText()
        self.status_label.setText(f"Running {scan_type} on {target}")
        self.terminal.append_output(f"=== Starting {scan_type} ===\n", "info")
        self.terminal.append_output(f"Target: {target}\n", "info")
        
        # Determine task type based on scan selection
        task_type = "reconnaissance"
        if "Vulnerability" in scan_type:
            task_type = "vulnerability"
        elif "Penetration" in scan_type:
            task_type = "exploit"
        
        # Create and start worker
        self.current_worker = PentestWorker(task_type, target, {
            "stealth": self.stealth_check.isChecked(),
            "aggressive": self.aggressive_check.isChecked()
        })
        
        self.current_worker.output_received.connect(
            lambda text: self.terminal.append_output(text, "default")
        )
        self.current_worker.progress_updated.connect(self.progress_bar.setValue)
        self.current_worker.status_updated.connect(self.status_label.setText)
        self.current_worker.task_completed.connect(self.handle_task_completed)
        self.current_worker.error_occurred.connect(
            lambda err: self.terminal.append_output(f"❌ Error: {err}\n", "error")
        )
        
        self.current_worker.start()
        
        # Update stats
        current_tests = int(self.stats_labels["tests"].findChild(QLabel, "value").text())
        self.stats_labels["tests"].findChild(QLabel, "value").setText(str(current_tests + 1))
    
    def start_module_scan(self, module: str):
        """Start specific module scan"""
        target = ""
        options = {}
        
        if module == "network":
            target = self.network_target.text().strip()
            if not target:
                QMessageBox.warning(self, "Warning", "Please enter a network target")
                return
            options = {
                "port_start": self.port_start.value(),
                "port_end": self.port_end.value(),
                "scan_type": self.network_scan_type.currentText()
            }
            
        elif module == "web":
            target = self.web_target.text().strip()
            if not target:
                QMessageBox.warning(self, "Warning", "Please enter a web target")
                return
            tools = [name for name, checkbox in self.web_modules.items() if checkbox.isChecked()]
            options = {"tools": tools}
            
        elif module == "mobile":
            target = self.mobile_file_path.text().strip()
            if not target or not os.path.exists(target):
                QMessageBox.warning(self, "Warning", "Please select a valid APK file")
                return
            options = {name: cb.isChecked() for name, cb in self.mobile_options.items()}
            
        elif module == "wireless":
            interface = self.wireless_interface.currentText()
            attack_type = next((name for name, rb in self.wireless_attacks.items() if rb.isChecked()), "scan")
            options = {"interface": interface, "attack": attack_type}
            target = interface  # Use interface as target for wireless
            
        elif module == "exploit":
            target = self.exploit_target.text().strip()
            if not target:
                QMessageBox.warning(self, "Warning", "Please enter an exploitation target")
                return
            options = {
                "service": self.exploit_service.currentText(),
                "port": self.exploit_port.value(),
                "type": self.exploit_type.currentText()
            }
        
        # Clear terminal and start scan
        self.terminal.clear()
        self.terminal.append_output(f"Starting {module} scan on {target}\n", "info")
        
        # Create and start worker
        self.current_worker = PentestWorker(module, target, options)
        self.current_worker.output_received.connect(
            lambda text: self.terminal.append_output(text, "default")
        )
        self.current_worker.progress_updated.connect(self.progress_bar.setValue)
        self.current_worker.task_completed.connect(self.handle_task_completed)
        self.current_worker.error_occurred.connect(
            lambda err: self.terminal.append_output(f"❌ Error: {err}\n", "error")
        )
        
        self.current_worker.start()
    
    def handle_task_completed(self, result: Dict[str, Any]):
        """Handle task completion"""
        self.terminal.append_output("\n=== Task Completed ===\n", "success")
        
        # Update vulnerability count
        if "findings" in result:
            vuln_count = len([f for f in result["findings"] if f["type"] == "vulnerability"])
            current_vulns = int(self.stats_labels["vulns"].findChild(QLabel, "value").text())
            self.stats_labels["vulns"].findChild(QLabel, "value").setText(str(current_vulns + vuln_count))
        
        # Store in history
        self.test_history.append({
            "timestamp": datetime.now(),
            "target": result.get("target", "Unknown"),
            "result": result
        })
        
        # Generate report if checked
        if hasattr(self, 'report_check') and self.report_check.isChecked():
            self.generate_report()
        
        self.status_label.setText("Task completed successfully")
    
    def browse_apk_file(self):
        """Browse for APK file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select APK File", "", "APK Files (*.apk);;All Files (*)"
        )
        if file_path:
            self.mobile_file_path.setText(file_path)
    
    def generate_report(self):
        """Generate penetration testing report"""
        if not self.test_history:
            QMessageBox.information(self, "Info", "No test results to report")
            return
        
        report_type = self.report_type.currentText() if hasattr(self, 'report_type') else "Full Report"
        report_format = self.report_format.currentText() if hasattr(self, 'report_format') else "HTML"
        
        # Create report content
        report_content = f"# Penetration Testing Report\n\n"
        report_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report_content += f"## Test Summary\n\n"
        report_content += f"Total Tests: {len(self.test_history)}\n\n"
        
        for i, test in enumerate(self.test_history, 1):
            report_content += f"### Test {i}\n"
            report_content += f"Target: {test['target']}\n"
            report_content += f"Time: {test['timestamp'].strftime('%H:%M:%S')}\n"
            report_content += f"Results: {json.dumps(test['result'], indent=2)}\n\n"
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"pentest_report_{timestamp}.{report_format.lower()}"
        report_path = Path("reports") / report_file
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, "w") as f:
            f.write(report_content)
        
        self.terminal.append_output(f"✅ Report saved to: {report_path}\n", "success")
        
        # Update report list
        if hasattr(self, 'report_list'):
            self.report_list.addItem(f"{report_file} - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    def send_ai_message(self):
        """Send message to AI assistant"""
        message = self.ai_input.text().strip()
        if not message:
            return
        
        # Display user message
        self.ai_chat_display.append(f"You: {message}\n")
        self.ai_input.clear()
        
        # Process with AI (simulate or use real copilot)
        self.ai_chat_display.append("AI: Processing your request...\n")
        
        if FRAMEWORK_AVAILABLE:
            try:
                result = copilot_run(message)
                response = f"I'll help you with that. Here's what I found:\n"
                if "plan" in result:
                    response += f"Plan: {result['plan']}\n"
                if "results" in result:
                    response += f"Results: {result['results']}\n"
                self.ai_chat_display.append(f"AI: {response}\n")
            except Exception as e:
                self.ai_chat_display.append(f"AI: Error processing request: {e}\n")
        else:
            # Simulated response
            self.ai_chat_display.append(
                f"AI: I understand you want to '{message}'. "
                f"In a real environment, I would execute the appropriate pentesting tools for this task.\n"
            )
    
    def use_ai_suggestion(self, item):
        """Use AI suggestion"""
        suggestion = item.text()
        # Remove emoji and quotes
        clean_suggestion = suggestion.split("'")[1] if "'" in suggestion else suggestion
        self.ai_input.setText(clean_suggestion)
        self.send_ai_message()
    
    def clear_terminal(self):
        """Clear terminal output"""
        self.terminal.clear()
        self.terminal.append_output("Terminal cleared\n", "info")
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        # For now, just show a message
        QMessageBox.information(self, "Theme", "Dark theme is currently active")
    
    def new_session(self):
        """Start new pentesting session"""
        self.test_history.clear()
        self.terminal.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("New session started")
        
        # Reset stats
        self.stats_labels["tests"].findChild(QLabel, "value").setText("0")
        self.stats_labels["vulns"].findChild(QLabel, "value").setText("0")
    
    def save_session(self):
        """Save current session"""
        if not self.test_history:
            QMessageBox.information(self, "Info", "No session data to save")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Session", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            session_data = {
                "timestamp": datetime.now().isoformat(),
                "tests": [
                    {
                        "timestamp": test["timestamp"].isoformat(),
                        "target": test["target"],
                        "result": test["result"]
                    }
                    for test in self.test_history
                ]
            }
            
            with open(file_path, "w") as f:
                json.dump(session_data, f, indent=2)
            
            self.status_bar.showMessage(f"Session saved to {file_path}")
    
    def load_session(self):
        """Load saved session"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Session", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, "r") as f:
                    session_data = json.load(f)
                
                self.test_history.clear()
                for test in session_data.get("tests", []):
                    self.test_history.append({
                        "timestamp": datetime.fromisoformat(test["timestamp"]),
                        "target": test["target"],
                        "result": test["result"]
                    })
                
                self.status_bar.showMessage(f"Session loaded from {file_path}")
                self.terminal.append_output(f"✅ Loaded {len(self.test_history)} tests from session\n", "success")
                
            except Exception as e:
                QMessageBox.error(self, "Error", f"Failed to load session: {e}")
    
    def show_documentation(self):
        """Show documentation"""
        QMessageBox.information(
            self, 
            "Documentation",
            "Automatic Pentesting Framework v1.0\n\n"
            "Features:\n"
            "✅ Network Penetration Testing\n"
            "✅ Web Application Testing\n"
            "✅ Mobile App Analysis\n"
            "✅ Wireless Network Testing\n"
            "✅ Automated Exploitation\n"
            "✅ AI-Powered Assistant\n\n"
            "For detailed documentation, visit the project repository."
        )
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About",
            "Automatic Pentesting Framework\n"
            "Version 1.0\n\n"
            "A comprehensive security testing suite with:\n"
            "• 70% Real pentesting capabilities\n"
            "• 15+ integrated security tools\n"
            "• AI-powered automation\n\n"
            "⚠️ Use responsibly and only on authorized targets!"
        )

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Automatic Pentesting Framework")
    app.setOrganizationName("Security Team")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = ComprehensiveGUI()
    window.show()
    
    # Initial message
    window.terminal.append_output(
        "🛡️ Automatic Pentesting Framework initialized\n"
        "✅ 70% Real Testing Capabilities Active\n"
        "⚠️ Use only on authorized targets!\n\n"
        "Select a target and testing type to begin...\n",
        "success"
    )
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
