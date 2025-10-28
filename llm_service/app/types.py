from enum import Enum

class ContextRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"