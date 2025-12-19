from app.schemas import BaseConfig


class SAccessToken(BaseConfig):
    access_token: str
    token_type: str = "bearer"
