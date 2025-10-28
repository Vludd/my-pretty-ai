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
            
            # New layer
            if stripped.startswith("# Layer:"):
                # Saving prev layer
                if current_layer is not None:
                    self._save_layer(current_layer, layer_content, variants)
                
                current_layer = stripped.split(":", 1)[1].strip()
                logger.debug(f"Reading layer: '{current_layer}'")
                layer_content = []
                variants = {}
                current_variant = None
            
            # Variant in layer (example, @tsundere:)
            elif stripped.startswith("@") and ":" in stripped and current_layer:
                # Saving prev variant
                if current_variant is not None:
                    variants[current_variant] = "\n".join(layer_content).strip()
                    layer_content = []
                
                # Export variant name (between @ and :)
                current_variant = stripped[1:].split(":", 1)[0].strip()
                
                logger.debug(f"  Reading variant: '{current_variant}'")
            
            else:
                layer_content.append(line)
        
        # Saving last layer
        if current_layer is not None:
            self._save_layer(current_layer, layer_content, variants)

    def _save_layer(self, layer_name: str, content: List[str], variants: Dict[str, str]):
        """Saves the layer with its variants"""
        # If variants exists then saving last
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
            # Default layer without variants
            self.layers[layer_name] = {
                "type": "simple",
                "content": "\n".join(content).strip()
            }
            logger.debug(f"Saved simple layer '{layer_name}'")

    def get_combined_prompt(
        self, 
        layers_order: Optional[List[str]] = None,
        variants: Optional[Dict[str, str]] = None,
        randomized_variant: bool = False            # In Dev
    ) -> str:
        """
        Collects the prompt from the specified layers and variants.
        
        Args:
            layers_order: list of layers in the desired order. If None, all are taken.
            variants: {layer_name: variant_name} dictionary for selecting specific variants
        
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
                # Simple layer
                parts.append(f"# Layer: {layer}")
                parts.append(layer_data["content"])
            
            elif layer_data["type"] == "variants":
                # Layer with variants
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
                    # If the option is not specified, we take all the variants
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
        """Returns a list of available layers"""
        return list(self.layers.keys())

    def get_layer_variants(self, layer_name: str) -> Optional[List[str]]:
        """Returns a list of options for the layer, if any"""
        if layer_name not in self.layers:
            return None
        
        layer_data = self.layers[layer_name]
        if layer_data["type"] == "variants":
            return list(layer_data["variants"].keys())
        
        return None

    def get_layer_info(self) -> Dict[str, Any]:
        """Returns information about all layers"""
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