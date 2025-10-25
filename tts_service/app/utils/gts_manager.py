import re
from typing import List, Tuple

def parse_emotion_text(text: str) -> List[Tuple[str, str]]:
    pattern = r"\[([a-zA-Z_]+)\]"
    parts = []
    last_idx = 0
    current_emotion = "neutral"

    for match in re.finditer(pattern, text):
        start, end = match.span()
        if start > last_idx:
            fragment = text[last_idx:start].strip()
            if fragment:
                parts.append((current_emotion, fragment))
        current_emotion = match.group(1).lower()
        last_idx = end

    if last_idx < len(text):
        fragment = text[last_idx:].strip()
        if fragment:
            parts.append((current_emotion, fragment))

    return parts