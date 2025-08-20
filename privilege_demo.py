#!/usr/bin/env python3
"""
Privilege Management Demo Script

This script demonstrates how to use the secure privilege management system
for automated pentesting operations.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.privilege_manager import PrivilegeManager
from rich.console import Console
from rich.table import Table

def main():
    console = Console()
    console.print("[bold cyan]🔐 Privilege Management System Demo[/bold cyan]\n")
    
    # Initialize privilege manager
    privilege_manager = PrivilegeManager()
    
    # Display system status
    console.print("[bold]System Status:[/bold]")
    console.print(f"Sudo Available: {'✅' if privilege_manager.sudo_available else '❌'}")
    
    # Show task summary
    summary = privilege_manager.get_task_summary()
    console.print(f"Total Tasks: {summary['total_tasks']}")
    console.print(f"Safe for Automation: {summary['safe_to_automate']}")
    console.print()
    
    # Test various commands
    test_commands = [
        ["nmap", "-sS", "127.0.0.1"],              # Requires sudo
        ["nmap", "-sT", "127.0.0.1"],              # User level
        ["airmon-ng", "start", "wlan0"],           # Requires sudo + confirmation
        ["nuclei", "-u", "http://example.com"],    # User level
        ["sqlmap", "-u", "http://example.com"],    # User level
        ["tcpdump", "-i", "eth0"],                 # Requires sudo
        ["wireshark"],                             # Requires sudo
    ]
    
    console.print("[bold]Command Classification Test:[/bold]")
    classification_table = Table()
    classification_table.add_column("Command", style="cyan")
    classification_table.add_column("Privilege Level", style="yellow")
    classification_table.add_column("Safe Auto", style="green")
    classification_table.add_column("Needs Confirm", style="red")
    
    for cmd in test_commands:
        classification = privilege_manager.classify_command(cmd)
        is_safe, _ = privilege_manager.validate_safe_execution(cmd)
        
        cmd_str = " ".join(cmd)
        safe_auto = "✅" if classification.safe_to_automate and is_safe else "❌"
        needs_confirm = "⚠️" if classification.requires_confirmation else "✅"
        
        classification_table.add_row(
            cmd_str,
            classification.privilege_level.value,
            safe_auto,
            needs_confirm
        )
    
    console.print(classification_table)
    
    # Demonstrate secure execution (if password is available)
    console.print("\n[bold]Execution Test:[/bold]")
    
    # Test a simple command that doesn't require sudo
    test_cmd = ["echo", "Hello from privilege manager"]
    result = privilege_manager.execute_with_privileges(test_cmd)
    
    if result['success']:
        console.print(f"✅ Command executed successfully with {result.get('privilege_used', 'unknown')} privileges")
        console.print(f"Output: {result['stdout'].strip()}")
    else:
        console.print(f"❌ Command failed: {result['stderr']}")
    
    # Check if sudo password is available in environment
    if os.getenv('PENTEST_SUDO_PASS'):
        console.print("\n[yellow]Found sudo password in environment. Testing sudo command...[/yellow]")
        
        # Test a simple sudo command
        sudo_test_cmd = ["whoami"]
        result = privilege_manager.execute_with_privileges(
            sudo_test_cmd, 
            password=os.getenv('PENTEST_SUDO_PASS')
        )
        
        if result['success']:
            console.print(f"✅ Sudo command executed successfully")
            console.print(f"Current user: {result['stdout'].strip()}")
        else:
            console.print(f"❌ Sudo command failed: {result['stderr']}")
    else:
        console.print("\n[dim]No sudo password found in PENTEST_SUDO_PASS environment variable[/dim]")
        console.print("[dim]Use 'python -m src.main privilege --set-password' to set it securely[/dim]")

if __name__ == "__main__":
    main()
