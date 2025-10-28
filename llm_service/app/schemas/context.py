from app.types import ContextRole
from app.schemas import BaseConfig

class SContextMessage(BaseConfig):
    role: ContextRole
    content: str
