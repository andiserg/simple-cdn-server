from abc import ABC, abstractmethod
from pathlib import Path

from src.domain import File, Server


class AWebClient(ABC):
    @abstractmethod
    async def download_file(self, link: str):
        pass

    @abstractmethod
    async def upload_file(self, server: Server, file: File, test: bool = False):
        pass


class AFileManager(ABC):
    @abstractmethod
    async def save_file(self, files_dir, file: File):
        pass

    @abstractmethod
    async def delete_file(self, files_dir, file_name: str):
        pass


class AEnvManager(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        pass


class AServersManager(ABC):
    @abstractmethod
    async def get_servers(self, root_dir: Path) -> list[Server]:
        pass
