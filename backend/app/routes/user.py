from fastapi import APIRouter
from typing import Sequence

from app.schemas.user import SUserCreate, SUserRead, SUserUpdate
from app.models.user import MUser
from app.dependencies import UserServiceDep

router = APIRouter()

@router.get("", response_model=Sequence[SUserRead])
async def get_users(service: UserServiceDep):
    users: Sequence[MUser] = await service.get_users()
    return [SUserRead.model_validate(user) for user in users]

@router.post("", response_model=SUserRead)
async def create_user(data: SUserCreate, service: UserServiceDep) -> SUserRead:
    created_user = await service.create_user(data)
    return created_user
