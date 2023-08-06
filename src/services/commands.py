import asyncio

from src.abstract.context import AContext
from src.domain import events
from src.domain.model import File


async def download_file(context: AContext, link: str) -> File:
    """
    Downloading a file from the link.
    :param context: Context instance
    :param link: link to the file
    :return: File instance
    """
    return await context.web.download_file(link)


async def save_file(context: AContext, file: File) -> str:
    """
    Saving the file in the system and returning its name.
    :param context: Context instance
    :param file: bytes
    :return: file name
    """
    return await context.files.save_file(context.FILES_DIR, file)


async def replication_file(context: AContext, file: File):
    """
    Replication saved file to servers
    :param context: Context instance
    :param file: saved File instance
    """
    servers = await context.servers.get_servers(context.ROOT_DIR)
    # create uploading tasks
    tasks = [context.web.upload_file(server, file) for server in servers]
    for task in asyncio.as_completed(tasks):
        # get result of finished task
        result = await task
        event = events.FileReplicatedEvent(file, result["server"])
        # run event handlers
        await context.events.publish(context, event)
