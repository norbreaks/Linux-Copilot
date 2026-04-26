import subprocess
import os
import glob
from llm import ask_llm

def get_journal_tail(lines=50):
    try:
        result = subprocess.run(
            ["journalctl", "-n", str(lines), "--no-pager", "-o", "short"],
            capture_output=True, text=True
        )
        return result.stdout
    except FileNotFoundError:
        return "journalctl command not available (Are you on WSL or missing systemd?)"

def get_wine_log():
    patterns = [
        os.path.expanduser("~/.wine/drive_c/*.log"),
        os.path.expanduser("~/.local/share/Steam/logs/*.txt"),
    ]
    for pattern in patterns:
        files = glob.glob(pattern)
        if files:
            latest = max(files, key=os.path.getmtime)
            with open(latest, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()[-3000:]  # last 3000 chars
    return "No Wine or Steam logs found."

def diagnose_crash(log_source="journal"):
    print(f"[Log Whisperer] Reading {log_source} logs...")
    if log_source == "journal":
        log = get_journal_tail()
    else:
        log = get_wine_log()
        
    prompt = f"""You are a Linux expert. Analyze this log and explain:
1. What crashed and why (in plain English)
2. The most likely fix
3. If there is a command to apply the fix, output it exactly.

LOG DATA:
{log}"""
    
    return ask_llm(prompt)
