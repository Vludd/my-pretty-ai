from pydantic import model_serializer, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.types.messages import SenderType
from app.schemas import BaseConfig

class SMessageCreate(BaseConfig):
    content: str = Field(..., min_length=1, examples=["Hello world!"])
    sender_type: SenderType = Field(..., examples=[SenderType.USER])

class SMessageUpdate(BaseConfig):
    content: str = Field(..., min_length=1, examples=["Hello world!"])
        
class SMessageRead(BaseConfig):
    public_id: UUID
    sender_type: SenderType
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
