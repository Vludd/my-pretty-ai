from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field

class LayerType(str, Enum):
    Default = "default"
    Selectable = "selectable"

@dataclass
class LayerOption:
    name: str
    description: Optional[str]
    prompt: List[str] = field(default_factory=list)

@dataclass
class BaseLayer:
    type: LayerType
    name: str

@dataclass
class DefaultLayer(BaseLayer):
    prompt: List[str] = field(default_factory=list)

@dataclass
class LayerWithOptions(BaseLayer):
    additional: Optional[str] = None
    options: List[LayerOption] = field(default_factory=list)
