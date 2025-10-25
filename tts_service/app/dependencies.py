from enum import Enum
from app.core.tts_engine import TTSEngine

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTSEngine(MODEL_NAME, use_cuda=False)

class EmotionType(str, Enum):
    Neutral = "neutral"
    Applause = "applause"
    Whisper = "whisper"
    Sarcastic = "sarcastic"
    Excited = "excited"
    Mischievously = "mischievously"