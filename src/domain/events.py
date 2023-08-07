from dataclasses import dataclass
from datetime import datetime

from src.domain.model import FileInfo, Server


class Event:
    pass


@dataclass
class FileSavedEvent(Event):
    file: FileInfo


@dataclass
class FileReplicatedEvent(Event):
    file: FileInfo
    server: Server
    duration: int
    time: datetime
