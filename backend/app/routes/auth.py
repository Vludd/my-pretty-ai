from fastapi import APIRouter
from typing import Sequence

from app.schemas.user import SUserCreate, SUserRead, SUserUpdate, SUserLogin, SToken

from app.dependencies import UserServiceDep

router = APIRouter()

@router.post("/register")
async def register(data: SUserCreate, service: UserServiceDep):
    token = await service.register_user(data)
    return token

@router.post("/login")
async def login(data: SUserLogin, service: UserServiceDep):
    token = await service.login_user(data)
    return token
