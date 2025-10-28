from app.data.configs.llm_config_schema import SLLMConfig
from app.core.engine import LLMEngine

llm_config = SLLMConfig()
LLM = LLMEngine(
    llm_config, 
    # layers_order=["system", "about", "rules", "safety", "personality", "relationship", "context", "time_context", "erotic"],
    # layer_variants={"personality": "sadodere", "relationship": "friend" }
)