import os

def read_file(filepath: str, lines=100) -> str:
    """Reads top N lines of a file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = [next(f) for _ in range(lines)]
        return "".join(content)
    except StopIteration:
        # File is shorter than 'lines'
        pass
    except Exception as e:
        return f"Error reading file {filepath}: {e}"
        
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {filepath}: {e}"

def list_files(directory: str) -> str:
    """Lists files in the given directory."""
    try:
        return "\n".join(os.listdir(directory))
    except Exception as e:
        return f"Error listing directory {directory}: {e}"
