from pydantic import model_serializer, Field
from typing import Optional
from datetime import datetime

from app.schemas import BaseConfig

class SConversationCreate(BaseConfig):
    title: str = Field(..., max_length=255, examples=["New Conversation"])

class SConversationUpdate(BaseConfig):
    title: str = Field(..., max_length=255, examples=["New Conversation"])
        
class SConversationRead(BaseConfig):
    public_id: int
    user_id: int
    title: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
