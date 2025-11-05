from dotenv import load_dotenv
import os

load_dotenv()

LLM_URL = "http://localhost:8001"
TTS_URL = "http://localhost:8002"
STT_URL = "http://localhost:8003"

APP_NAME = os.getenv("APP_NAME", "MyPrettyAI")
APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", 8000)) 
DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "adminpassword")
DB_NAME = os.getenv("DB_NAME", "database")
DB_SCHEMA = os.getenv("DB_SCHEMA", "public")
