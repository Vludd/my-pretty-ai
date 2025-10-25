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
        comment="Первичный ключ записи"
    )
    
    public_id = Column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
        comment="Публичный UUID пользователя"
    )
    
    username = Column(
        String(50),
        nullable=False,
        index=True,
        comment="Никнейм пользователя"
    )
    
    email = Column(
        String(255), 
        nullable=False,
        unique=True,
        index=True,
        comment="Email пользователя"
    )
    
    password_hash = Column(
        String(255), 
        nullable=True, 
        default=None,
        comment="Хэшированный пароль пользователя"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Дата создания записи"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Дата обновления записи"
    )
    
    last_login_at = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Дата последнего входа в систему"
    )
