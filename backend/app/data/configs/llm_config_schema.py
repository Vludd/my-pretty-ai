import torch
from pydantic import BaseModel

from typing import ClassVar

class SQuantizationConfig(BaseModel):
    load_in_4bit: bool = True
    bnb_4bit_compute_dtype: ClassVar[torch.dtype] = torch.float16
    bnb_4bit_use_double_quant: bool = True
    bnb_4bit_quant_type: str = "nf4"
    
class SGenerationConfig(BaseModel):
    max_new_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    do_sample: bool = True
    use_cache: bool = True

class SLLMConfig(BaseModel):
    model_name: str = "Qwen/Qwen3-4B-Instruct-2507"
    device_map: str = "auto"
    dtype: str = "auto"
    max_memory: dict = {0: "7GiB", "cpu": "30GiB"}
    low_cpu_mem_usage: bool = True
    system_prompt: str = "system_prompt.txt"
    quantization_config: SQuantizationConfig = SQuantizationConfig()
    generation_config: SGenerationConfig = SGenerationConfig()
