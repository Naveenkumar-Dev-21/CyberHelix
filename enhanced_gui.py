#!/usr/bin/env python3
"""
Enhanced AI Pentesting GUI with Terminal Integration
Real command execution with terminal output display
"""

import sys
import os
import subprocess
import threading
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QPushButton, QLabel, QLineEdit, QSplitter, QTabWidget,
    QProgressBar, QComboBox, QCheckBox, QFrame, QScrollArea, QTreeWidget,
    QTreeWidgetItem, QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QProcess
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QTextCursor, QIcon, QAction,
    QTextCharFormat, QSyntaxHighlighter, QTextDocument
)

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from ai_model import IntentClassifierModel
    from enhanced_nlp_processor import EnhancedNLPProcessor
    from copilot import copilot_run
    from config import Config
    AI_AVAILABLE = True
except ImportError as e:
    print(f"AI modules not available: {e}")
    AI_AVAILABLE = False


class TerminalHighlighter(QSyntaxHighlighter):
    """Enhanced syntax highlighter for terminal output"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        
        # Command patterns (cyan)
        cmd_format = QTextCharFormat()
        cmd_format.setForeground(QColor("#00FFFF"))
        cmd_format.setFontWeight(QFont.Weight.Bold)
        self.rules.append((r'^\$ .*$', cmd_format))
        self.rules.append((r'^❯ .*$', cmd_format))
        
        # Success patterns (green)
        success_format = QTextCharFormat()
        success_format.setForeground(QColor("#00FF00"))
        success_format.setFontWeight(QFont.Weight.Bold)
        success_patterns = [r'✅', r'SUCCESS', r'COMPLETED', r'ACTIVE', r'RUNNING', r'LISTENING']
        for pattern in success_patterns:
            self.rules.append((pattern, success_format))
        
        # Error patterns (red)
        error_format = QTextCharFormat()
        error_format.setForeground(QColor("#FF0000"))
        error_format.setFontWeight(QFont.Weight.Bold)
        error_patterns = [r'❌', r'ERROR', r'FAILED', r'CRITICAL', r'DENIED', r'REFUSED']
        for pattern in error_patterns:
            self.rules.append((pattern, error_format))
        
        # Warning patterns (yellow)
        warning_format = QTextCharFormat()
        warning_format.setForeground(QColor("#FFFF00"))
        warning_patterns = [r'⚠️', r'WARNING', r'MEDIUM', r'STOPPED', r'INACTIVE']
        for pattern in warning_patterns:
            self.rules.append((pattern, warning_format))
        
        # Info patterns (blue)
        info_format = QTextCharFormat()
        info_format.setForeground(QColor("#00BFFF"))
        info_patterns = [r'🔍', r'INFO', r'SCANNING', r'PID:', r'Port']
        for pattern in info_patterns:
            self.rules.append((pattern, info_format))
        
        # IP addresses (magenta)
        ip_format = QTextCharFormat()
        ip_format.setForeground(QColor("#FF00FF"))
        self.rules.append((r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', ip_format))
        
        # Ports (orange)
        port_format = QTextCharFormat()
        port_format.setForeground(QColor("#FFA500"))
        self.rules.append((r':\d+', port_format))
    
    def highlightBlock(self, text):
        import re
        for pattern, format_obj in self.rules:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                start, end = match.span()
                self.setFormat(start, end - start, format_obj)


class CommandExecutor(QThread):
    """Thread for executing system commands"""
    
    output_ready = pyqtSignal(str)
    command_finished = pyqtSignal(int, str, str)
    progress_update = pyqtSignal(int)
    
    def __init__(self, command, shell=True):
        super().__init__()
        self.command = command
        self.shell = shell
        self.process = None
    
    def run(self):
        """Execute command and emit output"""
        try:
            self.output_ready.emit(f"❯ {self.command}\n")
            
            self.process = subprocess.Popen(
                self.command,
                shell=self.shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output in real-time
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_ready.emit(output)
            
            # Get any remaining output
            stdout, stderr = self.process.communicate()
            if stdout:
                self.output_ready.emit(stdout)
            if stderr:
                self.output_ready.emit(f"STDERR: {stderr}")
            
            self.command_finished.emit(self.process.returncode, stdout, stderr)
            
        except Exception as e:
            self.output_ready.emit(f"❌ Error executing command: {str(e)}\n")
            self.command_finished.emit(1, "", str(e))
    
    def stop(self):
        """Stop the running process"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()


class AICommandProcessor(QThread):
    """Process natural language commands using AI"""
    
    result_ready = pyqtSignal(dict)
    status_update = pyqtSignal(str)
    
    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input
    
    def run(self):
        """Process the user input with AI"""
        try:
            if not AI_AVAILABLE:
                # Fallback: convert common requests to system commands
                self.status_update.emit("🤖 AI not available, using fallback...")
                command_map = {
                    "services": "systemctl list-units --type=service --state=running",
                    "processes": "ps aux",
                    "network": "netstat -tulpn",
                    "ports": "ss -tulpn",
                    "disk": "df -h",
                    "memory": "free -h",
                    "users": "who",
                    "system": "uname -a",
                }
                
                for keyword, cmd in command_map.items():
                    if keyword in self.user_input.lower():
                        result = {
                            "request": self.user_input,
                            "plan": [{"module": "system", "args": [cmd]}],
                            "ai_intent": keyword,
                            "confidence": 0.8,
                            "command": cmd
                        }
                        self.result_ready.emit(result)
                        return
                
                # Default fallback
                result = {
                    "request": self.user_input,
                    "plan": [{"module": "system", "args": [self.user_input]}],
                    "ai_intent": "unknown",
                    "confidence": 0.5,
                    "command": self.user_input
                }
                self.result_ready.emit(result)
                return
            
            # Use AI system
            self.status_update.emit("🧠 Processing with AI...")
            
            # Load AI model
            model = IntentClassifierModel()
            if model.load_model():
                ai_result = model.predict(self.user_input)
                self.status_update.emit(f"AI Intent: {ai_result['intent']} ({ai_result['confidence']:.2f})")
            else:
                ai_result = {"intent": "unknown", "confidence": 0.0}
            
            # Use NLP processor
            nlp = EnhancedNLPProcessor()
            nlp_result = nlp.process_request(self.user_input)
            
            # Convert to system commands
            command = self.convert_to_system_command(ai_result['intent'], nlp_result, self.user_input)
            
            result = {
                "request": self.user_input,
                "ai_intent": ai_result['intent'],
                "ai_confidence": ai_result['confidence'],
                "nlp_command": nlp_result.primary_command.value,
                "nlp_confidence": nlp_result.confidence,
                "targets": nlp_result.targets,
                "command": command,
                "plan": [{"module": "system", "args": [command]}]
            }
            
            self.result_ready.emit(result)
            
        except Exception as e:
            self.status_update.emit(f"❌ AI processing error: {str(e)}")
            # Fallback
            result = {
                "request": self.user_input,
                "command": self.user_input,
                "error": str(e)
            }
            self.result_ready.emit(result)
    
    def convert_to_system_command(self, ai_intent, nlp_result, user_input):
        """Convert AI/NLP results to system commands"""
        
        # Common system information commands
        system_commands = {
            "services": "systemctl list-units --type=service --state=running",
            "running services": "systemctl list-units --type=service --state=running",
            "processes": "ps aux | head -20",
            "running processes": "ps aux | head -20",
            "network": "netstat -tulpn | head -20",
            "open ports": "ss -tulpn",
            "listening ports": "ss -tulpn | grep LISTEN",
            "disk usage": "df -h",
            "memory usage": "free -h",
            "system info": "uname -a && lsb_release -a",
            "users": "who && last | head -10",
            "load": "uptime && top -bn1 | head -5",
        }
        
        # Check for exact matches or keywords
        user_lower = user_input.lower()
        
        for key, cmd in system_commands.items():
            if key in user_lower:
                return cmd
        
        # Network scanning commands
        if any(word in user_lower for word in ['scan', 'nmap', 'port scan']):
            if nlp_result.targets:
                target = nlp_result.targets[0]
                return f"nmap -sS -O {target}"
            else:
                return "nmap -sS localhost"
        
        # File system commands
        if any(word in user_lower for word in ['list', 'ls', 'directory']):
            return "ls -la"
        
        # Default: try to execute as shell command
        return user_input


class EnhancedPentestGUI(QMainWindow):
    """Enhanced GUI with terminal integration"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_ai()
        self.command_history = []
        self.current_executor = None
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI-Powered Pentesting Terminal")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #000000;
                color: #00ff00;
                border: 1px solid #333333;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0080ff;
            }
            QPushButton:pressed {
                background-color: #004499;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #3d3d3d;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0066cc;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready - Enter commands in natural language")
        
        # Top controls
        controls_layout = QHBoxLayout()
        
        # Input field
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command in natural language (e.g., 'show running services', 'scan localhost', 'list processes')")
        self.command_input.returnPressed.connect(self.execute_command)
        
        # Execute button
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self.execute_command)
        
        # Stop button
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_execution)
        self.stop_btn.setEnabled(False)
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_terminal)
        
        controls_layout.addWidget(QLabel("Command:"))
        controls_layout.addWidget(self.command_input)
        controls_layout.addWidget(self.execute_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Create splitter for terminal and info
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Terminal output
        terminal_widget = QWidget()
        terminal_layout = QVBoxLayout(terminal_widget)
        
        terminal_layout.addWidget(QLabel("Terminal Output:"))
        self.terminal_output = QTextEdit()
        self.terminal_output.setFont(QFont("Courier New", 12))
        self.highlighter = TerminalHighlighter(self.terminal_output.document())
        terminal_layout.addWidget(self.terminal_output)
        
        # Right side - Information tabs
        info_tabs = QTabWidget()
        
        # AI Analysis tab
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        ai_layout.addWidget(QLabel("AI Analysis:"))
        self.ai_analysis = QTextEdit()
        self.ai_analysis.setMaximumHeight(200)
        ai_layout.addWidget(self.ai_analysis)
        
        ai_layout.addWidget(QLabel("Command Translation:"))
        self.command_translation = QTextEdit()
        self.command_translation.setMaximumHeight(100)
        ai_layout.addWidget(self.command_translation)
        
        info_tabs.addTab(ai_tab, "AI Analysis")
        
        # Results tab
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        results_layout.addWidget(QLabel("Execution Results:"))
        self.results_display = QTextEdit()
        results_layout.addWidget(self.results_display)
        info_tabs.addTab(results_tab, "Results Summary")
        
        # History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        history_layout.addWidget(QLabel("Command History:"))
        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        history_layout.addWidget(self.history_list)
        info_tabs.addTab(history_tab, "History")
        
        # Add to splitter
        splitter.addWidget(terminal_widget)
        splitter.addWidget(info_tabs)
        splitter.setSizes([800, 400])
        
        main_layout.addWidget(splitter)
        
        # Add welcome message
        self.add_terminal_output("""
🤖 AI-Powered Pentesting Terminal Ready!

Examples of commands you can try:
• "show running services"
• "list all processes" 
• "check network connections"
• "scan localhost for open ports"
• "show disk usage"
• "display memory usage"
• "who is logged in"

Type your command above and press Enter or click Execute.
""")
    
    def init_ai(self):
        """Initialize AI components"""
        if AI_AVAILABLE:
            try:
                self.ai_model = IntentClassifierModel()
                self.ai_model.load_model()
                self.nlp_processor = EnhancedNLPProcessor()
                self.statusbar.showMessage("AI System Ready")
            except Exception as e:
                self.statusbar.showMessage(f"AI initialization failed: {e}")
        else:
            self.statusbar.showMessage("AI not available - using fallback mode")
    
    def execute_command(self):
        """Execute the command entered by user"""
        user_input = self.command_input.text().strip()
        if not user_input:
            return
        
        # Add to history
        self.command_history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "command": user_input,
            "status": "executing"
        })
        self.update_history_display()
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.execute_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # Process with AI
        self.ai_processor = AICommandProcessor(user_input)
        self.ai_processor.result_ready.connect(self.handle_ai_result)
        self.ai_processor.status_update.connect(self.update_status)
        self.ai_processor.start()
        
        # Clear input
        self.command_input.clear()
    
    def handle_ai_result(self, result):
        """Handle AI processing result and execute command"""
        # Update AI analysis display
        ai_info = f"""
Input: {result['request']}
AI Intent: {result.get('ai_intent', 'unknown')} (confidence: {result.get('ai_confidence', 0):.2f})
NLP Command: {result.get('nlp_command', 'unknown')}
Targets: {result.get('targets', [])}
System Command: {result['command']}
        """
        self.ai_analysis.setPlainText(ai_info)
        self.command_translation.setPlainText(result['command'])
        
        # Execute the actual system command
        if 'command' in result:
            self.current_executor = CommandExecutor(result['command'])
            self.current_executor.output_ready.connect(self.add_terminal_output)
            self.current_executor.command_finished.connect(self.handle_command_finished)
            self.current_executor.start()
        else:
            self.handle_command_finished(1, "", "No command to execute")
    
    def handle_command_finished(self, return_code, stdout, stderr):
        """Handle command execution completion"""
        # Update UI
        self.progress_bar.setVisible(False)
        self.execute_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Update history
        if self.command_history:
            self.command_history[-1]["status"] = "completed" if return_code == 0 else "failed"
            self.command_history[-1]["return_code"] = return_code
        
        self.update_history_display()
        
        # Update results
        results_text = f"""
Return Code: {return_code}
Status: {'Success' if return_code == 0 else 'Failed'}
Output Length: {len(stdout)} characters
Error Length: {len(stderr)} characters
        """
        self.results_display.setPlainText(results_text)
        
        # Update status
        status_msg = "✅ Command completed successfully" if return_code == 0 else f"❌ Command failed (code: {return_code})"
        self.statusbar.showMessage(status_msg)
        
        self.add_terminal_output(f"\n{status_msg}\n{'='*50}\n")
    
    def stop_execution(self):
        """Stop the current command execution"""
        if self.current_executor:
            self.current_executor.stop()
        self.progress_bar.setVisible(False)
        self.execute_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.add_terminal_output("\n❌ Command execution stopped by user\n")
    
    def clear_terminal(self):
        """Clear the terminal output"""
        self.terminal_output.clear()
        self.add_terminal_output("Terminal cleared.\n")
    
    def add_terminal_output(self, text):
        """Add text to terminal output"""
        self.terminal_output.append(text)
        # Auto-scroll to bottom
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_output.setTextCursor(cursor)
    
    def update_status(self, message):
        """Update status bar message"""
        self.statusbar.showMessage(message)
    
    def update_history_display(self):
        """Update the command history display"""
        history_text = ""
        for entry in self.command_history[-10:]:  # Show last 10 commands
            status_icon = "✅" if entry["status"] == "completed" else "⏳" if entry["status"] == "executing" else "❌"
            history_text += f"[{entry['timestamp']}] {status_icon} {entry['command']}\n"
        
        self.history_list.setPlainText(history_text)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("AI Pentesting Terminal")
    app.setApplicationVersion("2.0")
    
    # Set dark fusion style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = EnhancedPentestGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
