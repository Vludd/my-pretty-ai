import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi.exceptions import HTTPException
# from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository_factory import RepositoryFactory
from app.models.user import MUser
from app.schemas.auth import SAccessToken
from app.schemas.user import (SToken, SUserCreate, SUserLogin, SUserRead,
                              SUserUpdate)
from app.utils.encryption import get_password_hash, verify_password
from app.utils.jwt import create_access_token

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.user_repo = RepositoryFactory.get_repository(MUser, db_session)
        
    async def get_by_public_id(self, public_id: str):
        user = await self.user_repo.get_by_public_id(public_id)
        if not user:
            logger.error("User is not found!")
            raise HTTPException(status_code=404, detail="User is not found!")
        
        return user
        
    async def get_users(self):
        users = await self.user_repo.get_all()
        
        if not users:
            logger.error("Users is not found!")
            raise HTTPException(status_code=404, detail="Users is not found!")

        return users
    
    async def create_user(self, data: SUserCreate) -> SUserRead:
        if data.password != data.password_verify:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        hashed_password = get_password_hash(data.password)
        
        user_dict = data.model_dump(exclude={"password", "password_verify"})
        user_dict["password_hash"] = hashed_password
        
        created_user = await self.user_repo.create(user_dict)
        if not created_user:
            logger.error("Users is not created!")
            raise HTTPException(status_code=500, detail="Users is not created!")

        return SUserRead.model_validate(created_user)
    
    async def login_user(self, data: SUserLogin) -> SAccessToken:
        exists_user = await self.user_repo.get_by_username(data.username)
        if not exists_user or not verify_password(data.password, exists_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        update_data = SUserUpdate(
            last_login_at=datetime.now(timezone.utc)
        ).model_dump(exclude_unset=True)
        
        updated_user = await self.user_repo.update(exists_user, update_data)
        if not updated_user:
            raise HTTPException(status_code=500, detail="Error while updating user")
        
        access_token = create_access_token({"sub": str(exists_user.public_id)})
        return SAccessToken(access_token=access_token, token_type="bearer")
    
    async def register_user(self, data: SUserCreate) -> str:
        exists_user = await self.user_repo.get_by_username(data.username)
        if exists_user:
            raise HTTPException(status_code=400, detail="User with this username already exists")
        
        if data.password != data.password_verify:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        hashed_password = get_password_hash(data.password)
        
        user_dict = data.model_dump(exclude={"password", "password_verify"})
        user_dict["password_hash"] = hashed_password
        user_dict["last_login_at"] = datetime.now(timezone.utc)
        
        try:
            created_user = await self.user_repo.create(user_dict)
            if not created_user:
                logger.error("Users is not created!")
                raise HTTPException(status_code=500, detail="Users is not created!")
            
            return str(created_user.public_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")
