from dataclasses import dataclass

from src.domain.model import File, Server


class Event:
    pass


@dataclass
class FileDownloadedEvent(Event):
    file: File


@dataclass
class FileReplicatedEvent(Event):
    file: File
    server: Server
