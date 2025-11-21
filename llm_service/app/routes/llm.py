from typing import List
from fastapi import APIRouter

from app.dependencies import LLM
from app.schemas.context import SContextMessage
from app.schemas.llm import SCompletionRequest

router = APIRouter()

@router.post("/completion")
def completion(data: SCompletionRequest):
    response = LLM.generate(data.text)
    return response

@router.post("/context/load")
def load_conversation(context: List[SContextMessage]):
    layers_order = ["system", "about", "rules", "safety", "personality", "relationship", "context", "time_context"]
    layer_variants = {"personality": "free spirit", "relationship": "stranger" }
    response = LLM.load_conversation(context, layers_order, layer_variants)
    return response
