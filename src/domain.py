from dataclasses import dataclass


@dataclass
class File:
    file_type: str
    file_content: bytes
