import httpx

from uuid import UUID
from typing import List, Sequence
from fastapi.exceptions import HTTPException

from app.dependencies import UserRepo, ConversationRepo, MessageRepo, LLM_URL
from app.schemas.message import SMessageCreate
from app.types.messages import SenderType
from app.utils.logger import logger

class TTSService:
    async def get_models(self):
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.get(f"{LLM_URL}/models")
                
                if response.status_code == 404:
                    logger.error(f"TTS Service request error: {response.text}")
                    raise HTTPException(
                        status_code=404,
                        detail=response.text
                    )

                elif response.status_code == 400:
                    logger.error(f"TTS Service request error: {response.text}")
                    raise HTTPException(
                        status_code=400,
                        detail=response.text
                    )

                elif not response.is_success:
                    logger.error(f"TTS Service request error: {response.text}")
                    raise HTTPException(
                        status_code=502,
                        detail=response.text
                    )
                
                llm_answer = response.json()["reply"]
                if not llm_answer:
                    logger.error("Response received, but unable to retrieve response content")
                    raise HTTPException(status_code=500, detail="Response received, but unable to retrieve response content")
                
                return response.json()
            
            except httpx.ConnectTimeout:
                logger.error("TTS Service request timeout")
                raise HTTPException(
                    status_code=504,
                    detail="TTS Service request timeout"
                )

            except httpx.ConnectError:
                logger.error("TTS Service unavailable")
                raise HTTPException(
                    status_code=503,
                    detail="TTS Service unavailable"
                )

            except Exception as e:
                logger.exception("Unexpected error when calling TTS Service")
                raise HTTPException(
                    status_code=500,
                    detail="Unexpected error when calling TTS Service"
                )
    