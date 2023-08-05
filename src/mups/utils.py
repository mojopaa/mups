import re


def normalize_name(name: str, lowercase: bool = True) -> str:
    name = re.sub(r"[^A-Za-z0-9]+", "-", name)
    return name.lower() if lowercase else name
