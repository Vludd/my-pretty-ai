from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from fastapi.exceptions import HTTPException

from app.models.user import MUser

from app.schemas.user import SUserCreate, SUserRead, SUserUpdate, SUserLogin, SToken

from app.core.repository_factory import RepositoryFactory

from passlib.hash import argon2

from app.utils.logger import logger

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.user_repo = RepositoryFactory.get_repository(MUser, db_session)
        
    async def get_users(self):
        users = await self.user_repo.get_all()
        
        if not users:
            logger.error("Users is not found!")
            raise HTTPException(status_code=404, detail="Users is not found!")

        return users
    
    async def create_user(self, data: SUserCreate) -> SUserRead:
        if data.password != data.password_verify:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        hashed_password = argon2.hash(data.password)
        
        user_dict = data.model_dump(exclude={"password", "password_verify"})
        user_dict["password_hash"] = hashed_password
        
        created_user = await self.user_repo.create(user_dict)
        if not created_user:
            logger.error("Users is not created!")
            raise HTTPException(status_code=500, detail="Users is not created!")

        return SUserRead.model_validate(created_user)
    
    async def login_user(self, data: SUserLogin):
        exists_user = await self.user_repo.get_by_username(data.username)
        if not exists_user:
            raise HTTPException(status_code=500, detail="User is not registered")
        
        if not exists_user.password_hash: # type: ignore
            raise HTTPException(status_code=400, detail="User account is broken")
        
        verified = argon2.verify(data.password, exists_user.password_hash)
        if not verified:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        update_data = SUserUpdate(
            last_login_at=datetime.now(timezone.utc)
        ).model_dump(exclude_unset=True)
        
        updated_user = await self.user_repo.update(exists_user, update_data)
        if not updated_user:
            raise HTTPException(status_code=500, detail="Error while updating user")
        
        return {"public_id": str(exists_user.public_id)}
    
    async def register_user(self, data: SUserCreate) -> str:
        if data.password != data.password_verify:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        
        hashed_password = argon2.hash(data.password)
        
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
