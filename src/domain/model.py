from dataclasses import dataclass


@dataclass
class FileInfo:
    file_type: str
    origin_url: str
    name: str | None = None


@dataclass
class Server:
    name: str
    url: str
    zone: str
