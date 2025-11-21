from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData
import app.config as cfg

SCHEMA_NAME = cfg.DB_SCHEMA
metadata = MetaData(schema=SCHEMA_NAME)

Base = declarative_base(metadata=metadata)
