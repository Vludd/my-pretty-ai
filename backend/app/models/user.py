import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
import app.config as cfg

TABLENAME = "users"

class MUser(Base):
    __tablename__ = TABLENAME
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="PK"
    )
    
    public_id = Column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
        comment="Public UUID of user"
    )
    
    username = Column(
        String(50),
        nullable=False,
        index=True,
        comment="Username"
    )
    
    email = Column(
        String(255), 
        nullable=False,
        unique=True,
        index=True,
        comment="User Email"
    )
    
    password_hash = Column(
        String(255), 
        nullable=True, 
        default=None,
        comment="User password (hashed)"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Updated At"
    )
    
    last_login_at = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Last Login At"
    )
