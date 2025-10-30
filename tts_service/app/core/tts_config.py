from pathlib import Path
import json
from threading import Lock

from app.schemas.config import STTSConfig

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CONFIG_FILE = CACHE_DIR / "tts_config.json"

_lock = Lock()

DEFAULT_CONFIG = STTSConfig().model_dump()

def load_config() -> dict:
    """Load a config, if default config is not exist then create it"""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data: dict):
    """Save config in JSON file"""
    with _lock:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def update_config(new_data: dict) -> dict:
    """Partially update current config"""
    config = load_config()
    config.update(new_data)
    validated = STTSConfig(**config).model_dump()
    save_config(validated)
    return validated

def get_config_as_model() -> STTSConfig:
    return STTSConfig(**load_config())
