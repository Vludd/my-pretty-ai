from pathlib import Path
from typing import Dict, List, Optional, Any
from app.utils.logger import logger

SYSTEM_PROMPT_FILENAME = "prompt.md"

PROMPT_DIR = Path(__file__).resolve().parent.parent / "data/prompts"
SYSTEM_PROMPT_PATH = f"{PROMPT_DIR}/{SYSTEM_PROMPT_FILENAME}"

class PromptLayerManager:
    def __init__(self):
        self.file_path = Path(SYSTEM_PROMPT_PATH)
        self.layers: Dict[str, Dict[str, Any]] = {}
        self._parse_file()

    def _parse_file(self):
        logger.debug(f"Reading prompt from {self.file_path}...")
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {self.file_path}")
        
        logger.debug(f"Reading {self.file_path}...")

        current_layer = None
        current_variant = None
        layer_content = []
        variants = {}
        
        for line in self.file_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            
            # Новый слой
            if stripped.startswith("# Layer:"):
                # Сохраняем предыдущий слой
                if current_layer is not None:
                    self._save_layer(current_layer, layer_content, variants)
                
                current_layer = stripped.split(":", 1)[1].strip()
                logger.debug(f"Reading layer: '{current_layer}'")
                layer_content = []
                variants = {}
                current_variant = None
            
            # Вариант внутри слоя (например, @tsundere:)
            elif stripped.startswith("@") and ":" in stripped and current_layer:
                # Сохраняем предыдущий вариант
                if current_variant is not None:
                    variants[current_variant] = "\n".join(layer_content).strip()
                    layer_content = []
                
                # Извлекаем название варианта (между @ и :)
                current_variant = stripped[1:].split(":", 1)[0].strip()
                
                logger.debug(f"  Reading variant: '{current_variant}'")
            
            else:
                layer_content.append(line)
        
        # Сохраняем последний слой
        if current_layer is not None:
            self._save_layer(current_layer, layer_content, variants)

    def _save_layer(self, layer_name: str, content: List[str], variants: Dict[str, str]):
        """Сохраняет слой с его вариантами"""
        # Если есть варианты, сохраняем последний
        if variants:
            if content:
                last_variant = list(variants.keys())[-1] if variants else None
                if last_variant:
                    variants[last_variant] = "\n".join(content).strip()
            
            self.layers[layer_name] = {
                "type": "variants",
                "variants": variants
            }
            logger.debug(f"Saved layer '{layer_name}' with {len(variants)} variants: {list(variants.keys())}")
        else:
            # Обычный слой без вариантов
            self.layers[layer_name] = {
                "type": "simple",
                "content": "\n".join(content).strip()
            }
            logger.debug(f"Saved simple layer '{layer_name}'")

    def get_combined_prompt(
        self, 
        layers_order: Optional[List[str]] = None,
        variants: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Собирает промпт из указанных слоёв и вариантов.
        
        Args:
            layers_order: список слоёв в нужном порядке. Если None, берутся все.
            variants: словарь {layer_name: variant_name} для выбора конкретных вариантов
        
        Example:
            get_combined_prompt(
                layers_order=["system", "about", "personality", "relationship"],
                variants={
                    "personality": "tsundere",
                    "relationship": "dating"
                }
            )
        """
        if layers_order is None:
            layers_order = list(self.layers.keys())
        
        if variants is None:
            variants = {}
        
        parts = []
        
        for layer in layers_order:
            if layer not in self.layers:
                logger.warning(f"Layer '{layer}' not found, skipping")
                continue
            
            layer_data = self.layers[layer]
            
            if layer_data["type"] == "simple":
                # Простой слой
                parts.append(f"# Layer: {layer}")
                parts.append(layer_data["content"])
            
            elif layer_data["type"] == "variants":
                # Слой с вариантами
                variant_name = variants.get(layer)
                
                if variant_name:
                    if variant_name in layer_data["variants"]:
                        parts.append(f"# Layer: {layer} [{variant_name}]")
                        parts.append(layer_data["variants"][variant_name])
                        logger.debug(f"Using variant '{variant_name}' for layer '{layer}'")
                    else:
                        available = list(layer_data["variants"].keys())
                        logger.warning(
                            f"Variant '{variant_name}' not found in layer '{layer}'. "
                            f"Available: {available}"
                        )
                else:
                    # Если вариант не указан, берём все варианты
                    parts.append(f"# Layer: {layer}")
                    for var_name, var_content in layer_data["variants"].items():
                        parts.append(f"\n@{var_name}:")
                        parts.append(var_content)
        
        combined_prompt = "\n\n".join(parts)
        
        logger.debug(f"Final prompt length: {len(combined_prompt)} chars")
        logger.debug(f"Layers used: {layers_order}")
        logger.debug(f"Variants selected: {variants}")
        logger.debug(f"Prompt contents: {combined_prompt}")
        
        return combined_prompt

    def get_available_layers(self) -> List[str]:
        """Возвращает список доступных слоёв"""
        return list(self.layers.keys())

    def get_layer_variants(self, layer_name: str) -> Optional[List[str]]:
        """Возвращает список вариантов для слоя, если они есть"""
        if layer_name not in self.layers:
            return None
        
        layer_data = self.layers[layer_name]
        if layer_data["type"] == "variants":
            return list(layer_data["variants"].keys())
        
        return None

    def get_layer_info(self) -> Dict[str, Any]:
        """Возвращает информацию о всех слоях"""
        info = {}
        for layer_name, layer_data in self.layers.items():
            if layer_data["type"] == "simple":
                info[layer_name] = {"type": "simple"}
            else:
                info[layer_name] = {
                    "type": "variants",
                    "variants": list(layer_data["variants"].keys())
                }
        return info