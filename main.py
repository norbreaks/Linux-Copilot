import json
import re
from rich.console import Console
from rich.prompt import Prompt
from tools.executor import run_command
from tools.log_whisperer import diagnose_crash
from tools.health import health_report
from tools.cron_builder import build_cron_job
from tools.file_nav import read_file, list_files
from tools.web_search import search_errors
from llm import ask_llm_with_tools
from distro import detect_distro, get_package_manager

console = Console()

SYSTEM_PROMPT = f"""You are LinuxAI, a friendly assistant that helps users navigate Linux.
Distro: {detect_distro()}
Package manager: {get_package_manager()}

When the user asks you to DO something on the system, respond with a JSON block EXACTLY like this (no markdown or external text):
{{"action": "run_command", "command": "<your command>", "explanation": "<why this command>"}}

If the user asks you to read a file, respond:
{{"action": "read_file", "filepath": "<path/to/file>"}}

If compiling a cron job, respond:
{{"action": "schedule", "query": "<the user query>"}}

If asked a question to search the web, respond:
{{"action": "web_search", "query": "<search query>"}}

For general Linux info questions, respond normally in plain English without JSON."""

def main():
    console.print("[bold green]LinuxAI Copilot[/] — via Ollama. Type 'help' for examples. Type 'exit' to quit.\n")
    history = []
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]>[/]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Exiting.[/dim]")
            break
            
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        if not user_input:
            continue
            
        # Hardcoded quick-routes for convenience
        if user_input == "health":
            try:
                console.print(health_report())
            except Exception as e:
                console.print(f"[red]Error checking health: {e}[/]")
            continue
            
        if user_input.startswith("why did") and "crash" in user_input:
            try:
                console.print(diagnose_crash())
            except Exception as e:
                console.print(f"[red]Error whispering to logs: {e}[/]")
            continue
            
        history.append({"role": "user", "content": user_input})
        
        with console.status("[bold green]Thinking..."):
            response = ask_llm_with_tools(SYSTEM_PROMPT, history)
            
        if response.startswith("Error connecting to Ollama"):
            console.print(f"[bold red]{response}[/]")
            continue
        
        # Parse and route tool calls based on phi:3 JSON string
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            try:
                tool = json.loads(match.group(0))
                action = tool.get("action")
                
                if action == "run_command":
                    val = run_command(tool["command"], tool["explanation"])
                    if val is not None:
                        history.append({"role": "assistant", "content": f"Executed command. Result: {val}"})
                elif action == "schedule":
                    build_cron_job(user_input)
                    history.append({"role": "assistant", "content": "Attempted to schedule cron job."})
                elif action == "read_file":
                    content = read_file(tool.get("filepath", ""))
                    console.print(f"[dim]File Content:[/dim]\n{content}")
                    history.append({"role": "assistant", "content": f"File read output:\n{content}"})
                elif action == "web_search":
                    results = search_errors(tool.get("query", ""))
                    console.print(f"[dim]Web Results:[/dim]\n{results}")
                    history.append({"role": "assistant", "content": f"Web search results:\n{results}"})
                else:
                    console.print(response)
                    history.append({"role": "assistant", "content": response})
            except json.JSONDecodeError:
                console.print(response)
                history.append({"role": "assistant", "content": response})
        else:
            console.print(response)
            history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
