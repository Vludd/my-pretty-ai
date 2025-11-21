from datetime import datetime
from typing import List, Optional, Union
from dataclasses import dataclass, field

from pydantic import Field
from uuid import UUID

from app.schemas import BaseConfig

from app.types.prompt import LayerType
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class LayerOption:
    name: str
    description: Optional[str]
    prompt: str
    selected: bool

@dataclass
class BaseLayer:
    type: LayerType
    name: str
    enabled: bool

@dataclass
class DefaultLayer(BaseLayer):
    prompt: str

@dataclass
class LayerWithOptions(BaseLayer):
    multiple: bool = False
    additional: Optional[str] = None
    options: List[LayerOption] = field(default_factory=list)
    
@dataclass
class PromptData:
    name: str
    layers: List[Union[DefaultLayer, LayerWithOptions]]
    is_default: bool = False
    
default_layer_example = DefaultLayer(
    type=LayerType.DEFAULT,
    name="about",
    enabled=True,
    prompt="some prompt"
)

layer_with_options_example = LayerWithOptions(
    type=LayerType.SELECTABLE,
    name="relationship",
    additional="",
    enabled=True,
    multiple=False,
    options=[
        LayerOption(name="option 1", description="", prompt="active prompt", selected=True),
        LayerOption(name="option 2", description="", prompt="inactive prompt", selected=False)
    ]
)

class SPromptCreate(BaseConfig):
    name: str = Field(..., min_length=1, max_length=50, examples=["Example prompt"])
    layers: List[Union[DefaultLayer, LayerWithOptions]] = Field(..., examples=[[
        default_layer_example, layer_with_options_example
    ]])

class SPromptUpdate(BaseConfig):
    name: Optional[str] = None
    layers: Optional[List[Union[DefaultLayer, LayerWithOptions]]] = None
        
class SPromptRead(BaseConfig):
    public_id: UUID
    name: str
    layers: List[Union[DefaultLayer, LayerWithOptions]]
    is_default: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
