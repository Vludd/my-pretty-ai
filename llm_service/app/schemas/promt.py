from enum import Enum

class LayerType(str, Enum):
    Default = "default"
    Selective = "selective"

class LayerOption:
    name: str
    description: str | None
    prompt: list[str]

class BaseLayer:
    type: str
    name: str
    
class DefaultLayer(BaseLayer):
    prompt: list[str]

class LayerWithOptions(BaseLayer):
    additional: str | None
    options: list[LayerOption]
