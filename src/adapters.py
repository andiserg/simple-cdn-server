import json
import os
from pathlib import Path

import aiofiles
from aiofiles import os as aios
from aiohttp import ClientSession

from src.abstract import adapters as abstract
from src.domain.model import File, Server


class WebClient(abstract.AWebClient):
    async def download_file(self, link: str) -> File:
        async with ClientSession() as session:
            async with session.get(link) as resp:
                file_type = resp.content_type.split("/")[1]
                return File(file_type, await resp.read())

    async def upload_file(self, server: Server, file: File, test: bool = False) -> dict:
        async with ClientSession() as session:
            data = {"content": file.content, "name": file.name, "type": file.file_type}
            async with session.post(f"http://{server.ip}:8080", data=data) as resp:
                return {"server": server, "status": resp.status}


class FileManager(abstract.AFileManager):
    async def save_file(self, files_dir: Path, file: File) -> str:
        """
        Saving the file in the system.
        :param files_dir: dir of files
        :param file: bytes
        :return: file name
        """
        async with aiofiles.open(
            files_dir / f"{file.name}.{file.file_type}", "wb"
        ) as f:
            await f.write(file.content)
            return f"{file.name}.{file.file_type}"

    async def delete_file(self, files_dir: Path, file_name: str):
        await aios.remove(files_dir / file_name)

    async def is_file_exists(self, files_dir: Path, file_name: str) -> bool:
        return await aios.path.exists(files_dir / file_name)


class EnvManager(abstract.AEnvManager):
    async def get(self, key: str) -> str:
        return os.environ.get(key)


class ServersManager(abstract.AServersManager):
    async def get_servers(self, root_dir: Path) -> list[Server]:
        with open(root_dir / "servers.json") as f:
            servers = json.load(f)
        return [
            Server(server["name"], server["ip"], server["zone"]) for server in servers
        ]
