from uuid import UUID

from sqlalchemy import desc, select

from app.core.exceptions import RepositoryError
from app.models import MConversation
from app.repositories import BaseRepository


class UserRecoveryRepository(BaseRepository):
    pass

