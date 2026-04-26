import subprocess
from rich.console import Console
from rich.prompt import Confirm

console = Console()

DESTRUCTIVE_KEYWORDS = [
    "rm", "dd", "mkfs", "chmod", "chown", "mv", "install", 
    "remove", "purge", "crontab", "systemctl", "sudo",
    "ufw", "iptables", "docker run", "docker rm"
]

def is_destructive(command: str) -> bool:
    """Flags a command if it modifies state or deletes resources."""
    return any(kw in command.split() for kw in DESTRUCTIVE_KEYWORDS)

def run_command(command: str, explanation: str, dry_run_required: bool = None) -> str:
    """Executes a command safely, catching destruction intents."""
    if dry_run_required is None:
        dry_run_required = is_destructive(command)
    
    if dry_run_required:
        console.print(f"\n[bold yellow]Target Command:[/] {command}")
        console.print(f"[bold cyan]Impact/Explanation:[/] {explanation}")
        
        if not Confirm.ask("[bold red]Are you sure you want to run this?[/]"):
            console.print("[dim]Command cancelled by user.[/dim]")
            return "Execution cancelled by user."
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0 and result.stderr:
            return f"Error: {result.stderr}"
        return result.stdout.strip() if result.stdout else "Success (No Output)"
    except Exception as e:
        return f"Failed to execute command: {e}"
