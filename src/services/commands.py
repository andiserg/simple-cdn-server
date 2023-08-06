import asyncio

from src.context import Context
from src.domain.model import File


async def download_file(context: Context, link: str) -> File:
    """
    Downloading a file from the link.
    :param context: Context instance
    :param link: link to the file
    :return: File instance
    """
    return await context.web.download_file(link)


async def save_file(context: Context, file: File) -> str:
    """
    Saving the file in the system and returning its name.
    :param context: Context instance
    :param file: bytes
    :return: file name
    """
    return await context.files.save_file(context.FILES_DIR, file)


async def replication_file(context: Context, file: File):
    """
    Replication saved file to servers
    :param context: Context instance
    :param file: saved File instance
    """
    servers = await context.servers.get_servers(context.ROOT_DIR)
    tasks = [context.web.upload_file(server, file) for server in servers]
    for task in asyncio.as_completed(tasks):
        await task
