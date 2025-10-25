from pydantic import model_serializer, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.types.llm import ContextRole
from app.schemas import BaseConfig

class SContextMessage(BaseConfig):
    role: ContextRole
    content: str
