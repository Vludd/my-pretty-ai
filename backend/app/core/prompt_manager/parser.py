from app.models.prompt import MPrompt
from app.schemas.prompt import DefaultLayer, LayerWithOptions
from app.utils.logger import logger
from app.utils.dict_converter import dict_to_layer, dict_to_option

def build_system_context(prompt: MPrompt) -> dict:
    system_prompt: str = ""
    skipped_layers: int = 0
    skipped_options: int = 0
    
    raw_layers = prompt.layers
    
    if not raw_layers: # type: ignore
        logger.error(f"Prompt <{prompt.id}> doesn't have layers!")
        return {"role": "system", "content": ""}
        
    layers = [dict_to_layer(l) for l in raw_layers] # type: ignore
    
    logger.debug("Collecting prompt...")
    for l in layers:
        if not l.name:
            logger.warning(f"Skipping unknown layer without name...")
            skipped_layers += 1
            continue
            
        if not l.enabled:
            logger.warning(f"Skipping disabled layer {l.name}...")
            skipped_layers += 1
            continue
        
        logger.debug(f"Collecting '{l.name}' [{l.type}] layer...")
        if isinstance(l, DefaultLayer):
            if not l.prompt:
                logger.warning(f"Skipping layer {l.name} without prompt data...")
                skipped_layers += 1
                continue
            
            system_prompt += f"### {l.name}:\n"
            system_prompt += l.prompt
            system_prompt += "\n\n"
            
        elif isinstance(l, LayerWithOptions):
            if not l.options:
                logger.warning(f"Skipping layer {l.name} without options...")
                skipped_layers += 1
                continue
            
            system_prompt += f"### {l.name}:\n"
            
            if l.additional:
                system_prompt += f"*{l.additional}*\n"
            
            raw_options = l.options
            options = [dict_to_option(o) for o in raw_options] # type: ignore
            
            for o in options:
                if not o.name:
                    logger.warning(f"Skipping unknown option without name...")
                    skipped_options += 1
                    continue
                
                if not o.prompt:
                    logger.warning(f"Skipping option {o.name} without prompt data...")
                    skipped_options += 1
                    continue
                
                if o.selected:
                    system_prompt += f"@{o.name}:\n"
                    
                    if o.description:
                        system_prompt += f"*{o.description}*\n"
                        
                    system_prompt += o.prompt
                    system_prompt += "\n\n"
                    
                    if not l.multiple:
                        break
                    
        logger.debug(f"Layer '{l.name}' [{l.type}] collected!")
        
    logger.debug(f"Prompt collected! Skipped Layers: {skipped_layers}. Skipped Options: {skipped_options}")
    system_prompt_context = {"role": "system", "content": system_prompt}
    return system_prompt_context
