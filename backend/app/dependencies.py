from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import JWT_ALGORITHM, JWT_SECRET_KEY
from app.database import get_db
from app.services.conversation import ConversationService
from app.services.llm import LLMService
from app.services.prompt import PromptService
from app.services.tts import TTSService
from app.services.user import UserService

DBSessionDep = Annotated[AsyncSession, Depends(get_db)]

def get_conversation_service(db: DBSessionDep) -> ConversationService: return ConversationService(db)
def get_llm_service(db: DBSessionDep) -> LLMService: return LLMService(db)
def get_tts_service(db: DBSessionDep) -> TTSService: return TTSService(db)
def get_user_service(db: DBSessionDep) -> UserService: return UserService(db)
def get_prompt_service(db: DBSessionDep) -> PromptService: return PromptService(db)

ConversationServiceDep = Annotated[ConversationService, Depends(get_conversation_service)]
LLMServiceDep = Annotated[LLMService, Depends(get_llm_service)]
TTSServiceDep = Annotated[TTSService, Depends(get_tts_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PromptsServiceDep = Annotated[PromptService, Depends(get_prompt_service)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload: dict = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub", "")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_by_public_id(user_id)
    if not user:
        raise credentials_exception
    
    return user
