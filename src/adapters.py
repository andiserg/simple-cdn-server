import json
import os
from datetime import datetime
from pathlib import Path
from typing import AsyncIterable, Callable

import aiofiles
from aiofiles import os as aios
from aiohttp import ClientSession

from src.abstract import adapters as abstract
from src.domain.model import FileInfo, Server


class WebClient(abstract.AWebClient):
    async def download_and_save_file(
        self, link: str, files_dir: Path, file_name: str, save_file_function: Callable
    ) -> FileInfo:
        async with ClientSession() as session:
            async with session.get(link) as resp:
                file_type = resp.content_type.split("/")[1]
                file_type = file_type if file_type != "octet-stream" else "bin"
                file_full_name = f"{file_name}.{file_type}"
                chunk_iterator = resp.content.iter_chunks()
                # Saving file
                await save_file_function(files_dir, file_full_name, chunk_iterator)
                return FileInfo(name=file_name, file_type=file_type, origin_url=link)

    async def upload_file(
        self, server: Server, file_info: FileInfo, chunk_iterator
    ) -> dict:
        headers = {"FILE_NAME": f"{file_info.name}.{file_info.file_type}"}
        async with ClientSession(headers=headers) as session:
            async with session.put(f"{server.url}/files/", data=chunk_iterator) as resp:
                return {"server": server, "status": resp.status}

    async def send_file_status(self, origin_url: str, status: dict):
        async with ClientSession() as session:
            async with session.post(f"{origin_url}/status/", data=json.dumps(status)):
                pass


class FileManager(abstract.AFileManager):
    async def save_file(
        self, files_dir: Path, file_name: str, chunk_iterator: AsyncIterable
    ):
        """
        Saving the file in the system.
        :param files_dir: dir of files
        :param file_name: file name
        :param chunk_iterator: file fragment iterator
        """
        async with aiofiles.open(files_dir / file_name, "wb") as f:
            async for chunk in chunk_iterator:
                await f.write(chunk[0])

    async def get_chunk_iterator(self, path: Path, chunk_size: int):
        async with aiofiles.open(path, "rb") as f:
            chunk = await f.read(chunk_size * 1024)
            while chunk:
                yield chunk
                chunk = await f.read(64 * 1024)

    async def is_file_exists(self, files_dir: Path, file_name: str) -> bool:
        return await aios.path.exists(files_dir / file_name)

    async def get_old_files(self, files_dir: Path, expiring_time: int) -> list:
        now = datetime.now()
        file_list = [file.name for file in files_dir.iterdir() if file.is_file()]
        old_files = []
        for file in file_list:
            if file == ".gitkeep":
                continue
            last_change_time = datetime.fromtimestamp(
                await aios.path.getmtime(files_dir / file)
            )
            if (now - last_change_time).seconds >= expiring_time:
                old_files.append(file)
        return old_files

    async def delete_files(self, files_dir: Path, files: list[str]):
        for file in files:
            await aios.remove(files_dir / file)


class EnvManager(abstract.AEnvManager):
    async def get(self, key: str) -> str:
        return os.environ.get(key)


class ServersManager(abstract.AServersManager):
    async def get_servers(self, root_dir: Path) -> list[Server]:
        servers_file = (
            "servers_test.json" if os.environ.get("TEST") == "TRUE" else "servers.json"
        )
        with open(root_dir / servers_file) as f:
            servers = json.load(f)
        return [
            Server(server["name"], server["url"], server["zone"]) for server in servers
        ]
