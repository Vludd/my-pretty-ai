from typing import Sequence

from fastapi import APIRouter, Depends

from app.dependencies import UserServiceDep, get_current_user
from app.models.user import MUser
from app.schemas.user import SUserCreate, SUserRead, SUserUpdate

router = APIRouter()

@router.get("", response_model=Sequence[SUserRead], description="Temporary endpoint to get all users - for admin purposes only")
async def get_users(
    service: UserServiceDep
):
    users: Sequence[MUser] = await service.get_users()
    return [SUserRead.model_validate(user) for user in users]

@router.post("", response_model=SUserRead, deprecated=True, description="Deprecated - Use /register endpoint instead")
async def create_user(
    data: SUserCreate,
    service: UserServiceDep
) -> SUserRead:
    created_user = await service.create_user(data)
    return created_user
