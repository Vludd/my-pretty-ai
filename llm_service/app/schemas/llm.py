from app.types import ContextRole
from app.schemas import BaseConfig

class SCompletionRequest(BaseConfig):
    text: str
