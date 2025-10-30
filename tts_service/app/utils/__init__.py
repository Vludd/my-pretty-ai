from pathlib import Path
import json
import re
import subprocess
from datetime import datetime, timezone
from app.utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "tts_models.json"

def fetch_tts_models() -> list:
    """Running command tts --list_models and parsing result."""
    result = subprocess.run(
        ["tts", "--list_models"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Error while running TTS: {result.stderr}")

    models = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("Name format"):
            continue

        line = re.sub(r"^\d+:\s*", "", line)
        downloaded = "[already downloaded]" in line
        name = line.replace(" [already downloaded]", "").strip()
        parts = name.split("/")
        lang = parts[1] if len(parts) > 1 else "unknown"

        models.append({
            "name": name,
            "language": lang,
            "downloaded": downloaded
        })
    return models

def load_tts_models(use_cache: bool = True) -> list:
    """Load models from cache or force update it"""
    if use_cache and CACHE_FILE.exists():
        logger.debug("Using cached list of models...")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)["models"]

    logger.debug("Fetching list of models...")
    models = fetch_tts_models()
    save_tts_models_cache(models)
    return models

def save_tts_models_cache(models: list):
    """Save model list in JSON."""
    logger.debug("Saving TTS model list in cache...")
    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "models": models
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def refresh_tts_models_cache() -> dict:
    """Force update cache"""
    logger.debug("Force updating TTS models cache...")
    
    models = fetch_tts_models()
    save_tts_models_cache(models)
    models_count = len(models)
    
    logger.debug(f"{models_count} models found")
    return {
        "message": "TTS model cache updated",
        "count": models_count,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
