from app.data.configs.llm_config_schema import SLLMConfig
from app.core.engine import LLMEngine

llm_config = SLLMConfig()
LLM = LLMEngine(llm_config)