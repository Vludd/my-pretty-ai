from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, model_serializer

from app.schemas import BaseConfig
from app.schemas.message import SMessageRead


class SConversationCreate(BaseConfig):
    title: str = Field(..., max_length=255, examples=["New Conversation"])

class SConversationUpdate(BaseConfig):
    title: str = Field(..., max_length=255, examples=["New Conversation"])
        
class SConversationRead(BaseConfig):
    public_id: Optional[UUID]
    title: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
class SConversationReadFull(BaseConfig):
    public_id: UUID
    title: Optional[str]
    messages: Optional[List[SMessageRead]]
    last_message: Optional[SMessageRead]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
