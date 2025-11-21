from app.schemas.prompt import DefaultLayer, LayerOption, LayerWithOptions
from app.types.prompt import LayerType

def dict_to_layer(data: dict):
    layer_type = data.get("type")

    if layer_type == LayerType.DEFAULT:
        return DefaultLayer(**data)
    
    if layer_type == LayerType.SELECTABLE:
        return LayerWithOptions(**data)

    raise ValueError(f"Unknown layer type: {layer_type}")

def dict_to_option(data: dict):
    return LayerOption(**data)
