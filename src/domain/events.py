from dataclasses import dataclass
from datetime import datetime
from typing import AsyncIterable

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
    chunk_iterator: AsyncIterable


@dataclass
class FileReplicatedEvent(FileProcessedEvent):
    server: Server
