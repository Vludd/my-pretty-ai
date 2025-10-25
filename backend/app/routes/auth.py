from fastapi import APIRouter
from typing import Sequence

from app.schemas.user import SUserCreate, SUserRead, SUserUpdate, SUserLogin, SToken
from app.models.user import MUser
from app.services.user_service import UserService
from app.dependencies import UserRepo

router = APIRouter()
service = UserService()

@router.post("/register")
async def register(data: SUserCreate, user_repo: UserRepo):
    token = await service.register_user(data, user_repo)
    return token

@router.post("/login")
async def login(data: SUserLogin, user_repo: UserRepo):
    token = await service.login_user(data, user_repo)
    return token
