from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "STT Local Service")
APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", 8003))
DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

STT_MODEL = os.getenv("STT_MODEL", "")
STT_USE_CUDA = os.getenv("STT_USE_CUDA", "False").lower() == "true"
