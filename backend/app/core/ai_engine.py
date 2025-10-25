from typing import Dict, List, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

import torch
from pathlib import Path

from app.data.configs.llm_config_schema import SLLMConfig
from app.schemas.llm import SContextMessage
from app.core.prompt_manager import PromptLayerManager

from app.utils.logger import logger

class LLMEngine:
    def __init__(
        self, 
        llm_config: SLLMConfig, 
        layers_order: Optional[List[str]] = None,
        layer_variants: Optional[Dict[str, str]] = None
    ) -> None:
        self.llm_config = llm_config
        self.messages: List[Dict[str, str]] = []
        
        logger.info("Initializaion LLMEngine...")
        
        prompt_manager = PromptLayerManager()
        
        layer_info = prompt_manager.get_layer_info()
        logger.debug(f"Available layers: {list(layer_info.keys())}")
        for layer_name, info in layer_info.items():
            if info["type"] == "variants":
                logger.debug(f"  {layer_name}: {info['variants']}")
                
        system_prompt = prompt_manager.get_combined_prompt(
            layers_order=layers_order,
            variants=layer_variants
        )
        # system_prompt = prompt_manager.get_combined_prompt(layers_order)
        
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_prompt += f"\n\nCurrent time: {current_time}"
        
        logger.debug(f"Datetime now: {current_time}")

        self.system_prompt = system_prompt
        self.messages.append({"role": "system", "content": self.system_prompt})

        # Конфигурация квантизации
        bnb_cfg = None
        if llm_config.quantization_config and llm_config.quantization_config.load_in_4bit:
            bnb_cfg = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=llm_config.quantization_config.bnb_4bit_compute_dtype,
                bnb_4bit_use_double_quant=llm_config.quantization_config.bnb_4bit_use_double_quant,
                bnb_4bit_quant_type=llm_config.quantization_config.bnb_4bit_quant_type,
            )

        # Загрузка модели
        self.model = AutoModelForCausalLM.from_pretrained(
            llm_config.model_name,
            local_files_only=True,
            quantization_config=bnb_cfg,
            device_map=llm_config.device_map,
            max_memory=llm_config.max_memory,
            dtype=llm_config.dtype,
            low_cpu_mem_usage=llm_config.low_cpu_mem_usage,
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(llm_config.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def update_system_prompt(
        self,
        layers_order: Optional[List[str]] = None,
        layer_variants: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Обновляет системный промпт с новыми слоями/вариантами.
        Полезно для динамического изменения личности/отношений в процессе работы.
        """
        prompt_manager = PromptLayerManager()
        system_prompt = prompt_manager.get_combined_prompt(
            layers_order=layers_order,
            variants=layer_variants
        )
        
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_prompt += f"\n\nCurrent time: {current_time}"
        
        self.system_prompt = system_prompt
        
        # Обновляем первое сообщение (system)
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = self.system_prompt
            logger.info("System prompt updated")
        else:
            self.messages.insert(0, {"role": "system", "content": self.system_prompt})
            logger.info("System prompt added")
    
    async def load_conversation(self, context: list[SContextMessage]):
        self.messages = [{"role": "system", "content": self.system_prompt}]
        
        logger.debug(f"Loading context... {len(context)} messages")
        for m in context:
            context_item = {"role": m.role.value, "content": m.content}
            self.messages.append(context_item)
            logger.debug(f"Loaded: {context_item}")
            
    async def generate(self, text: str):
        self.messages.append({"role": "user", "content": text})

        prompt = self.tokenizer.apply_chat_template(
            self.messages,
            tokenize=False,
            add_generation_prompt=True
        )

        input_tokenized = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        input_ids = input_tokenized["input_ids"]
        input_tokens = input_ids.shape[1]
        
        input_len = input_tokens

        gen_cfg = self.llm_config.generation_config
        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=input_tokenized.get("attention_mask"),
                max_new_tokens=gen_cfg.max_new_tokens,
                temperature=gen_cfg.temperature,
                top_p=gen_cfg.top_p,
                do_sample=gen_cfg.do_sample,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=getattr(self.tokenizer, "eos_token_id", None),
                use_cache=gen_cfg.use_cache,
            )

        reply_ids = output_ids[0, input_len:]
        output_tokens = reply_ids.shape[0]
        
        reply = self.tokenizer.decode(reply_ids, skip_special_tokens=True).strip()
        self.messages.append({"role": "assistant", "content": reply})
        
        total_context_tokens = input_tokens + output_tokens
        max_context = self.model.config.max_position_embeddings
        tokens_left = max_context - total_context_tokens
        
        logger.debug(
            f"Usage:\n"
            f"  Input: {input_tokens}\n"
            f"  Output: {output_tokens}\n"
            f"  Total: {total_context_tokens}\n"
            f"  Remaining: {tokens_left}\n"
            f"  MaxContext: {max_context}"
        )
        
        torch.cuda.empty_cache()
        
        return {
            "reply": reply,
            "usage": {
                "input": input_tokens,
                "output": output_tokens,
                "total": total_context_tokens,
                "remaining": tokens_left,
                "max": max_context
            }
        }
