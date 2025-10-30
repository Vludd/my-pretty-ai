from enum import Enum

class TTSDevice(str, Enum):
    CUDA = "cuda"
    CPU = "cpu"

class EmotionType(str, Enum):
    Neutral = "neutral"
    Applause = "applause"
    Whisper = "whisper"
    Sarcastic = "sarcastic"
    Excited = "excited"
    Mischievously = "mischievously"
