import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as ex
from app.core.repository_factory import RepositoryFactory
from app.models.user import MUser
from app.models.user_recovery_key import MUserRecoveryKey
from app.schemas.auth import SAccessToken
from app.schemas.user import SUserCreate, SUserLogin, SUserRead, SUserUpdate
from app.schemas.user_recovery_key import SUserRecoveryKeys
from app.utils.encryption import (get_password_hash, hash_recovery_key,
                                  verify_password)
from app.utils.jwt import create_access_token
from app.utils.recovery_keys_generator import generate_recovery_keys

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.user_repo = RepositoryFactory.get_repository(MUser, db_session)
        self.user_recovery_repo = RepositoryFactory.get_repository(MUserRecoveryKey, db_session)
        
    async def get_by_public_id(self, public_id: str):
        user = await self.user_repo.get_by_public_id(public_id)
        if not user:
            raise ex.NotFoundException("User is not found!", log_level="warning")
        
        return user
        
    async def get_users(self):
        users = await self.user_repo.get_all()
        
        if not users:
            raise ex.NotFoundException("Users is not found!", log_level="warning")

        return users
    
    async def create_user(self, data: SUserCreate) -> SUserRead:
        if data.password != data.password_verify:
            raise ex.AppException("Passwords do not match")
        
        hashed_password = get_password_hash(data.password)
        
        user_dict = data.model_dump(exclude={"password", "password_verify"})
        user_dict["password_hash"] = hashed_password
        
        created_user = await self.user_repo.create(user_dict)
        if not created_user:
            raise ex.InternalServerException("User is not created!")

        return SUserRead.model_validate(created_user)
    
    async def login_user(self, data: SUserLogin) -> SAccessToken:
        exists_user = await self.user_repo.get_by_username(data.username)
        if not exists_user or not verify_password(data.password, exists_user.password_hash):
            raise ex.ForbiddenException("Invalid credentials!")
        
        update_data = SUserUpdate(
            last_login_at=datetime.now(timezone.utc)
        ).model_dump(exclude_unset=True)
        
        updated_user = await self.user_repo.update(exists_user, update_data)
        if not updated_user:
            raise ex.InternalServerException("Error while updating user!")
        
        access_token = create_access_token({"sub": str(exists_user.public_id)})
        return SAccessToken(access_token=access_token, token_type="bearer")
    
    async def register_user(self, data: SUserCreate):
        exists_user = await self.user_repo.get_by_username(data.username)
        if exists_user:
            raise ex.AppException("User with this username already exists!", log_level="warning")
        
        if data.password != data.password_verify:
            raise ex.AppException("Passwords do not match!", log_level="warning")
        
        hashed_password = get_password_hash(data.password)
        
        user_dict = data.model_dump(exclude={"password", "password_verify"})
        user_dict["password_hash"] = hashed_password
        user_dict["last_login_at"] = datetime.now(timezone.utc)
        
        created_user: MUser = await self.user_repo.create(user_dict)
        
        if not created_user:
            raise ex.InternalServerException("User is not created!")
        
        generated_keys: list[str] = generate_recovery_keys()
        
        logger.debug(generated_keys)
        
        if not generated_keys:
            raise ex.InternalServerException("Recovery keys is not created for user!")
        
        for k in generated_keys:
            logger.debug(f"Recovery key: {k}")
            
            hashed_key = hash_recovery_key(k)
            key_data = { "user_id": created_user.id, "key_hash": hashed_key, "used": False }
            
            logger.debug(f"Recovery key data: {key_data}")
            
            created_key = await self.user_recovery_repo.create(key_data)
            if not created_key:
                raise ex.InternalServerException("Recovery key is not created for user!")

        return SUserRecoveryKeys(keys=generated_keys)
