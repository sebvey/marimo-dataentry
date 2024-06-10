from dataclasses import dataclass

@dataclass
class UIFile:
    name: str
    contents: bytes

__all__ = [
    UIFile
]
