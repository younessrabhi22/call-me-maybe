import json
from typing import List, Dict, Any

def load_json(filepath: str) -> Any:
    """Reads a JSON file and returns the data."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data: Any, filepath: str) -> None:
    """Writes data to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
