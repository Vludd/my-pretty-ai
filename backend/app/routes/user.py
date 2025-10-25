from fastapi import APIRouter
from typing import Sequence

from app.schemas.user import SUserCreate, SUserRead, SUserUpdate
from app.models.user import MUser
from app.services.user_service import UserService
from app.dependencies import UserRepo

router = APIRouter()
service = UserService()

@router.get("", response_model=Sequence[SUserRead])
async def get_users(user_repo: UserRepo):
    users: Sequence[MUser] = await service.get_users(user_repo)
    return [SUserRead.model_validate(user) for user in users]

@router.post("", response_model=SUserRead)
async def create_user(data: SUserCreate, user_repo: UserRepo) -> SUserRead:
    created_user = await service.create_user(data, user_repo)
    return created_user
