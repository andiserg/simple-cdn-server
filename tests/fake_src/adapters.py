from pathlib import Path
from typing import AsyncIterable, Callable

from src.abstract import adapters as abstract
from src.domain.model import FileInfo, Server


class FakeWebClient(abstract.AWebClient):
    async def download_and_save_file(
        self, link: str, files_dir: Path, file_name: str, save_file_function: Callable
    ) -> FileInfo:
        return FileInfo(name="test", file_type="txt", origin_url="test")

    async def upload_file(
        self, server: Server, file_info: FileInfo, chunk_iterator: AsyncIterable
    ):
        return {"server": Server, "status": 200}

    async def send_file_status(self, origin_url: str, status: dict):
        pass


class FakeFileManager(abstract.AFileManager):
    async def save_file(
        self, files_dir: Path, file_name: str, chunk_iterator: AsyncIterable
    ):
        pass

    async def get_chunk_iterator(self, path: Path, chunk_size: int) -> AsyncIterable:
        pass

    async def delete_file(self, files_dir, file_name: str):
        pass

    async def is_file_exists(self, file_dir: Path, file_name: str) -> bool:
        return False


class FakeEnvManager(abstract.AEnvManager):
    async def get(self, key: str) -> str:
        if key == "CHUNK_SIZE":
            return "10"


class FakeServersManager(abstract.AServersManager):
    async def get_servers(self, root_dir: Path) -> list[Server]:
        return [Server(name="TestVPS", ip="test", zone="test_zone")]
