from abc import ABC, abstractmethod

from src.domain import File


class AWebClient(ABC):
    @abstractmethod
    async def download_file(self, link: str):
        pass


class AFileManager(ABC):
    @abstractmethod
    async def save_file(self, files_dir, file: File, name: str):
        pass

    @abstractmethod
    async def delete_file(self, files_dir, file_name: str):
        pass


class AEnvManager(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        pass
