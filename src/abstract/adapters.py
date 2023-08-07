from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncIterable, Callable

from src.domain.model import FileInfo, ReplicatedFileStatus, Server


class AWebClient(ABC):
    @abstractmethod
    async def download_and_save_file(
        self, link: str, files_dir: Path, file_name: str, save_file_function: Callable
    ):
        pass

    @abstractmethod
    async def upload_file(self, server: Server, file: FileInfo, test: bool = False):
        pass

    @abstractmethod
    async def send_file_status(self, origin_url: str, status: ReplicatedFileStatus):
        pass


class AFileManager(ABC):
    @abstractmethod
    async def save_file(self, files_dir, file_name: str, chunk_iterator: AsyncIterable):
        pass

    @abstractmethod
    async def delete_file(self, files_dir, file_name: str):
        pass

    @abstractmethod
    async def is_file_exists(self, file_dir: Path, file_name: str) -> bool:
        pass


class AEnvManager(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        pass


class AServersManager(ABC):
    @abstractmethod
    async def get_servers(self, root_dir: Path) -> list[Server]:
        pass
