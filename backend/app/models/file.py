from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, TEXT, BIGINT

from app.database import Base
import app.config as cfg
from app.types.files import FileStatus

TABLENAME = "files"

class MFile(Base):
    __tablename__ = TABLENAME
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Первичный ключ записи"
    )
    
    storage_provider = Column(
        String(32), 
        nullable=False, 
        default="local",
        comment="Провайдер хранилища: local, s3, ..."
    )
    
    storage_bucket = Column(
        String(128), 
        nullable=True,
        comment="Имя бакета/контейнера"
    )
    
    storage_key = Column(
        TEXT, 
        nullable=False,
        comment="Ключ/путь до файла в хранилище"
    )
    
    file_name = Column(
        TEXT, 
        nullable=False,
        comment="Название файла с расширением"
    )
    
    mime_type = Column(
        String(128), 
        nullable=False,
        comment="Тип-MIME"
    )
    
    size_bytes = Column(
        BIGINT, 
        nullable=False,
        comment="Размер файла в байтах"
    )
    
    checksum_sha256 = Column(
        TEXT, 
        nullable=False,
        comment="Контрольная сумма файла"
    )
    
    status = Column(
        Enum(FileStatus, name="file_status", create_constraint=True),
        nullable=False,
        default=FileStatus.ACTIVE,
        comment="Статус файла: active, deleted"
    )
    
    created_at = Column(DateTime(
        timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Дата создания записи"
    )
