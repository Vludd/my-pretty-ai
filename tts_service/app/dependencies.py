from enum import Enum
from app.core.tts_engine import TTSEngine
from app.types import TTSDevice

from app.config import TTS_MODEL

tts = TTSEngine(TTS_MODEL)
