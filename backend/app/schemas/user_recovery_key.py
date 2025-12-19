from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas import BaseConfig


class SUserRecoveryKeys(BaseConfig):
    keys: list[str] = Field(examples=[["MPA1-XXXX-XXXX-XXXX", "MPA1-XXXX-XXXX-XXXX", "MPA1-XXXX-XXXX-XXXX", "MPA1-XXXX-XXXX-XXXX"]])

class SUserRecoveryKeyRead(BaseConfig):
    key_hash: str
    used: bool
    created_at: Optional[datetime]
    used_at: Optional[datetime]
