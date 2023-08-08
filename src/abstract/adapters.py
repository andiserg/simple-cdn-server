from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncIterable, Callable

from src.domain.model import FileInfo, Server


class AWebClient(ABC):
    @abstractmethod
    async def download_and_save_file(
        self, link: str, files_dir: Path, file_name: str, save_file_function: Callable
    ) -> FileInfo:
        pass

    @abstractmethod
    async def upload_file(
        self, server: Server, file_info: FileInfo, chunk_iterator: AsyncIterable
    ):
        pass

    @abstractmethod
    async def send_file_status(self, origin_url: str, status: dict):
        pass


class AFileManager(ABC):
    @abstractmethod
    async def save_file(self, files_dir, file_name: str, chunk_iterator: AsyncIterable):
        pass

    @abstractmethod
    async def get_chunk_iterator_factory(self, path: Path, chunk_size: int) -> Callable:
        pass

    @abstractmethod
    async def is_file_exists(self, file_dir: Path, file_name: str) -> bool:
        pass

    @abstractmethod
    async def get_old_files(self, files_dir: Path, expiring_time: int):
        pass

    @abstractmethod
    async def delete_files(self, files_dir: Path, files: list[str]):
        pass


class AEnvManager(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        pass


class AServersManager(ABC):
    @abstractmethod
    async def get_servers(self, root_dir: Path) -> list[Server]:
        pass
