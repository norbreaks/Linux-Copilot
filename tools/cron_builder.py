from llm import ask_llm
from .executor import run_command
import json
import re

def build_cron_job(user_request: str):
    prompt = f"""Convert this natural language request to a cron job entry. 
Reply with ONLY a valid JSON object. No markdown, no triple backticks.
Must contain keys: "cron", "command", "explanation".

Request: {user_request}"""
    
    response = ask_llm(prompt)
    
    try:
        # Extra safeguards for local LLM output parsing
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            clean_response = match.group(0)
        else:
            clean_response = response
            
        data = json.loads(clean_response)
        cron_line = f'{data["cron"]} {data["command"]}'
        
        print(f"Proposed Cron: {cron_line}")
        print(f"Explanation: {data.get('explanation', 'None')}")
        
        # Append to user's crontab safely (Note: requires user approval via run_command)
        install_command = f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab -'
        
        run_command(
            install_command,
            explanation=f"Adding cron job: {cron_line}\nReason: {data.get('explanation')}",
            dry_run_required=True
        )
    except Exception as e:
        print(f"Failed to parse LLM response into JSON.\nRaw output: {response}\nError: {e}")
