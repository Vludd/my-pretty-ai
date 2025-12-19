import re

RECOVERY_KEY_REGEX = re.compile(
    r"^MPA1(?:-[A-Z2-9]{4}){4}$"
)

def is_valid_recovery_key(key: str) -> bool:
    return bool(RECOVERY_KEY_REGEX.fullmatch(key))
