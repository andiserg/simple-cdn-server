from pathlib import Path

from src.abstract import adapters as abstract
from src.domain.model import File, Server


class FakeWebClient(abstract.AWebClient):
    async def download_file(self, link: str) -> File:
        return File(content=b"Hello world", file_type="txt", name="test")

    async def upload_file(self, server: Server, file: File, test: bool = False):
        return {"server": Server, "file": file}


class FakeFileManager(abstract.AFileManager):
    async def save_file(self, files_dir, file: File):
        return f"{file.name}.{file.file_type}"

    async def delete_file(self, files_dir, file_name: str):
        pass

    async def is_file_exists(self, file_dir: Path, file_name: str) -> bool:
        return False


class FakeEnvManager(abstract.AEnvManager):
    async def get(self, key: str) -> str:
        pass


class FakeServersManager(abstract.AServersManager):
    async def get_servers(self, root_dir: Path) -> list[Server]:
        return [Server(name="TestVPS", ip="test", zone="test_zone")]
