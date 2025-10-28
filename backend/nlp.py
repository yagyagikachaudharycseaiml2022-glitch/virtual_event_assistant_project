import re
from typing import Optional, Tuple

def extract_location_tokens(text: str):
    text = text.lower()
    tokens = []
    for m in re.finditer(r'gate\s*[-]?\s*(\d+)', text):
        tokens.append(('gate', m.group(1)))
    for m in re.finditer(r'hall\s*[-]?\s*(\d+)', text):
        tokens.append(('hall', m.group(1)))
    for m in re.finditer(r'booth\s*[-]?\s*(\d+)', text):
        tokens.append(('booth', m.group(1)))
    return tokens

def parse_origin_destination(text: str) -> Tuple[Optional[str], Optional[str]]:
    lower = (text or '').lower()
    tokens = extract_location_tokens(lower)
    origin = None
    destination = None
    if ' to ' in lower or ' take me to ' in lower:
        parts = re.split(r'\bto\b', lower, maxsplit=1)
        left, right = parts[0], parts[1] if len(parts) > 1 else ''
        left_tokens = extract_location_tokens(left)
        right_tokens = extract_location_tokens(right)
        if left_tokens:
            origin = f"{left_tokens[-1][0]}-{left_tokens[-1][1]}"
        if right_tokens:
            destination = f"{right_tokens[0][0]}-{right_tokens[0][1]}"
    if not origin and tokens:
        origin = f"{tokens[0][0]}-{tokens[0][1]}"
    if not destination and len(tokens) > 1:
        destination = f"{tokens[1][0]}-{tokens[1][1]}"
    return origin, destination
