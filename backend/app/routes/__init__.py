from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.conversations import router as conversations_router
from app.routes.llm import router as llm_router
from app.routes.prompts import router as prompts_router
from app.routes.users import router as users_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(llm_router, prefix="/llm", tags=["LLM"])

api_router.include_router(prompts_router, prefix="/prompts", tags=["Prompts"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["Conversations"])
