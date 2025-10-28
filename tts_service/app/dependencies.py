from enum import Enum
from app.core.tts_engine import TTSEngine

from app.config import TTS_MODEL, TTS_USE_CUDA

tts = TTSEngine(TTS_MODEL, use_cuda=TTS_USE_CUDA)

class EmotionType(str, Enum):
    Neutral = "neutral"
    Applause = "applause"
    Whisper = "whisper"
    Sarcastic = "sarcastic"
    Excited = "excited"
    Mischievously = "mischievously"
