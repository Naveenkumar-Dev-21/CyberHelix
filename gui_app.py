#!/usr/bin/env python3
"""
AI-Powered Automated Penetration Testing System - GUI Application
Interactive interface for testing and demonstrating the complete system
"""

import sys
import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

# GUI imports
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from tkinter.font import Font

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.ai_model_manager import AIModelManager
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure the src directory and AI models are properly set up")
    sys.exit(1)

class PentestingGUI:
    """Main GUI application for AI-powered penetration testing system"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 AI-Powered Automated Penetration Testing System v1.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize AI Model Manager
        self.ai_manager = None
        self.analysis_thread = None
        self.current_analysis = None
        
        # Color scheme
        self.colors = {
            'bg': '#2b2b2b',
            'panel': '#3c3c3c',
            'accent': '#0078d4',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'text': '#ffffff',
            'text_secondary': '#cccccc'
        }
        
        # Fonts
        self.fonts = {
            'title': Font(family="Arial", size=16, weight="bold"),
            'header': Font(family="Arial", size=12, weight="bold"),
            'body': Font(family="Consolas", size=10),
            'small': Font(family="Arial", size=9)
        }
        
        self.create_widgets()
        self.initialize_system()
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Main title
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="🤖 AI-Powered Automated Penetration Testing System",
            font=self.fonts['title'],
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Multi-Domain Security Analysis with Advanced AI Models",
            font=self.fonts['small'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        subtitle_label.pack()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['panel'])
        style.configure('TNotebook.Tab', padding=[12, 8])
        
        # Create tabs
        self.create_analysis_tab()
        self.create_models_tab()
        self.create_results_tab()
        self.create_system_tab()
        
        # Status bar
        self.create_status_bar()
        
    def create_analysis_tab(self):
        """Create the main analysis tab"""
        
        analysis_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(analysis_frame, text="🎯 Security Analysis")
        
        # Left panel - Input and controls
        left_panel = tk.Frame(analysis_frame, bg=self.colors['panel'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left_panel.pack_propagate(False)
        
        # Target input section
        input_frame = tk.LabelFrame(
            left_panel,
            text="🎯 Target Configuration",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['panel']
        )
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Target input
        tk.Label(
            input_frame,
            text="Target:",
            font=self.fonts['body'],
            fg=self.colors['text'],
            bg=self.colors['panel']
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        self.target_entry = tk.Entry(
            input_frame,
            font=self.fonts['body'],
            bg='#4c4c4c',
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        self.target_entry.pack(fill=tk.X, padx=5, pady=2)
        self.target_entry.insert(0, "https://example.com")
        
        # Preset targets
        presets_frame = tk.Frame(input_frame, bg=self.colors['panel'])
        presets_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(
            presets_frame,
            text="Quick Presets:",
            font=self.fonts['small'],
            fg=self.colors['text_secondary'],
            bg=self.colors['panel']
        ).pack(anchor=tk.W)
        
        presets = [
            ("Web App", "https://api.company.com/v1"),
            ("Network Host", "192.168.1.100"),
            ("Mobile App", "banking-app.apk"),
            ("Domain", "company.com")
        ]
        
        for name, target in presets:
            btn = tk.Button(
                presets_frame,
                text=name,
                font=self.fonts['small'],
                bg=self.colors['accent'],
                fg=self.colors['text'],
                command=lambda t=target: self.set_target(t),
                relief=tk.FLAT
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Analysis options
        options_frame = tk.LabelFrame(
            left_panel,
            text="⚙️ Analysis Options",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['panel']
        )
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Checkboxes for different analysis types
        self.analysis_options = {}
        options = [
            ("network", "Network Security Analysis", True),
            ("web", "Web Application Testing", True),
            ("mobile", "Mobile Security Assessment", True),
            ("advanced", "Advanced AI Models", False)
        ]
        
        for key, text, default in options:
            var = tk.BooleanVar(value=default)
            self.analysis_options[key] = var
            
            chk = tk.Checkbutton(
                options_frame,
                text=text,
                variable=var,
                font=self.fonts['small'],
                fg=self.colors['text'],
                bg=self.colors['panel'],
                selectcolor=self.colors['accent']
            )
            chk.pack(anchor=tk.W, padx=5, pady=2)
        
        # Action buttons
        buttons_frame = tk.Frame(left_panel, bg=self.colors['panel'])
        buttons_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.analyze_btn = tk.Button(
            buttons_frame,
            text="🚀 Start Analysis",
            font=self.fonts['header'],
            bg=self.colors['success'],
            fg=self.colors['text'],
            command=self.start_analysis,
            relief=tk.FLAT,
            height=2
        )
        self.analyze_btn.pack(fill=tk.X, pady=5)
        
        self.stop_btn = tk.Button(
            buttons_frame,
            text="⏹️ Stop Analysis",
            font=self.fonts['body'],
            bg=self.colors['danger'],
            fg=self.colors['text'],
            command=self.stop_analysis,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.stop_btn.pack(fill=tk.X, pady=5)
        
        # Right panel - Live analysis output
        right_panel = tk.Frame(analysis_frame, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Analysis output
        output_frame = tk.LabelFrame(
            right_panel,
            text="📊 Live Analysis Output",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.analysis_output = scrolledtext.ScrolledText(
            output_frame,
            font=self.fonts['body'],
            bg='#1e1e1e',
            fg='#00ff00',
            insertbackground='#00ff00',
            wrap=tk.WORD
        )
        self.analysis_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            output_frame,
            variable=self.progress_var,
            maximum=100,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
    def create_models_tab(self):
        """Create the AI models status tab"""
        
        models_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(models_frame, text="🤖 AI Models")
        
        # Models status section
        status_frame = tk.LabelFrame(
            models_frame,
            text="🔧 AI Models Status",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for models
        columns = ("Model", "Status", "Type", "Features", "Accuracy", "Last Trained")
        self.models_tree = ttk.Treeview(status_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.models_tree.heading(col, text=col)
            self.models_tree.column(col, width=120, anchor=tk.CENTER)
        
        # Scrollbar for treeview
        models_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.models_tree.yview)
        self.models_tree.configure(yscrollcommand=models_scrollbar.set)
        
        self.models_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        models_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Model actions
        actions_frame = tk.Frame(models_frame, bg=self.colors['bg'])
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            actions_frame,
            text="🔄 Refresh Status",
            font=self.fonts['body'],
            bg=self.colors['accent'],
            fg=self.colors['text'],
            command=self.refresh_models_status,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_frame,
            text="🎓 Train All Models",
            font=self.fonts['body'],
            bg=self.colors['warning'],
            fg=self.colors['text'],
            command=self.train_all_models,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
    def create_results_tab(self):
        """Create the results visualization tab"""
        
        results_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(results_frame, text="📈 Analysis Results")
        
        # Results summary
        summary_frame = tk.LabelFrame(
            results_frame,
            text="📊 Analysis Summary",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Summary metrics
        metrics_frame = tk.Frame(summary_frame, bg=self.colors['bg'])
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.result_metrics = {}
        metrics = [
            ("target_type", "Target Type", "N/A"),
            ("risk_level", "Risk Level", "N/A"),
            ("priority_score", "Priority Score", "0/100"),
            ("confidence", "AI Confidence", "0.00"),
            ("models_used", "Models Used", "0"),
            ("attack_vectors", "Attack Vectors", "0")
        ]
        
        for i, (key, label, default) in enumerate(metrics):
            row = i // 3
            col = i % 3
            
            metric_frame = tk.Frame(metrics_frame, bg=self.colors['panel'], relief=tk.RAISED, bd=1)
            metric_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            tk.Label(
                metric_frame,
                text=label,
                font=self.fonts['small'],
                fg=self.colors['text_secondary'],
                bg=self.colors['panel']
            ).pack()
            
            value_label = tk.Label(
                metric_frame,
                text=default,
                font=self.fonts['header'],
                fg=self.colors['text'],
                bg=self.colors['panel']
            )
            value_label.pack()
            self.result_metrics[key] = value_label
        
        # Configure grid weights
        for i in range(3):
            metrics_frame.columnconfigure(i, weight=1)
        
        # Detailed results
        details_frame = tk.LabelFrame(
            results_frame,
            text="📋 Detailed Analysis Results",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.results_output = scrolledtext.ScrolledText(
            details_frame,
            font=self.fonts['body'],
            bg='#1e1e1e',
            fg=self.colors['text'],
            wrap=tk.WORD
        )
        self.results_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Export buttons
        export_frame = tk.Frame(results_frame, bg=self.colors['bg'])
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            export_frame,
            text="💾 Export JSON",
            font=self.fonts['body'],
            bg=self.colors['accent'],
            fg=self.colors['text'],
            command=self.export_results_json,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            export_frame,
            text="📄 Export Report",
            font=self.fonts['body'],
            bg=self.colors['accent'],
            fg=self.colors['text'],
            command=self.export_results_report,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
    def create_system_tab(self):
        """Create the system information and logs tab"""
        
        system_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(system_frame, text="⚙️ System Info")
        
        # System status
        status_frame = tk.LabelFrame(
            system_frame,
            text="📊 System Status",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # System metrics
        sys_metrics_frame = tk.Frame(status_frame, bg=self.colors['bg'])
        sys_metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.system_metrics = {}
        sys_metrics = [
            ("total_models", "Total Models", "0"),
            ("available_models", "Available Models", "0"),
            ("trained_models", "Trained Models", "0"),
            ("total_requests", "Total Requests", "0"),
            ("avg_execution_time", "Avg Execution Time", "0.00s"),
            ("uptime", "System Uptime", "0s")
        ]
        
        for i, (key, label, default) in enumerate(sys_metrics):
            row = i // 3
            col = i % 3
            
            metric_frame = tk.Frame(sys_metrics_frame, bg=self.colors['panel'], relief=tk.RAISED, bd=1)
            metric_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            tk.Label(
                metric_frame,
                text=label,
                font=self.fonts['small'],
                fg=self.colors['text_secondary'],
                bg=self.colors['panel']
            ).pack()
            
            value_label = tk.Label(
                metric_frame,
                text=default,
                font=self.fonts['header'],
                fg=self.colors['text'],
                bg=self.colors['panel']
            )
            value_label.pack()
            self.system_metrics[key] = value_label
        
        # Configure grid weights
        for i in range(3):
            sys_metrics_frame.columnconfigure(i, weight=1)
        
        # System logs
        logs_frame = tk.LabelFrame(
            system_frame,
            text="📝 System Logs",
            font=self.fonts['header'],
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.system_logs = scrolledtext.ScrolledText(
            logs_frame,
            font=self.fonts['body'],
            bg='#1e1e1e',
            fg='#cccccc',
            wrap=tk.WORD
        )
        self.system_logs.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log controls
        log_controls = tk.Frame(system_frame, bg=self.colors['bg'])
        log_controls.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(
            log_controls,
            text="🔄 Refresh Logs",
            font=self.fonts['body'],
            bg=self.colors['accent'],
            fg=self.colors['text'],
            command=self.refresh_system_logs,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            log_controls,
            text="🗑️ Clear Logs",
            font=self.fonts['body'],
            bg=self.colors['danger'],
            fg=self.colors['text'],
            command=self.clear_system_logs,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        
        self.status_frame = tk.Frame(self.root, bg=self.colors['panel'], relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="🔄 Initializing AI Model Manager...",
            font=self.fonts['small'],
            fg=self.colors['text'],
            bg=self.colors['panel'],
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Connection indicator
        self.connection_indicator = tk.Label(
            self.status_frame,
            text="●",
            font=Font(size=12),
            fg=self.colors['warning'],
            bg=self.colors['panel']
        )
        self.connection_indicator.pack(side=tk.RIGHT, padx=5, pady=2)
        
    def initialize_system(self):
        """Initialize the AI Model Manager system"""
        
        def init_worker():
            try:
                self.log_message("🔄 Initializing AI Model Manager...")
                self.ai_manager = AIModelManager()
                
                self.log_message("✅ AI Model Manager initialized successfully")
                self.log_message(f"📊 {len(self.ai_manager.models)} AI models loaded")
                
                # Update UI in main thread
                self.root.after(0, self.on_system_initialized)
                
            except Exception as e:
                error_msg = f"❌ Failed to initialize AI Model Manager: {e}"
                self.log_message(error_msg)
                self.root.after(0, lambda: self.on_system_error(error_msg))
        
        # Start initialization in background thread
        init_thread = threading.Thread(target=init_worker, daemon=True)
        init_thread.start()
        
    def on_system_initialized(self):
        """Handle successful system initialization"""
        
        self.update_status("✅ AI Model Manager ready - System operational")
        self.connection_indicator.configure(fg=self.colors['success'])
        
        # Refresh models status
        self.refresh_models_status()
        self.refresh_system_status()
        
        # Enable analyze button
        self.analyze_btn.configure(state=tk.NORMAL)
        
    def on_system_error(self, error_msg: str):
        """Handle system initialization error"""
        
        self.update_status(f"❌ System error - {error_msg[:50]}...")
        self.connection_indicator.configure(fg=self.colors['danger'])
        
        messagebox.showerror("System Error", error_msg)
        
    def set_target(self, target: str):
        """Set the target in the entry field"""
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, target)
        
    def start_analysis(self):
        """Start the security analysis"""
        
        if not self.ai_manager:
            messagebox.showerror("Error", "AI Model Manager not initialized")
            return
        
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a target to analyze")
            return
        
        # Update UI
        self.analyze_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self.progress_bar.start(10)
        
        # Clear previous output
        self.analysis_output.delete(1.0, tk.END)
        
        # Start analysis in background thread
        self.analysis_thread = threading.Thread(
            target=self.run_analysis,
            args=(target,),
            daemon=True
        )
        self.analysis_thread.start()
        
    def run_analysis(self, target: str):
        """Run the security analysis in background thread"""
        
        try:
            self.log_analysis(f"🎯 Starting security analysis for: {target}")
            self.log_analysis(f"⏰ Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.log_analysis("=" * 60)
            
            start_time = time.time()
            
            # Perform AI analysis
            self.log_analysis("🤖 Invoking AI Model Manager...")
            analysis = self.ai_manager.analyze_target_with_ai(target)
            
            execution_time = time.time() - start_time
            
            # Store results
            self.current_analysis = analysis
            
            # Log results
            self.log_analysis("✅ Analysis completed successfully!")
            self.log_analysis(f"⏱️ Execution time: {execution_time:.2f} seconds")
            self.log_analysis("")
            
            # Display results
            self.display_analysis_results(analysis, execution_time)
            
            # Update UI in main thread
            self.root.after(0, self.on_analysis_complete)
            
        except Exception as e:
            error_msg = f"❌ Analysis failed: {e}"
            self.log_analysis(error_msg)
            self.root.after(0, lambda: self.on_analysis_error(error_msg))
            
    def display_analysis_results(self, analysis, execution_time: float):
        """Display the analysis results in the output"""
        
        self.log_analysis("📊 ANALYSIS RESULTS")
        self.log_analysis("=" * 60)
        
        # Basic info
        self.log_analysis(f"🎯 Target: {analysis.target}")
        self.log_analysis(f"🏷️ Target Type: {analysis.target_type.replace('_', ' ').title()}")
        self.log_analysis(f"🚨 Risk Level: {analysis.risk_level.upper()}")
        self.log_analysis(f"📊 Priority Score: {analysis.priority_score:.1f}/100")
        self.log_analysis("")
        
        # Vulnerability assessment
        vuln = analysis.vulnerability_assessment
        self.log_analysis("🛡️ VULNERABILITY ASSESSMENT")
        self.log_analysis(f"   Primary Prediction: {vuln.get('overall_prediction', 'N/A')}")
        self.log_analysis(f"   AI Confidence: {vuln['confidence']:.2f}")
        self.log_analysis(f"   Consensus Score: {vuln.get('consensus_score', 0):.2f}")
        self.log_analysis(f"   Contributing Models: {vuln['contributing_models']}")
        self.log_analysis("")
        
        # Attack vectors
        self.log_analysis("⚔️ RECOMMENDED ATTACK VECTORS")
        for i, vector in enumerate(analysis.recommended_attack_vectors[:5], 1):
            self.log_analysis(f"   {i}. {vector['vector'].replace('_', ' ').title()}")
            self.log_analysis(f"      Confidence: {vector['confidence']:.2f}")
            self.log_analysis(f"      Priority: {vector.get('priority', 'N/A')}")
            if 'reasoning' in vector:
                self.log_analysis(f"      Reasoning: {vector['reasoning']}")
            self.log_analysis("")
        
        # Execution plan
        self.log_analysis("📋 EXECUTION PLAN")
        for step in analysis.execution_plan:
            phase = step.get('phase', 'unknown').replace('_', ' ').title()
            action = step.get('action', 'unknown').replace('_', ' ').title()
            self.log_analysis(f"   Step {step.get('step', '?')}: {phase} - {action}")
            if 'description' in step:
                self.log_analysis(f"      {step['description']}")
            if 'expected_duration' in step:
                self.log_analysis(f"      Duration: {step['expected_duration']}")
        
        self.log_analysis("")
        self.log_analysis("=" * 60)
        self.log_analysis(f"✅ Analysis completed in {execution_time:.2f} seconds")
        
    def on_analysis_complete(self):
        """Handle successful analysis completion"""
        
        self.analyze_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.progress_bar.stop()
        
        self.update_status("✅ Analysis completed successfully")
        
        # Update results tab
        if self.current_analysis:
            self.update_results_display(self.current_analysis)
        
        # Refresh system status
        self.refresh_system_status()
        
    def on_analysis_error(self, error_msg: str):
        """Handle analysis error"""
        
        self.analyze_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.progress_bar.stop()
        
        self.update_status(f"❌ Analysis failed")
        messagebox.showerror("Analysis Error", error_msg)
        
    def stop_analysis(self):
        """Stop the running analysis"""
        
        if self.analysis_thread and self.analysis_thread.is_alive():
            # Note: Python threads can't be forcefully stopped
            self.log_analysis("⏹️ Analysis stop requested...")
            
        self.analyze_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.progress_bar.stop()
        
        self.update_status("⏹️ Analysis stopped")
        
    def update_results_display(self, analysis):
        """Update the results tab with analysis data"""
        
        # Update metrics
        self.result_metrics['target_type'].configure(
            text=analysis.target_type.replace('_', ' ').title()
        )
        self.result_metrics['risk_level'].configure(
            text=analysis.risk_level.upper(),
            fg=self.get_risk_color(analysis.risk_level)
        )
        self.result_metrics['priority_score'].configure(
            text=f"{analysis.priority_score:.1f}/100"
        )
        self.result_metrics['confidence'].configure(
            text=f"{analysis.vulnerability_assessment['confidence']:.2f}"
        )
        self.result_metrics['models_used'].configure(
            text=str(len(analysis.vulnerability_assessment['contributing_models']))
        )
        self.result_metrics['attack_vectors'].configure(
            text=str(len(analysis.recommended_attack_vectors))
        )
        
        # Update detailed results
        self.results_output.delete(1.0, tk.END)
        
        # Format detailed results as JSON
        results_data = {
            'target': analysis.target,
            'target_type': analysis.target_type,
            'risk_level': analysis.risk_level,
            'priority_score': analysis.priority_score,
            'vulnerability_assessment': analysis.vulnerability_assessment,
            'recommended_attack_vectors': analysis.recommended_attack_vectors,
            'execution_plan': analysis.execution_plan,
            'specialized_recommendations': analysis.specialized_recommendations
        }
        
        formatted_json = json.dumps(results_data, indent=2, default=str)
        self.results_output.insert(1.0, formatted_json)
        
    def get_risk_color(self, risk_level: str) -> str:
        """Get color for risk level"""
        colors = {
            'critical': self.colors['danger'],
            'high': '#ff6b35',
            'medium': self.colors['warning'],
            'low': self.colors['success']
        }
        return colors.get(risk_level.lower(), self.colors['text'])
        
    def refresh_models_status(self):
        """Refresh the AI models status display"""
        
        if not self.ai_manager:
            return
        
        # Clear existing items
        for item in self.models_tree.get_children():
            self.models_tree.delete(item)
        
        try:
            status_report = self.ai_manager.get_model_status_report()
            
            for model_name, status in status_report['model_status'].items():
                if model_name == 'physical':  # Skip non-existent model
                    continue
                    
                # Extract model info
                available = status.get('available', False)
                trained = status.get('trained', False)
                model_info = status.get('model_info', {})
                
                # Format status
                status_text = "✅ Ready" if (available and trained) else "⚠️ Not Ready"
                model_type = model_info.get('type', 'Unknown')
                features = model_info.get('feature_count', 0)
                
                # Get accuracy from metrics
                metrics = model_info.get('metrics', {})
                accuracy = f"{metrics.get('accuracy', 0):.3f}"
                last_trained = metrics.get('last_trained', 'Never')[:10]
                
                # Insert into tree
                self.models_tree.insert('', tk.END, values=(
                    model_name.title().replace('_', ' '),
                    status_text,
                    model_type.title(),
                    features,
                    accuracy,
                    last_trained
                ))
                
        except Exception as e:
            self.log_message(f"❌ Failed to refresh models status: {e}")
            
    def refresh_system_status(self):
        """Refresh system status metrics"""
        
        if not self.ai_manager:
            return
        
        try:
            status_report = self.ai_manager.get_model_status_report()
            manager_info = status_report['manager_info']
            
            # Update metrics
            self.system_metrics['total_models'].configure(
                text=str(manager_info['total_models'])
            )
            self.system_metrics['available_models'].configure(
                text=str(manager_info['available_models'])
            )
            self.system_metrics['trained_models'].configure(
                text=str(manager_info['trained_models'])
            )
            self.system_metrics['total_requests'].configure(
                text=str(manager_info['total_requests'])
            )
            self.system_metrics['avg_execution_time'].configure(
                text=f"{manager_info['average_execution_time']:.3f}s"
            )
            
            # Calculate uptime (simplified)
            uptime = datetime.now().strftime('%H:%M:%S')
            self.system_metrics['uptime'].configure(text=uptime)
            
        except Exception as e:
            self.log_message(f"❌ Failed to refresh system status: {e}")
            
    def train_all_models(self):
        """Train all AI models"""
        
        if not self.ai_manager:
            messagebox.showerror("Error", "AI Model Manager not initialized")
            return
        
        def train_worker():
            try:
                self.log_message("🎓 Starting model training...")
                training_results = self.ai_manager.train_all_models()
                
                success_count = sum(1 for result in training_results.values() if 'error' not in result)
                total_count = len(training_results)
                
                self.log_message(f"✅ Training completed: {success_count}/{total_count} models trained")
                
                # Refresh status in main thread
                self.root.after(0, self.refresh_models_status)
                
            except Exception as e:
                error_msg = f"❌ Model training failed: {e}"
                self.log_message(error_msg)
                self.root.after(0, lambda: messagebox.showerror("Training Error", error_msg))
        
        # Start training in background
        train_thread = threading.Thread(target=train_worker, daemon=True)
        train_thread.start()
        
        messagebox.showinfo("Training Started", "Model training started in background. Check system logs for progress.")
        
    def export_results_json(self):
        """Export analysis results as JSON"""
        
        if not self.current_analysis:
            messagebox.showwarning("No Results", "No analysis results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Analysis Results"
        )
        
        if filename:
            try:
                results_data = {
                    'timestamp': datetime.now().isoformat(),
                    'target': self.current_analysis.target,
                    'target_type': self.current_analysis.target_type,
                    'risk_level': self.current_analysis.risk_level,
                    'priority_score': self.current_analysis.priority_score,
                    'vulnerability_assessment': self.current_analysis.vulnerability_assessment,
                    'recommended_attack_vectors': self.current_analysis.recommended_attack_vectors,
                    'execution_plan': self.current_analysis.execution_plan,
                    'specialized_recommendations': self.current_analysis.specialized_recommendations
                }
                
                with open(filename, 'w') as f:
                    json.dump(results_data, f, indent=2, default=str)
                
                messagebox.showinfo("Export Complete", f"Results exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export results: {e}")
                
    def export_results_report(self):
        """Export analysis results as readable report"""
        
        if not self.current_analysis:
            messagebox.showwarning("No Results", "No analysis results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Analysis Report"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("AI-POWERED AUTOMATED PENETRATION TESTING REPORT\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Target: {self.current_analysis.target}\n")
                    f.write(f"Target Type: {self.current_analysis.target_type}\n")
                    f.write(f"Risk Level: {self.current_analysis.risk_level.upper()}\n")
                    f.write(f"Priority Score: {self.current_analysis.priority_score:.1f}/100\n\n")
                    
                    # Add more detailed report content here...
                    f.write("VULNERABILITY ASSESSMENT\n")
                    f.write("-" * 30 + "\n")
                    vuln = self.current_analysis.vulnerability_assessment
                    f.write(f"AI Confidence: {vuln['confidence']:.2f}\n")
                    f.write(f"Contributing Models: {vuln['contributing_models']}\n\n")
                    
                    f.write("RECOMMENDED ATTACK VECTORS\n")
                    f.write("-" * 30 + "\n")
                    for i, vector in enumerate(self.current_analysis.recommended_attack_vectors, 1):
                        f.write(f"{i}. {vector['vector'].replace('_', ' ').title()}\n")
                        f.write(f"   Confidence: {vector['confidence']:.2f}\n")
                        if 'reasoning' in vector:
                            f.write(f"   Reasoning: {vector['reasoning']}\n")
                        f.write("\n")
                
                messagebox.showinfo("Export Complete", f"Report exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export report: {e}")
                
    def refresh_system_logs(self):
        """Refresh system logs display"""
        # In a real implementation, this would read from log files
        self.system_logs.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] System logs refreshed\n")
        self.system_logs.see(tk.END)
        
    def clear_system_logs(self):
        """Clear system logs display"""
        self.system_logs.delete(1.0, tk.END)
        
    def log_message(self, message: str):
        """Log a message to system logs"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        # Add to system logs
        self.system_logs.insert(tk.END, log_entry)
        self.system_logs.see(tk.END)
        
    def log_analysis(self, message: str):
        """Log a message to analysis output"""
        self.analysis_output.insert(tk.END, message + "\n")
        self.analysis_output.see(tk.END)
        
    def update_status(self, message: str):
        """Update the status bar"""
        self.status_label.configure(text=message)
        
    def on_closing(self):
        """Handle application closing"""
        
        if messagebox.askokcancel("Quit", "Do you want to quit the AI Pentesting System?"):
            if self.ai_manager:
                try:
                    self.ai_manager.shutdown()
                except:
                    pass  # Ignore shutdown errors
            
            self.root.destroy()
            
    def run(self):
        """Start the GUI application"""
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_height()) // 2
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()


def main():
    """Main entry point"""
    
    print("🚀 Starting AI-Powered Automated Penetration Testing System GUI...")
    
    try:
        app = PentestingGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start GUI application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
