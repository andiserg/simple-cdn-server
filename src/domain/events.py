from dataclasses import dataclass

from src.domain.model import File, Server


@dataclass
class FileDownloadedEvent:
    file: File


@dataclass
class FileReplicatedEvent:
    file: File
    server: Server
