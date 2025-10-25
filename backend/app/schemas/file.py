# from pydantic import model_serializer, Field
# from uuid import UUID
# from typing import Optional
# from datetime import datetime

# from app.types.messages import SenderType
# from app.schemas import BaseConfig

# class SFileMessageCreate(BaseConfig):
#     content: str

# class SFileMessageUpdate(BaseConfig):
#     content: str
        
# class SFileMessageRead(BaseConfig):
#     public_id: UUID
#     conversation_id: int
#     file_id: int
#     sender_type: SenderType
#     content: Optional[str]
#     created_at: Optional[datetime]
#     updated_at: Optional[datetime]
