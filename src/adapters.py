import asyncio
import json
import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import Callable

import aiofiles
from aiofiles import os as aios
from aiohttp import ClientSession

from src.abstract import adapters as abstract
from src.domain.model import FileInfo, Server


class WebClient(abstract.AWebClient):
    async def download_and_save_file(
        self, link: str, files_dir: Path, file_name: str, save_file_function: Callable
    ) -> FileInfo:
        """
        Downloading and saving a file in the system.

        :param files_dir: file directory path
        :param file_name: file save name
        :param link: web link to download file
        :param save_file_function: Function for saving a file to the file system.
        The algorithm for downloading and saving the file will be executed in one place
        because they implement chunks download.
        :return: information about saved file
        """
        async with ClientSession() as session:
            async with session.get(link) as resp:
                # get the file type based on the content-type
                file_type = mimetypes.guess_extension(resp.content_type)
                # If file_type is None then the value is overridden with an empty string
                file_type = file_type if file_type else ""
                file_full_name = f"{file_name}{file_type}"
                # iterator for file chunks for streaming storage
                chunk_iterator = resp.content.iter_chunks()
                # save file
                await save_file_function(files_dir, file_full_name, chunk_iterator)
                return FileInfo(name=file_name, file_type=file_type, origin_url=link)

    async def upload_file(
        self, server: Server, files_dir: Path, file_info: FileInfo
    ) -> dict:
        """
        Send a file to the server using the SSH copy command

        :param server: server info for file transfer
        :param files_dir: file directory path
        :param file_info: file information
        :return: info about the server to which the file was sent
        """
        file_name = f"{file_info.name}{file_info.file_type}"
        # running the SCP command to transfer the file
        process = await asyncio.create_subprocess_exec(
            "scp",
            "-o",
            # Exclude the interactive part of the command
            "StrictHostKeyChecking=no",
            files_dir / file_name,
            f"root@{server.ip}:files/",
        )
        # waiting for the operation to complete
        await process.wait()
        return {"server": server}

    async def send_file_status(self, origin_url: str, status: dict):
        """Send information about the file status to the server"""
        async with ClientSession() as session:
            async with session.post(f"{origin_url}/status/", data=json.dumps(status)):
                pass


class FileManager(abstract.AFileManager):
    async def save_file(self, files_dir: Path, file_name: str, chunk_iterator):
        """
        Saving the file in the system.
        Writing occurs in streaming mode to
        avoid loading the operational memory in case of uploading a large file.

        :param files_dir: file directory path
        :param file_name: file name
        :param chunk_iterator: file fragment iterator
        """
        async with aiofiles.open(files_dir / file_name, "wb") as f:
            async for chunk in chunk_iterator:
                await f.write(chunk[0])

    async def is_file_exists(self, files_dir: Path, file_name: str) -> bool:
        """Check if the file exists in the storage"""
        return await aios.path.exists(files_dir / file_name)

    async def get_old_files(self, files_dir: Path, expiring_time: int) -> list:
        """
        Get a list of files that were created earlier than now - expiring_time.
        :param files_dir: file directory path
        :param expiring_time: maximum file lifespan
        :return: List of "old" files
        that were created earlier than the specified duration
        """
        now = datetime.now()
        # all files in the directory
        file_list = [file.name for file in files_dir.iterdir() if file.is_file()]
        old_files = []
        for file in file_list:
            # last modification time
            mtime = await aios.path.getmtime(files_dir / file)
            mtime = datetime.fromtimestamp(mtime)
            if (now - mtime).seconds >= expiring_time:
                old_files.append(file)
        # remove the special git file from the list
        old_files.remove(".gitkeep")
        return old_files

    async def delete_files(self, files_dir: Path, files: list[str]):
        """Deleted the list of files"""
        for file in files:
            await aios.remove(files_dir / file)


class EnvManager(abstract.AEnvManager):
    async def get(self, key: str) -> str:
        return os.environ.get(key)


class ServersManager(abstract.AServersManager):
    async def get_servers(self, root_dir: Path) -> list[Server]:
        """Get a list of servers from a JSON file."""
        # If it's in test mode, return the test server.
        test_mode = os.environ.get("TEST") == "TRUE"
        servers_file = "servers_test.json" if test_mode else "servers.json"
        with open(root_dir / servers_file) as f:
            servers = json.load(f)
        return [Server(s["name"], s["ip"], s["zone"]) for s in servers]
