from fastapi import APIRouter
from app.routes.auth import router as auth_router
from app.routes.llm import router as llm_router
from app.routes.user import router as user_router
from app.routes.conversation import router as conversation_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(llm_router, prefix="/llm", tags=["LLM"])
api_router.include_router(conversation_router, prefix="/conversations", tags=["Conversations"])
