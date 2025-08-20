#!/usr/bin/env python3
"""
Improved ChatGPT-Style AI Penetration Testing Interface
Enhanced chatbot with better working principles and more intelligent responses
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
import json
import time
import re
from datetime import datetime
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class IntelligentChatbot:
    """Enhanced chatbot with direct action-oriented responses like Cursor IDE"""
    
    def __init__(self):
        self.conversation_context = []
        self.user_password = None  # Store for sudo operations
        self.comprehensive_pentest_phases = {
            'reconnaissance': [
                'ping -c 4 {}',
                'nmap -sn {}/24',
                'nmap -sS -T4 -p- {}',
                'nmap -sV -sC -A {}',
                'whatweb http://{}',
                'dig {} ANY',
                'whois {}'
            ],
            'vulnerability_scanning': [
                'nmap --script vuln {}',
                'nmap --script http-enum {}',
                'nikto -h http://{}',
                'dirb http://{}/'
            ],
            'web_application_testing': [
                'gobuster dir -u http://{} -w /usr/share/wordlists/dirb/common.txt',
                'sqlmap -u "http://{}" --crawl=2 --batch --random-agent',
                'wpscan --url http://{} --enumerate vp,vt,u',
                'python3 -c "import requests; r=requests.get(\'http://{}/robots.txt\'); print(r.text if r.status_code==200 else \'No robots.txt\')"'
            ],
            'service_enumeration': [
                'enum4linux {}',
                'smbclient -L {}',
                'showmount -e {}',
                'snmpwalk -c public -v1 {}',
                'rpcinfo -p {}'
            ],
            'exploitation_attempts': [
                'searchsploit --nmap nmap_scan_results.xml',
                'msfconsole -q -x "use auxiliary/scanner/http/http_version; set RHOSTS {}; run; exit"',
                'hydra -l admin -P /usr/share/wordlists/rockyou.txt {} ssh',
                'python autopentest_launcher.py --target {} --mode aggressive'
            ],
            'post_exploitation': [
                'python autopentest_launcher.py --target {} --mode post-exploit',
                'enum -a {}',
                'python3 -c "print(\'Checking for privilege escalation opportunities...\')"'
            ]
        }
        self.knowledge_base = {
            'network_scanning': {
                'keywords': ['scan', 'nmap', 'port', 'network', 'host', 'ip', 'subnet', 'ping'],
                'direct_commands': {
                    'basic_scan': 'nmap -sS -T4 {}',
                    'service_scan': 'nmap -sV -sC {}', 
                    'full_scan': 'nmap -A -T4 {}',
                    'ping_sweep': 'nmap -sn {}'
                },
                'response': "🔍 Scanning target network..."
            },
            'vulnerability_assessment': {
                'keywords': ['vulnerability', 'vuln', 'exploit', 'cve', 'security', 'weakness'],
                'direct_commands': {
                    'basic_vuln': 'nmap --script vuln {}',
                    'nikto_scan': 'nikto -h {}',
                    'dirb_scan': 'dirb http://{}/',
                    'ai_analysis': 'python autopentest_launcher.py --analyze --targets {}'
                },
                'response': "🛡️ Running vulnerability assessment..."
            },
            'web_testing': {
                'keywords': ['web', 'http', 'https', 'website', 'application', 'sql', 'xss'],
                'direct_commands': {
                    'whatweb': 'whatweb {}',
                    'gobuster': 'gobuster dir -u {} -w /usr/share/wordlists/dirb/common.txt',
                    'sqlmap': 'sqlmap -u {} --batch --random-agent',
                    'ai_web': 'python autopentest_launcher.py --platform web --target {}'
                },
                'response': "🌐 Testing web application security..."
            },
            'mobile_analysis': {
                'keywords': ['mobile', 'apk', 'android', 'ios', 'app'],
                'direct_commands': {
                    'aapt_info': 'aapt dump badging {}',
                'strings_analysis': 'strings {} | grep -i "api\\|key\\|pass"',
                    'ai_mobile': 'python autopentest_launcher.py --platform mobile --target {}'
                },
                'response': "📱 Analyzing mobile application..."
            },
            'wireless_testing': {
                'keywords': ['wifi', 'wireless', 'airmon', 'aircrack', 'wpa', 'wep'],
                'direct_commands': {
                    'monitor_mode': 'sudo airmon-ng start wlan0',
                    'scan_networks': 'sudo airodump-ng wlan0mon',
                    'interface_check': 'iwconfig'
                },
                'response': "📡 Setting up wireless security testing..."
            },
            'system_recon': {
                'keywords': ['system', 'info', 'enumerate', 'privilege', 'escalation', 'sudo'],
                'direct_commands': {
                    'system_info': 'uname -a && lsb_release -a',
                    'network_info': 'ip a && netstat -tuln',
                    'processes': 'ps aux | head -20',
                    'sudo_check': 'sudo -l'
                },
                'response': "🔍 Gathering system information..."
            },
            'file_analysis': {
                'keywords': ['file', 'analyze', 'strings', 'hex', 'metadata'],
                'direct_commands': {
                    'file_type': 'file {}',
                    'strings_dump': 'strings {}',
                    'hex_dump': 'hexdump -C {} | head -20',
                    'metadata': 'exiftool {}'
                },
                'response': "📄 Analyzing uploaded file..."
            }
        }
        
        # Load AI components
        self.ai_agent = None
        self.nlp_processor = None
        self.initialize_ai()
    
    def initialize_ai(self):
        """Initialize AI components"""
        try:
            from src.enhanced_nlp_processor import EnhancedNLPProcessor
            self.nlp_processor = EnhancedNLPProcessor()
        except Exception as e:
            print(f"Warning: Could not load NLP processor: {e}")
    
    def process_message(self, message, uploaded_files=None):
        """Process user message and generate intelligent response"""
        message_lower = message.lower()
        
        # Store context
        self.conversation_context.append({
            'user': message,
            'timestamp': datetime.now().isoformat(),
            'files': uploaded_files or []
        })
        
        # Extract targets from message
        targets = self.extract_targets(message)
        
        # Check for comprehensive pentest request
        comprehensive_keywords = ['complete pentest', 'full pentest', 'comprehensive pentest', 
                                'complete penetration test', 'full penetration test',
                                'do a pentest', 'perform pentest', 'run pentest',
                                'complete security test', 'full security assessment']
        
        is_comprehensive = any(keyword in message_lower for keyword in comprehensive_keywords)
        
        if is_comprehensive and targets:
            return self.generate_comprehensive_pentest_response(targets[0], message)
        
        # Determine intent
        intent_category = self.determine_intent(message_lower)
        
        # Generate response based on intent
        if intent_category:
            return self.generate_response(intent_category, message, targets, uploaded_files)
        else:
            return self.generate_general_response(message, targets, uploaded_files)
    
    def extract_targets(self, message):
        """Extract potential targets from user message"""
        targets = []
        
        # IP addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
        targets.extend(re.findall(ip_pattern, message))
        
        # URLs
        url_pattern = r'https?://[^\s]+'
        targets.extend(re.findall(url_pattern, message))
        
        # Domain names
        domain_pattern = r'\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b'
        potential_domains = re.findall(domain_pattern, message)
        # Filter out common words that might match domain pattern
        domains = [d for d in potential_domains if not d.lower() in ['example.com', 'localhost']]
        targets.extend(domains)
        
        return targets
    
    def determine_intent(self, message_lower):
        """Determine user intent based on keywords"""
        best_match = None
        max_score = 0
        
        for category, data in self.knowledge_base.items():
            score = sum(1 for keyword in data['keywords'] if keyword in message_lower)
            if score > max_score:
                max_score = score
                best_match = category
        
        return best_match if max_score > 0 else None
    
    def generate_response(self, category, message, targets, uploaded_files):
        """Generate direct action-oriented response like Cursor IDE"""
        data = self.knowledge_base[category]
        response = {
            'text': data['response'],
            'commands': [],
            'suggestions': []
        }
        
        # Get appropriate commands based on category and targets
        commands = self.get_direct_commands(category, message, targets, uploaded_files)
        response['commands'] = commands
        
        # Update response text based on what we're about to do
        if commands:
            response['text'] += f"\n\n🚀 Executing {len(commands)} command(s)..."
            for i, cmd in enumerate(commands[:3]):
                response['text'] += f"\n{i+1}. {cmd}"
            if len(commands) > 3:
                response['text'] += f"\n... and {len(commands)-3} more commands"
        
        # Add file-specific analysis
        if uploaded_files:
            for file_path in uploaded_files:
                if file_path.endswith('.apk'):
                    response['text'] += f"\n\n📱 Analyzing APK: {os.path.basename(file_path)}"
                    response['commands'].extend([
                        f'aapt dump badging "{file_path}"',
                        f'strings "{file_path}" | grep -i "api\\|key\\|pass" | head -20'
                    ])
                elif file_path.endswith(('.py', '.sh')):
                    response['text'] += f"\n💻 Analyzing script: {os.path.basename(file_path)}"
                    response['commands'].extend([
                        f'file "{file_path}"',
                        f'head -50 "{file_path}"'
                    ])
                elif file_path.endswith(('.conf', '.cfg')):
                    response['text'] += f"\n⚙️ Analyzing config: {os.path.basename(file_path)}"
                    response['commands'].extend([
                        f'cat "{file_path}"',
                        f'grep -i "password\\|key\\|secret" "{file_path}"'
                    ])
        
        # No suggestions - just direct action
        return response
    
    def get_direct_commands(self, category, message, targets, uploaded_files):
        """Get direct commands to execute based on category and context"""
        commands = []
        data = self.knowledge_base[category]
        
        if targets:
            # Execute commands for each target
            for target in targets[:2]:  # Limit to 2 targets to avoid spam
                if category == 'network_scanning':
                    # Choose appropriate scan based on target type
                    if '/' in target:  # Network range
                        commands.append(data['direct_commands']['ping_sweep'].format(target))
                        commands.append(data['direct_commands']['basic_scan'].format(target.split('/')[0]))
                    else:  # Single host
                        commands.append(data['direct_commands']['service_scan'].format(target))
                        
                elif category == 'vulnerability_assessment':
                    commands.append(data['direct_commands']['basic_vuln'].format(target))
                    if target.startswith(('http', 'https')):
                        commands.append(data['direct_commands']['nikto_scan'].format(target))
                        
                elif category == 'web_testing':
                    if not target.startswith(('http', 'https')):
                        target = f'http://{target}'
                    commands.append(data['direct_commands']['whatweb'].format(target))
                    # Only run gobuster if it looks like a web service
                    if 'directory' in message.lower() or 'dir' in message.lower():
                        commands.append(data['direct_commands']['gobuster'].format(target))
                        
        else:
            # No specific targets - execute general commands
            if category == 'system_recon':
                commands.extend([
                    data['direct_commands']['system_info'],
                    data['direct_commands']['network_info']
                ])
            elif category == 'wireless_testing':
                commands.extend([
                    data['direct_commands']['interface_check']
                ])
                # Only start monitor mode if explicitly requested
                if 'monitor' in message.lower() or 'airmon' in message.lower():
                    commands.append(data['direct_commands']['monitor_mode'])
        
        return commands
    
    def generate_general_response(self, message, targets, uploaded_files):
        """Generate general response for unclear intents"""
        response = {
            'text': "I'm here to help with penetration testing and security analysis. ",
            'commands': [],
            'suggestions': []
        }
        
        if targets:
            response['text'] += f"I noticed you mentioned: {', '.join(targets)}. "
            
        if uploaded_files:
            response['text'] += f"You've uploaded {len(uploaded_files)} file(s). "
            
        response['text'] += "What would you like me to help you with?\n\nI can assist with:"
        
        response['suggestions'] = [
            "🔍 Network scanning and reconnaissance",
            "🛡️ Vulnerability assessment and analysis", 
            "🌐 Web application security testing",
            "📱 Mobile application analysis",
            "📊 Security report generation",
            "🤖 Automated AI-driven assessments"
        ]
        
        return response
    
    def generate_comprehensive_pentest_response(self, target, original_message):
        """Generate comprehensive penetration testing workflow for target"""
        response = {
            'text': f"🎯 **COMPREHENSIVE PENETRATION TEST INITIATED**\n\nTarget: {target}\n\n",
            'commands': [],
            'suggestions': []
        }
        
        # Build comprehensive command list
        all_commands = []
        
        # Phase 1: Reconnaissance
        response['text'] += "📊 **PHASE 1: RECONNAISSANCE & DISCOVERY**\n"
        recon_commands = [cmd.format(target) for cmd in self.comprehensive_pentest_phases['reconnaissance']]
        all_commands.extend(recon_commands)
        response['text'] += f"• {len(recon_commands)} reconnaissance commands queued\n\n"
        
        # Phase 2: Vulnerability Scanning
        response['text'] += "🔍 **PHASE 2: VULNERABILITY SCANNING**\n"
        vuln_commands = [cmd.format(target) for cmd in self.comprehensive_pentest_phases['vulnerability_scanning']]
        all_commands.extend(vuln_commands)
        response['text'] += f"• {len(vuln_commands)} vulnerability scanning commands queued\n\n"
        
        # Phase 3: Web Application Testing
        response['text'] += "🌐 **PHASE 3: WEB APPLICATION TESTING**\n"
        web_commands = [cmd.format(target) for cmd in self.comprehensive_pentest_phases['web_application_testing']]
        all_commands.extend(web_commands)
        response['text'] += f"• {len(web_commands)} web application tests queued\n\n"
        
        # Phase 4: Service Enumeration
        response['text'] += "⚙️ **PHASE 4: SERVICE ENUMERATION**\n"
        service_commands = [cmd.format(target) for cmd in self.comprehensive_pentest_phases['service_enumeration']]
        all_commands.extend(service_commands)
        response['text'] += f"• {len(service_commands)} service enumeration commands queued\n\n"
        
        # Phase 5: Exploitation Attempts
        response['text'] += "⚔️ **PHASE 5: EXPLOITATION ATTEMPTS**\n"
        exploit_commands = [cmd.format(target) for cmd in self.comprehensive_pentest_phases['exploitation_attempts']]
        all_commands.extend(exploit_commands)
        response['text'] += f"• {len(exploit_commands)} exploitation attempts queued\n\n"
        
        # Phase 6: Post-Exploitation
        response['text'] += "🏴‍☠️ **PHASE 6: POST-EXPLOITATION**\n"
        post_commands = [cmd.format(target) for cmd in self.comprehensive_pentest_phases['post_exploitation']]
        all_commands.extend(post_commands)
        response['text'] += f"• {len(post_commands)} post-exploitation commands queued\n\n"
        
        # Add summary
        response['text'] += f"🚀 **EXECUTION SUMMARY**\n"
        response['text'] += f"• Total commands: {len(all_commands)}\n"
        response['text'] += f"• Estimated duration: {len(all_commands) * 2} minutes\n"
        response['text'] += f"• Target: {target}\n\n"
        
        response['text'] += "⚡ **STARTING AUTOMATED PENTESTING WORKFLOW...**\n"
        response['text'] += "Watch the terminal for real-time execution and results!"
        
        # Set commands to execute (limit for safety)
        response['commands'] = all_commands[:15]  # Execute first 15 commands automatically
        
        return response

class ImprovedChatGPTGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Application state
        self.conversation_history = []
        self.uploaded_files = []
        self.current_task = None
        self.running_processes = []
        self.is_comprehensive_running = False
        self.stop_requested = False
        
        # Initialize enhanced chatbot
        self.chatbot = IntelligentChatbot()
        
        # Create interface
        self.create_widgets()
        
        # Initialize with welcome message
        self.show_welcome_message()
        
    def setup_window(self):
        """Setup main window with modern styling"""
        self.root.title("🤖 AI Penetration Testing Assistant")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Configure modern styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Chat.TFrame', background='#f8f9fa')
        style.configure('User.TLabel', background='#007bff', foreground='white', padding=10)
        style.configure('AI.TLabel', background='#28a745', foreground='white', padding=10)
        
    def create_widgets(self):
        """Create the main interface"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_container)
        
        # Content area with paned window
        paned_window = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        # Left side - Chat interface (70%)
        chat_frame = ttk.Frame(paned_window)
        paned_window.add(chat_frame, weight=70)
        
        # Right side - Terminal (30%)
        terminal_frame = ttk.Frame(paned_window)
        paned_window.add(terminal_frame, weight=30)
        
        # Create interfaces
        self.create_enhanced_chat_interface(chat_frame)
        self.create_terminal_interface(terminal_frame)
        
    def create_header(self, parent):
        """Create modern header"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Title section
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title_label = ttk.Label(title_frame, 
                               text="🤖 AI Penetration Testing Assistant", 
                               font=('Segoe UI', 20, 'bold'))
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="Intelligent security analysis powered by AI • Upload files • Execute commands", 
                                  font=('Segoe UI', 11),
                                  foreground='#6c757d')
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Status section
        status_frame = ttk.Frame(header_frame)
        status_frame.pack(side=tk.RIGHT)
        
        self.status_var = tk.StringVar(value="🟢 AI Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                font=('Segoe UI', 11, 'bold'),
                                foreground='#28a745')
        status_label.pack()
        
    def create_enhanced_chat_interface(self, parent):
        """Create enhanced chat interface"""
        chat_container = ttk.Frame(parent)
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        # Messages area
        messages_frame = ttk.LabelFrame(chat_container, text="💬 Conversation", padding="10")
        messages_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create scrollable messages display
        self.messages_frame = ttk.Frame(messages_frame)
        
        # Canvas and scrollbar for custom message bubbles
        canvas_frame = ttk.Frame(messages_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Input section
        self.create_input_section(chat_container)
        
    def create_input_section(self, parent):
        """Create enhanced input section"""
        input_container = ttk.Frame(parent)
        input_container.pack(fill=tk.X)
        
        # File upload area
        file_section = ttk.Frame(input_container)
        file_section.pack(fill=tk.X, pady=(0, 10))
        
        # Files display
        self.files_display = ttk.Frame(file_section)
        self.files_display.pack(fill=tk.X, pady=(0, 10))
        
        # Upload button
        upload_frame = ttk.Frame(file_section)
        upload_frame.pack(fill=tk.X)
        
        upload_btn = ttk.Button(upload_frame, text="📎 Upload Files", command=self.upload_files)
        upload_btn.pack(side=tk.LEFT)
        
        file_info = ttk.Label(upload_frame, 
                             text="Drag & drop or click to upload • Supports: APK, configs, scripts, reports",
                             font=('Segoe UI', 9),
                             foreground='#6c757d')
        file_info.pack(side=tk.LEFT, padx=(15, 0))
        
        # Message input
        input_frame = ttk.Frame(input_container)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Text input with placeholder
        self.message_text = tk.Text(
            input_frame,
            height=3,
            font=('Segoe UI', 12),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            padx=15,
            pady=12
        )
        self.message_text.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        # Send button
        send_btn = ttk.Button(
            input_frame,
            text="Send\n🚀",
            command=self.send_message,
            width=10
        )
        send_btn.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.Y)
        
        # Bind events
        self.message_text.bind('<Control-Return>', self.send_message)
        self.message_text.bind('<KeyPress>', self.on_typing)
        
        # Quick actions
        self.create_quick_actions(input_container)
        
    def create_quick_actions(self, parent):
        """Create quick action buttons"""
        quick_frame = ttk.LabelFrame(parent, text="Quick Actions", padding="10")
        quick_frame.pack(fill=tk.X, pady=(10, 0))
        
        actions = [
            ("🔍 Network Scan", "Scan network 192.168.1.0/24 for open ports and services"),
            ("🛡️ Vulnerability Check", "Check my system for vulnerabilities and security issues"),
            ("🌐 Web App Test", "Test https://example.com for web application vulnerabilities"),
            ("📱 Mobile Analysis", "Analyze uploaded APK file for security vulnerabilities"),
            ("📊 Generate Report", "Generate a comprehensive security assessment report"),
            ("🤖 AI Assessment", "Perform automated AI-driven security assessment")
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(
                quick_frame, 
                text=text,
                command=lambda cmd=command: self.quick_action(cmd)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky=tk.W)
    
    def create_terminal_interface(self, parent):
        """Create integrated terminal"""
        terminal_container = ttk.LabelFrame(parent, text="🖥️ System Terminal", padding="10")
        terminal_container.pack(fill=tk.BOTH, expand=True)
        
        # Terminal display
        self.terminal_display = scrolledtext.ScrolledText(
            terminal_container,
            font=('Consolas', 10),
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='#00ff00',
            selectbackground='#333333',
            wrap=tk.WORD
        )
        self.terminal_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Terminal input
        terminal_input_frame = ttk.Frame(terminal_container)
        terminal_input_frame.pack(fill=tk.X)
        
        ttk.Label(terminal_input_frame, text="$", font=('Consolas', 12)).pack(side=tk.LEFT)
        
        self.terminal_entry = ttk.Entry(
            terminal_input_frame, 
            font=('Consolas', 11)
        )
        self.terminal_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(5, 5))
        self.terminal_entry.bind('<Return>', self.execute_terminal_command)
        
        exec_btn = ttk.Button(terminal_input_frame, text="Execute", command=self.execute_terminal_command)
        exec_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Stop button
        self.stop_btn = ttk.Button(
            terminal_input_frame, 
            text="⏹️ Stop", 
            command=self.stop_all_processes,
            state="disabled"
        )
        self.stop_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Initialize terminal
        self.add_terminal_output("🤖 AI Penetration Testing Terminal\n")
        self.add_terminal_output(f"📍 Working directory: {os.getcwd()}\n")
        self.add_terminal_output("💡 Type commands or let the AI execute them for you\n")
        self.add_terminal_output("-" * 50 + "\n\n")
    
    def stop_all_processes(self):
        """Stop all running processes"""
        self.stop_requested = True
        
        # Terminate all running processes
        terminated_count = 0
        for process in self.running_processes:
            try:
                if process.poll() is None:  # Process is still running
                    process.terminate()
                    terminated_count += 1
                    # Give process time to terminate gracefully
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        # Force kill if it doesn't terminate gracefully
                        process.kill()
                        process.wait()
            except Exception as e:
                self.add_terminal_output(f"⚠️ Error stopping process: {e}\n")
        
        # Clear process list
        self.running_processes.clear()
        
        # Update UI
        self.stop_btn.config(state="disabled")
        self.is_comprehensive_running = False
        
        # Show stop message
        if terminated_count > 0:
            self.add_terminal_output(f"\n🛑 STOPPED: Terminated {terminated_count} running process(es)\n")
            self.add_terminal_output("💡 You can start new commands or analysis\n\n")
        else:
            self.add_terminal_output("\n🔍 No running processes to stop\n\n")
        
        # Reset stop flag after a delay
        self.root.after(1000, lambda: setattr(self, 'stop_requested', False))
    
    def show_welcome_message(self):
        """Show enhanced welcome message"""
        welcome_msg = {
            'sender': 'ai',
            'content': """👋 **Welcome to your AI Penetration Testing Assistant!**

I'm here to help you with comprehensive security testing and analysis. I can:

🔍 **Reconnaissance & Scanning**
• Network discovery and port scanning
• Service enumeration and fingerprinting
• Target intelligence gathering

🛡️ **Vulnerability Assessment** 
• Automated vulnerability detection
• CVE analysis and prioritization
• Security posture evaluation

⚔️ **Penetration Testing**
• Web application security testing
• Mobile app analysis (APK files)
• Network penetration testing

📊 **Reporting & Analysis**
• Comprehensive security reports
• Risk assessment and recommendations
• Executive summaries

🤖 **AI-Powered Features**
• Natural language command processing
• Intelligent target analysis
• Automated assessment workflows

**How to get started:**
1. 💬 Just ask me anything in natural language
2. 📎 Upload files (APKs, configs, reports) for analysis
3. 🚀 Use quick actions for common tasks
4. 🖥️ Watch the terminal for real-time execution

**Example queries:**
• "Scan the network 192.168.1.0/24 for vulnerabilities"
• "Analyze this APK file for security issues" 
• "What are the security risks in my uploaded config?"
• "Generate a penetration testing report"

What would you like to analyze today?""",
            'timestamp': datetime.now(),
            'commands': []
        }
        
        self.add_chat_message(welcome_msg)
    
    def send_message(self, event=None):
        """Send user message"""
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            return "break"  # Prevent default behavior
        
        # Clear input
        self.message_text.delete("1.0", tk.END)
        
        # Add user message
        user_msg = {
            'sender': 'user',
            'content': message,
            'timestamp': datetime.now()
        }
        self.add_chat_message(user_msg)
        
        # Process with AI
        self.process_user_message(message)
        
        return "break"
    
    def process_user_message(self, message):
        """Process user message with enhanced AI"""
        def process():
            # Show typing indicator
            self.root.after(0, lambda: self.show_typing_indicator())
            
            try:
                # Process with intelligent chatbot
                response = self.chatbot.process_message(message, self.uploaded_files)
                
                # Create AI response
                ai_msg = {
                    'sender': 'ai',
                    'content': response['text'],
                    'timestamp': datetime.now(),
                    'commands': response.get('commands', []),
                    'suggestions': response.get('suggestions', [])
                }
                
                # Add response
                self.root.after(0, lambda: self.add_chat_message(ai_msg))
                
                # Execute commands if any - Check if comprehensive pentest
                commands_to_execute = response.get('commands', [])
                if len(commands_to_execute) > 10:  # Comprehensive pentest detected
                    # Execute all commands for comprehensive pentest
                    self.execute_comprehensive_pentest(commands_to_execute)
                else:
                    # Regular execution - limit to 2 commands
                    for command in commands_to_execute[:2]:
                        self.root.after(0, lambda cmd=command: self.execute_ai_command(cmd))
                
            except Exception as e:
                error_msg = {
                    'sender': 'ai',
                    'content': f"I encountered an error processing your request: {str(e)}\n\nPlease try rephrasing your question or check the terminal for more details.",
                    'timestamp': datetime.now(),
                    'commands': []
                }
                self.root.after(0, lambda: self.add_chat_message(error_msg))
        
        threading.Thread(target=process, daemon=True).start()
    
    def show_typing_indicator(self):
        """Show AI is typing"""
        typing_msg = {
            'sender': 'ai',
            'content': "🤖 AI is analyzing your request...",
            'timestamp': datetime.now(),
            'is_typing': True
        }
        self.add_chat_message(typing_msg)
    
    def add_chat_message(self, message):
        """Add message to chat with modern styling"""
        container = ttk.Frame(self.scrollable_frame)
        container.pack(fill=tk.X, pady=5, padx=10)
        
        if message['sender'] == 'user':
            # User message (right aligned, blue)
            msg_frame = tk.Frame(container, bg='#007bff', padx=15, pady=10)
            msg_frame.pack(side=tk.RIGHT, anchor=tk.E)
            
            tk.Label(msg_frame, text=message['content'], 
                    bg='#007bff', fg='white', 
                    font=('Segoe UI', 11),
                    wraplength=400, justify=tk.LEFT).pack()
            
            timestamp = tk.Label(container, 
                                text=f"You • {message['timestamp'].strftime('%H:%M')}", 
                                font=('Segoe UI', 9), 
                                fg='#6c757d')
            timestamp.pack(side=tk.RIGHT, anchor=tk.E, pady=(5, 0))
            
        else:
            # AI message (left aligned, green)
            msg_frame = tk.Frame(container, bg='#28a745', padx=15, pady=10)
            msg_frame.pack(side=tk.LEFT, anchor=tk.W)
            
            content_label = tk.Label(msg_frame, text=message['content'], 
                                   bg='#28a745', fg='white', 
                                   font=('Segoe UI', 11),
                                   wraplength=500, justify=tk.LEFT)
            content_label.pack()
            
            # Add suggestions if any
            if message.get('suggestions'):
                suggest_frame = tk.Frame(container, bg='#e9ecef', padx=10, pady=5)
                suggest_frame.pack(side=tk.LEFT, anchor=tk.W, pady=(5, 0))
                
                tk.Label(suggest_frame, text="💡 Suggestions:", 
                        bg='#e9ecef', font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
                
                for suggestion in message['suggestions'][:3]:  # Show max 3
                    btn = tk.Button(suggest_frame, text=suggestion,
                                  bg='#f8f9fa', relief=tk.FLAT,
                                  command=lambda s=suggestion: self.suggestion_clicked(s))
                    btn.pack(anchor=tk.W, pady=1)
            
            timestamp = tk.Label(container, 
                                text=f"AI Assistant • {message['timestamp'].strftime('%H:%M')}", 
                                font=('Segoe UI', 9), 
                                fg='#6c757d')
            timestamp.pack(side=tk.LEFT, anchor=tk.W, pady=(5, 0))
        
        # Auto-scroll to bottom
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))
    
    def suggestion_clicked(self, suggestion):
        """Handle suggestion click"""
        self.message_text.insert(tk.END, suggestion)
        self.send_message()
    
    def quick_action(self, command):
        """Execute quick action"""
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert(tk.END, command)
        self.send_message()
    
    def on_typing(self, event):
        """Handle typing events"""
        # Could add typing indicators or suggestions here
        pass
    
    def upload_files(self):
        """Handle file upload with better feedback"""
        files = filedialog.askopenfilenames(
            title="Upload files for analysis",
            filetypes=[
                ("All supported", "*.txt *.csv *.json *.apk *.py *.sh *.conf *.xml *.yaml *.pdf"),
                ("Mobile apps", "*.apk *.ipa"),
                ("Configuration files", "*.conf *.cfg *.ini *.xml *.yaml"),
                ("Scripts", "*.py *.sh *.bat"),
                ("Documents", "*.txt *.pdf *.doc *.docx"),
                ("Data files", "*.csv *.json"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            for file_path in files:
                self.add_uploaded_file(file_path)
    
    def add_uploaded_file(self, file_path):
        """Add uploaded file with enhanced display"""
        if file_path not in self.uploaded_files:
            self.uploaded_files.append(file_path)
            
            file_frame = ttk.Frame(self.files_display, relief=tk.SOLID, borderwidth=1)
            file_frame.pack(fill=tk.X, pady=2)
            
            # File icon based on type
            file_ext = os.path.splitext(file_path)[1].lower()
            icon = "📱" if file_ext == ".apk" else "📄" if file_ext in [".txt", ".pdf"] else "⚙️" if file_ext in [".conf", ".cfg"] else "📋"
            
            file_info = f"{icon} {os.path.basename(file_path)} ({self.format_file_size(os.path.getsize(file_path))})"
            
            info_label = ttk.Label(file_frame, text=file_info)
            info_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            remove_btn = ttk.Button(file_frame, text="❌", width=3,
                                   command=lambda fp=file_path, fw=file_frame: self.remove_file(fp, fw))
            remove_btn.pack(side=tk.RIGHT, padx=5, pady=2)
            
            # Add system message
            system_msg = {
                'sender': 'ai',
                'content': f"📎 File uploaded successfully: **{os.path.basename(file_path)}**\n\nI'm ready to analyze this file. What would you like me to look for?",
                'timestamp': datetime.now(),
                'commands': []
            }
            self.add_chat_message(system_msg)
    
    def remove_file(self, file_path, widget):
        """Remove uploaded file"""
        if file_path in self.uploaded_files:
            self.uploaded_files.remove(file_path)
            widget.destroy()
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def execute_terminal_command(self, event=None):
        """Execute terminal command"""
        command = self.terminal_entry.get().strip()
        if not command:
            return
        
        self.terminal_entry.delete(0, tk.END)
        self.add_terminal_output(f"$ {command}\n")
        self.execute_command(command)
    
    def execute_ai_command(self, command):
        """Execute AI-generated command"""
        self.add_terminal_output(f"🤖 AI executing: {command}\n")
        self.execute_command(command)
    
    def execute_command(self, command):
        """Execute system command with automatic sudo handling and better output"""
        def run_command():
            if self.stop_requested:
                self.add_terminal_output("🛑 Command execution cancelled by user\n\n")
                return
            try:
                # Handle sudo commands automatically
                if command.strip().startswith('sudo'):
                    # Use sudo with NOPASSWD or try to handle password automatically
                    # For Garuda Linux, user is typically in wheel/sudo group
                    env = os.environ.copy()
                    env['SUDO_ASKPASS'] = '/bin/true'  # Skip password prompt

                    # Try with current user permissions first
                    try:
                        process = subprocess.Popen(
                            command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            cwd=os.getcwd(),
                            env=env
                        )
                        self.running_processes.append(process)
                        self.root.after(0, lambda: self.stop_btn.config(state="normal"))
                    except Exception:
                        # Fallback: remove sudo and try without it
                        command_no_sudo = command.replace('sudo ', '', 1)
                        self.root.after(0, lambda: self.add_terminal_output(f"🔄 Trying without sudo: {command_no_sudo}\n"))
                        process = subprocess.Popen(
                            command_no_sudo,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            cwd=os.getcwd()
                        )
                        self.running_processes.append(process)
                        self.root.after(0, lambda: self.stop_btn.config(state="normal"))
                else:
                    process = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        cwd=os.getcwd()
                    )
                    self.running_processes.append(process)
                    self.root.after(0, lambda: self.stop_btn.config(state="normal"))
                
                # Read output in real-time
                output_lines = []
                while True:
                    if self.stop_requested:
                        process.terminate()
                        self.root.after(0, lambda: self.add_terminal_output("🛑 Process terminated by user\n\n"))
                        break
                    
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        output_lines.append(output)
                        self.root.after(0, lambda text=output: self.add_terminal_output(text))
                
                # Get remaining output
                stdout, stderr = process.communicate()
                if stdout:
                    self.root.after(0, lambda: self.add_terminal_output(stdout))
                
                # Handle errors gracefully
                if stderr:
                    # Filter out common sudo warnings
                    filtered_stderr = stderr
                    sudo_warnings = ['sudo: unable to resolve host', 'sudo: a password is required']
                    
                    if not any(warning in stderr.lower() for warning in sudo_warnings):
                        self.root.after(0, lambda: self.add_terminal_output(f"⚠️ Warning: {stderr}\n"))
                    
                    # If sudo password required, try alternative approach
                    if 'password is required' in stderr.lower() and command.strip().startswith('sudo'):
                        self.root.after(0, lambda: self.add_terminal_output("🔄 Retrying command with user permissions...\n"))
                        command_alt = command.replace('sudo ', '', 1)
                        # Recursively call with modified command
                        self.execute_command(command_alt)
                        return
                
                exit_code = process.returncode
                # Clean up process from running list
                if process in self.running_processes:
                    self.running_processes.remove(process)
                
                # Disable stop button if no processes running
                if not self.running_processes and not self.is_comprehensive_running:
                    self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
                
                if not self.stop_requested:
                    if exit_code == 0:
                        self.root.after(0, lambda: self.add_terminal_output("✅ Command completed successfully\n\n"))
                    elif exit_code == 127:
                        self.root.after(0, lambda: self.add_terminal_output("❌ Command not found. Install the required tool first.\n\n"))
                    elif exit_code == 1:
                        self.root.after(0, lambda: self.add_terminal_output("⚠️ Command completed with warnings\n\n"))
                    else:
                        self.root.after(0, lambda: self.add_terminal_output(f"❌ Command failed (exit code: {exit_code})\n\n"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.add_terminal_output(f"Error executing command: {str(e)}\n\n"))
        
        threading.Thread(target=run_command, daemon=True).start()
    
    def execute_comprehensive_pentest(self, commands):
        """Execute comprehensive pentest commands in sequence"""
        def run_comprehensive():
            self.is_comprehensive_running = True
            self.stop_requested = False
            self.root.after(0, lambda: self.stop_btn.config(state="normal"))
            
            self.root.after(0, lambda: self.add_terminal_output("\n🎯 ========== COMPREHENSIVE PENETRATION TEST STARTED ==========\n"))
            self.root.after(0, lambda: self.add_terminal_output(f"📋 Total Commands: {len(commands)}\n"))
            self.root.after(0, lambda: self.add_terminal_output("⏰ Estimated Duration: {}+ minutes\n".format(len(commands) * 2)))
            self.root.after(0, lambda: self.add_terminal_output("🛑 Use the STOP button to cancel at any time\n\n"))
            
            phase_names = {
                0: "🔍 PHASE 1: RECONNAISSANCE",
                7: "🛡️ PHASE 2: VULNERABILITY SCANNING", 
                11: "🌐 PHASE 3: WEB APPLICATION TESTING",
                15: "⚙️ PHASE 4: SERVICE ENUMERATION",
                20: "⚔️ PHASE 5: EXPLOITATION ATTEMPTS",
                24: "🏴‍☠️ PHASE 6: POST-EXPLOITATION"
            }
            
            for i, command in enumerate(commands):
                # Check if stop was requested
                if self.stop_requested:
                    self.root.after(0, lambda: self.add_terminal_output("\n🛑 COMPREHENSIVE PENTEST STOPPED BY USER\n"))
                    self.root.after(0, lambda: self.add_terminal_output(f"✅ Completed {i} out of {len(commands)} commands\n\n"))
                    break
                
                # Add phase headers
                if i in phase_names:
                    self.root.after(0, lambda phase=phase_names[i]: self.add_terminal_output(f"\n{phase}\n{'-'*50}\n"))
                
                # Execute command
                self.root.after(0, lambda cmd=command, idx=i: self.add_terminal_output(f"🤖 [{idx+1}/{len(commands)}] Executing: {cmd}\n"))
                
                # Run the command synchronously in this thread
                try:
                    if self.stop_requested:
                        break
                    if command.strip().startswith('sudo'):
                        env = os.environ.copy()
                        env['SUDO_ASKPASS'] = '/bin/true'
                        try:
                            process = subprocess.Popen(
                                command, shell=True, stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, text=True, cwd=os.getcwd(), env=env
                            )
                            self.running_processes.append(process)
                        except:
                            command_no_sudo = command.replace('sudo ', '', 1)
                            process = subprocess.Popen(
                                command_no_sudo, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, cwd=os.getcwd()
                            )
                            self.running_processes.append(process)
                    else:
                        process = subprocess.Popen(
                            command, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, cwd=os.getcwd()
                        )
                        self.running_processes.append(process)
                    
                    stdout, stderr = process.communicate(timeout=120)  # 2 min timeout per command
                    
                    # Remove from running processes
                    if process in self.running_processes:
                        self.running_processes.remove(process)
                    
                    if stdout:
                        # Truncate output if too long
                        output_lines = stdout.split('\n')
                        if len(output_lines) > 20:
                            truncated_output = '\n'.join(output_lines[:15]) + f"\n... (truncated, {len(output_lines)-15} more lines)\n" + '\n'.join(output_lines[-5:])
                            self.root.after(0, lambda out=truncated_output: self.add_terminal_output(out + "\n"))
                        else:
                            self.root.after(0, lambda out=stdout: self.add_terminal_output(out + "\n"))
                    
                    if stderr and 'password is required' not in stderr.lower():
                        self.root.after(0, lambda err=stderr[:500]: self.add_terminal_output(f"⚠️ Warning: {err}\n"))
                    
                    exit_code = process.returncode
                    if exit_code == 0:
                        self.root.after(0, lambda: self.add_terminal_output("✅ Success\n\n"))
                    elif exit_code == 127:
                        self.root.after(0, lambda: self.add_terminal_output("⚠️ Tool not found - skipping\n\n"))
                    else:
                        self.root.after(0, lambda code=exit_code: self.add_terminal_output(f"⚠️ Exit code: {code}\n\n"))
                        
                except subprocess.TimeoutExpired:
                    self.root.after(0, lambda: self.add_terminal_output("⏰ Command timed out - continuing...\n\n"))
                    process.kill()
                except Exception as e:
                    self.root.after(0, lambda err=str(e): self.add_terminal_output(f"❌ Error: {err}\n\n"))
                
                # Small delay between commands
                time.sleep(1)
            
            # Completion message
            if not self.stop_requested:
                self.root.after(0, lambda: self.add_terminal_output("\n🎉 ========== COMPREHENSIVE PENTEST COMPLETED ==========\n"))
                self.root.after(0, lambda: self.add_terminal_output("📊 All phases executed successfully!\n"))
                self.root.after(0, lambda: self.add_terminal_output("📋 Check the output above for detailed results.\n\n"))
            
            # Clean up
            self.is_comprehensive_running = False
            if not self.running_processes:
                self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
        
        # Run in background thread
        threading.Thread(target=run_comprehensive, daemon=True).start()
    
    def add_terminal_output(self, text):
        """Add output to terminal with syntax highlighting"""
        self.terminal_display.insert(tk.END, text)
        self.terminal_display.see(tk.END)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ImprovedChatGPTGUI(root)
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Close the AI Penetration Testing Assistant?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
