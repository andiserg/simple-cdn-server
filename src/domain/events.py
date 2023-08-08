from dataclasses import dataclass
from datetime import datetime

from src.domain.model import FileInfo, Server


class Event:
    pass


@dataclass
class FileProcessedEvent(Event):
    file_info: FileInfo
    duration: int
    time: datetime


@dataclass
class FileSavedEvent(FileProcessedEvent):
    pass


@dataclass
class FileReplicatedEvent(FileProcessedEvent):
    server: Server
