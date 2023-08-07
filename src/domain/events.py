from dataclasses import dataclass
from datetime import datetime
from typing import AsyncIterable

from src.domain.model import FileInfo, Server


class Event:
    pass


@dataclass
class FileSavedEvent(Event):
    file_info: FileInfo
    chunk_iterator: AsyncIterable


@dataclass
class FileReplicatedEvent(Event):
    file: FileInfo
    server: Server
    duration: int
    time: datetime
