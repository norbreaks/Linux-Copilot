import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3:mini"

def ask_llm(prompt: str) -> str:
    """Sends a single prompt to the Ollama API."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.3}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def ask_llm_with_tools(system_prompt: str, history: list) -> str:
    """Sends conversational history with a system prompt to Ollama."""
    messages = [{"role": "system", "content": system_prompt}] + history
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")
    except Exception as e:
        return f"Error connecting to Ollama: {e}"
