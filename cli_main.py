#!/usr/bin/env python3
"""
Enhanced CLI interface for Automatic Pentesting Framework
Main entry point with interactive menu and path traversal support
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import click
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import pyfiglet

console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pentest_cli.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'rich',
        'click',
        'questionary',
        'pyfiglet',
        'pathlib'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        console.print(f"[red]Missing required packages: {', '.join(missing)}[/red]")
        console.print("[yellow]Please install them using:[/yellow]")
        console.print(f"[cyan]pip install {' '.join(missing)}[/cyan]")
        return False
    
    return True


def display_welcome():
    """Display welcome message."""
    banner = pyfiglet.figlet_format("AutoPenTest", font="slant")
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print("[bold]🔐 Automated Penetration Testing Framework[/bold]")
    console.print("[dim]Enhanced CLI with Interactive Menu and File Browser[/dim]")
    console.print()
    
    # Display feature highlights
    features = [
        "🎯 Interactive module browser with categorization",
        "📂 Advanced file browser with path traversal",
        "🔍 Smart module search and discovery",
        "📊 Real-time execution status and results",
        "💾 Session management and history tracking",
        "📝 Automated report generation",
        "🤖 AI-powered analysis modules",
        "⚙️ Dynamic module loading and execution"
    ]
    
    console.print(Panel(
        "\n".join(features),
        title="[bold cyan]Key Features[/bold cyan]",
        border_style="cyan"
    ))


@click.group(invoke_without_command=True)
@click.option('--interactive', '-i', is_flag=True, default=True, help='Launch interactive CLI (default)')
@click.option('--module', '-m', help='Direct module execution')
@click.option('--list-modules', '-l', is_flag=True, help='List all available modules')
@click.option('--check-tools', is_flag=True, help='Check tool availability')
@click.pass_context
def cli(ctx, interactive, module, list_modules, check_tools):
    """
    AutoPenTest Enhanced CLI Interface
    
    This is the main entry point for the automated pentesting framework.
    It provides an interactive menu system with file browsing capabilities.
    """
    
    # Check dependencies first
    if not check_dependencies():
        ctx.exit(1)
    
    if ctx.invoked_subcommand is None:
        if list_modules:
            list_all_modules()
        elif check_tools:
            check_tool_availability()
        elif module:
            execute_module_direct(module)
        else:
            # Default: launch interactive CLI
            launch_interactive_cli()


def launch_interactive_cli():
    """Launch the interactive CLI interface."""
    display_welcome()
    
    try:
        # Import and run the CLI interface
        from src.cli_interface import CLIInterface
        
        console.print("[bold green]Starting interactive CLI...[/bold green]\n")
        
        cli_interface = CLIInterface()
        cli_interface.run()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except ImportError as e:
        console.print(f"[red]Failed to import CLI interface: {e}[/red]")
        console.print("[yellow]Make sure all modules are properly installed[/yellow]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error in CLI")
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


def list_all_modules():
    """List all available modules."""
    try:
        from src.module_manager import get_module_manager
        
        manager = get_module_manager()
        
        console.print(Panel(
            "[bold cyan]Available Pentesting Modules[/bold cyan]",
            border_style="cyan"
        ))
        
        # Group modules by category
        categories = manager.get_categories()
        
        for category in categories:
            console.print(f"\n[bold yellow]{category.upper()}[/bold yellow]")
            
            modules = manager.list_modules(category)
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Name", style="cyan", width=20)
            table.add_column("Display Name", style="white", width=25)
            table.add_column("Description", style="dim", width=50)
            table.add_column("Requirements", style="yellow", width=15)
            
            for module in modules:
                reqs = []
                if module.requires_root:
                    reqs.append("Root")
                if module.requires_api_keys:
                    reqs.append("API Keys")
                
                table.add_row(
                    module.name,
                    module.display_name,
                    module.description[:47] + "..." if len(module.description) > 47 else module.description,
                    ", ".join(reqs) if reqs else "None"
                )
            
            console.print(table)
        
        console.print(f"\n[dim]Total modules: {len(manager.modules)}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error listing modules: {e}[/red]")


def check_tool_availability():
    """Check availability of external tools."""
    try:
        from src.utils import check_tool_available
        from src.config import Config
        
        console.print(Panel(
            "[bold cyan]Tool Availability Check[/bold cyan]",
            border_style="cyan"
        ))
        
        tools = {
            "Nmap": Config.NMAP_PATH,
            "Nuclei": Config.NUCLEI_PATH,
            "Nikto": Config.NIKTO_PATH,
            "SQLMap": Config.SQLMAP_PATH,
            "Metasploit": "msfconsole",
            "Burp Suite": Config.BURP_PATH,
            "Wireshark": "wireshark",
            "Aircrack-ng": Config.AIRCRACK_NG_PATH,
            "John the Ripper": "john",
            "Hashcat": "hashcat",
            "Hydra": "hydra",
            "Gobuster": "gobuster",
            "Ffuf": "ffuf",
            "Amass": Config.AMASS_PATH,
            "theHarvester": Config.THEHARVESTER_PATH
        }
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Tool", style="cyan", width=20)
        table.add_column("Status", style="white", width=15)
        table.add_column("Path/Command", style="yellow", width=30)
        
        available_count = 0
        for tool_name, tool_path in tools.items():
            is_available = check_tool_available(tool_path)
            if is_available:
                available_count += 1
                status = "✅ Available"
            else:
                status = "❌ Not Found"
            
            table.add_row(tool_name, status, tool_path)
        
        console.print(table)
        console.print(f"\n[bold]Summary:[/bold] {available_count}/{len(tools)} tools available")
        
        if available_count < len(tools):
            console.print("\n[yellow]Some tools are missing. Install them for full functionality.[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error checking tools: {e}[/red]")


def execute_module_direct(module_name: str):
    """Execute a module directly from command line.
    
    Args:
        module_name: Name of the module to execute
    """
    try:
        from src.module_manager import get_module_manager
        
        manager = get_module_manager()
        
        if module_name not in manager.modules:
            console.print(f"[red]Module '{module_name}' not found[/red]")
            console.print("[yellow]Use --list-modules to see available modules[/yellow]")
            return
        
        # Display module info
        manager.display_module_info(module_name)
        
        console.print("\n[yellow]Direct module execution requires the interactive CLI[/yellow]")
        console.print("[cyan]Launching interactive mode...[/cyan]\n")
        
        # Launch interactive CLI and navigate to the module
        from src.cli_interface import CLIInterface
        cli_interface = CLIInterface()
        cli_interface.execute_module_interactive(module_name)
        
    except Exception as e:
        console.print(f"[red]Error executing module: {e}[/red]")


@cli.command()
@click.argument('target')
@click.option('--quick', is_flag=True, help='Quick scan mode')
def scan(target, quick):
    """Run a quick scan on the target."""
    console.print(f"[bold]Scanning target: {target}[/bold]")
    
    try:
        from src.cli_interface import CLIInterface
        
        cli_interface = CLIInterface()
        cli_interface.current_session['target'] = target
        
        if quick:
            console.print("[cyan]Running quick scan...[/cyan]")
            cli_interface._run_module("recon", "scan_target", [target])
        else:
            console.print("[cyan]Running comprehensive scan...[/cyan]")
            cli_interface._run_module("recon", "scan_target", [target])
            cli_interface._run_module("vuln_scanner", "scan_target", [target])
        
        console.print("[green]✅ Scan completed![/green]")
        
    except Exception as e:
        console.print(f"[red]Scan failed: {e}[/red]")


@cli.command()
def browser():
    """Launch the file browser directly."""
    console.print("[bold cyan]File Browser[/bold cyan]\n")
    
    try:
        from src.file_browser import FileBrowser
        
        browser = FileBrowser()
        
        # Interactive file selection
        file_path = browser.browse(select_type="any")
        
        if file_path:
            console.print(f"[green]Selected: {file_path}[/green]")
        else:
            console.print("[yellow]No file selected[/yellow]")
            
    except Exception as e:
        console.print(f"[red]File browser error: {e}[/red]")


@cli.command()
@click.option('--category', '-c', help='Filter by category')
def modules(category):
    """Browse and execute modules."""
    try:
        from src.module_manager import get_module_manager
        
        manager = get_module_manager()
        
        if category:
            console.print(f"[bold]Modules in category: {category}[/bold]\n")
            manager.display_modules_table(category)
        else:
            console.print("[bold]All available modules:[/bold]\n")
            manager.display_modules_table()
            
    except Exception as e:
        console.print(f"[red]Error browsing modules: {e}[/red]")


@cli.command()
def interactive():
    """Launch the interactive CLI (same as default)."""
    launch_interactive_cli()


if __name__ == '__main__':
    try:
        # Set up environment
        os.environ['PYTHONPATH'] = str(Path(__file__).parent)
        
        # Check if questionary is installed (required for interactive mode)
        try:
            import questionary
        except ImportError:
            console.print("[red]questionary package is required for the interactive CLI[/red]")
            console.print("[yellow]Install it with: pip install questionary[/yellow]")
            sys.exit(1)
        
        # Run the CLI
        cli()
        
    except Exception as e:
        logger.exception("Fatal error")
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)
