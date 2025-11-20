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

@dataclass
class BaseLayer:
    type: LayerType
    name: str

@dataclass
class DefaultLayer(BaseLayer):
    prompt: str

@dataclass
class LayerWithOptions(BaseLayer):
    additional: Optional[str] = None
    options: List[LayerOption] = field(default_factory=list)

class SPromptCreate(BaseConfig):
    name: str = Field(..., min_length=1, max_length=50, examples=["Example prompt"])
    layers: List[Union[DefaultLayer, LayerWithOptions]] = Field(..., examples=[[{"type": LayerType.DEFAULT, "name": "about", "prompt": "some prompt"}]])

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
