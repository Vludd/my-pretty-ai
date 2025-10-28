from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "TTS Local Service")
APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", 8002))
DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

TTS_MODEL = os.getenv("TTS_MODEL", "")
TTS_USE_CUDA = os.getenv("TTS_USE_CUDA", "False").lower() == "true"
