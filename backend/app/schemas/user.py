from pydantic import model_serializer, Field
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.schemas import BaseConfig

class SToken(BaseConfig):
    access_token: str

class SUserLogin(BaseConfig):
    username: str = Field(..., min_length=2, max_length=50, examples=["YourBunnyWrote123"])
    password: str = Field(..., min_length=8, max_length=64, examples=["U6u2nyWr0te!"])

class SUserCreate(BaseConfig):
    username: str = Field(..., min_length=2, max_length=50, examples=["YourBunnyWrote123"])
    email: str = Field(..., max_length=255, examples=["urbunnywrote@example.com"])
    password: str = Field(..., min_length=8, max_length=64, examples=["U6u2nyWr0te!"])
    password_verify: str = Field(..., min_length=8, max_length=64, examples=["U6u2nyWr0te!"])

class SUserUpdate(BaseConfig):
    username: Optional[str] = Field(min_length=2, max_length=50, examples=["YourBunnyWrote123"], default=None)
    email: Optional[str] = Field(max_length=255, examples=["urbunnywrote@example.com"], default=None)
    password: Optional[str] = Field(min_length=8, max_length=64, examples=["U6u2nyWr0te!"], default=None)
    last_login_at: Optional[datetime] = Field(examples=["2025-10-02T12:00:00Z"], default=None)
        
class SUserRead(BaseConfig):
    public_id: UUID
    username: str
    email: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_login_at: Optional[datetime]
    
    # @model_serializer
    # def serialize_in_order(self):
    #     return {
    #         "public_id": self.public_id,
    #         "full_name": self.full_name,
    #         "phone": self.phone,
    #         "role": self.role,
    #         "is_active": self.is_active,
    #         "created_at": self.created_at,
    #         "updated_at": self.updated_at,
    #         "last_login_at": self.last_login_at,
    #     }
