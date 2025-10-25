from pydantic import BaseModel, ConfigDict

class BaseConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# class SMessageResponse(BaseModel):
#     detail: str
    
# class SErrorResponse(BaseModel):
#     detail: str