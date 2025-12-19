import secrets
import string

KEYS_COUNT_MIN = 4
KEYS_COUNT_DEFAULT = 6
KEYS_COUNT_MAX = 10

KEY_LENGTH = 16
GROUP_SIZE = 4   # MPA1-XXXX-XXXX-XXXX

PREFIX = "MPA1"
EXCLUDED = {"I", "O", "0", "1"}

ALPHABET = ''.join(
    c for c in (string.ascii_uppercase + string.digits)
    if c not in EXCLUDED
)

def _generate_single_key() -> str:
    raw = ''.join(secrets.choice(ALPHABET) for _ in range(KEY_LENGTH))
    groups = [raw[i:i + GROUP_SIZE] for i in range(0, KEY_LENGTH, GROUP_SIZE)]
    return f"{PREFIX}-" + "-".join(groups)

def generate_recovery_keys(count: int = KEYS_COUNT_DEFAULT) -> list[str]:
    if not (KEYS_COUNT_MIN <= count <= KEYS_COUNT_MAX):
        raise ValueError("Invalid recovery keys count")
    return [_generate_single_key() for _ in range(count)]
