from dataclasses import dataclass
from datetime import datetime

from src.domain.model import File, Server


class Event:
    pass


@dataclass
class FileSavedEvent(Event):
    file: File


@dataclass
class FileReplicatedEvent(Event):
    file: File
    server: Server
    duration: int
    time: datetime
