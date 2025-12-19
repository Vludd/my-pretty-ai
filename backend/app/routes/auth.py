from fastapi import APIRouter, Depends, Form

from app.dependencies import get_current_user, get_user_service
from app.schemas import SMessageResponse
from app.schemas.auth import SAccessToken
from app.schemas.user import SUserCreate, SUserLogin
from app.services.user import UserService

router = APIRouter()

@router.get("/me")
async def me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/register")
async def register(
    data: SUserCreate,
    service: UserService = Depends(get_user_service)
):
    token = await service.register_user(data)
    return token

@router.post("/login", response_model=SAccessToken)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    service: UserService = Depends(get_user_service)
):
    data = SUserLogin(username=username, password=password)
    token = await service.login_user(data)
    return token

@router.post("/recover-account", response_model=SMessageResponse)
async def recover_account(
    key: str = Form(...),
    new_password: str = Form(...),
    password_verify: str = Form(...),
    service: UserService = Depends(get_user_service)
):
    pass

