from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import MConversation
from app.models.message import MMessage
from app.models.prompt import MPrompt
from app.models.user import MUser
from app.models.user_recovery_key import MUserRecoveryKey
from app.repositories import BaseRepository
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository
from app.repositories.prompt import PromptRepository
from app.repositories.user import UserRepository
from app.repositories.user_recovery import UserRecoveryRepository


class RepositoryFactory:
    """Centralized repository factory for dependency injection."""

    _repository_map = {
        MConversation: ConversationRepository,
        MUser: UserRepository,
        MMessage: MessageRepository,
        MPrompt: PromptRepository,
        MUserRecoveryKey: UserRecoveryRepository,
    }

    @classmethod
    def get_repository(cls, model: Type, db_session: AsyncSession):
        """
        Returns an appropriate repository class for the given model.
        Falls back to BaseRepository if no specific one is found.
        """
        repo_class = cls._repository_map.get(model, BaseRepository)
        return repo_class(db_session, model)
