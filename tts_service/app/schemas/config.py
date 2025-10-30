from app.schemas import BaseConfig

from app.types import TTSDevice

class STTSConfig(BaseConfig):
    active_model: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    language: str = "ru"
    device: TTSDevice = TTSDevice.CUDA
    max_concurrent_jobs: int = 2
    save_audio_to_cache: bool = True
