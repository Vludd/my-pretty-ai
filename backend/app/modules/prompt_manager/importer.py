import json
from pathlib import Path

def load_file_prompt(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    
    return file_path.read_text(encoding="utf-8").splitlines()

def import_prompt_json(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt JSON file not found: {file_path}")
    
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)
