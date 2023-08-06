from dataclasses import dataclass


@dataclass
class File:
    file_type: str
    content: bytes
    name: str | None = None


@dataclass
class Server:
    name: str
    ip: str
    zone: str
