import subprocess
import psutil
from llm import ask_llm

def collect_health_data():
    """Collects CPU, RAM, Disk, and Sensor data safely."""
    try:
        df_res = subprocess.run(["df", "-h", "--output=target,size,used,avail,pcent"], 
                                capture_output=True, text=True)
        df = df_res.stdout
    except FileNotFoundError:
        df = "df command not available"
    
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    
    try:
        sensors_res = subprocess.run(["sensors"], capture_output=True, text=True)
        sensors = sensors_res.stdout
    except FileNotFoundError:
        sensors = "sensors command not available"
    
    return {
        "cpu_percent": cpu,
        "ram_used_gb": round(mem.used / 1e9, 1),
        "ram_total_gb": round(mem.total / 1e9, 1),
        "disk": df,
        "temps": sensors
    }

def health_report():
    data = collect_health_data()
    prompt = f"""You are a helpful Linux assistant. Summarize this system health data in 3-4 friendly sentences. 
Warn if anything looks concerning (high CPU, low disk space, high temps). 
Data: {data}"""
    return ask_llm(prompt)
