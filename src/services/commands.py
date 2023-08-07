from pathlib import Path
from typing import AsyncIterable, Callable

from src.abstract.context import AContext
from src.domain.events import Event
from src.domain.model import FileInfo


async def publish_event(context: AContext, event: Event):
    """
    Publish an event to trigger the execution of handlers.

    :param context: Context instance
    :param event: The event to be published.
    """
    await context.events.publish(context, event)


async def download_and_save_file(
    context: AContext,
    link: str,
    files_dir: Path,
    file_name: str,
    save_file_function: Callable,
) -> FileInfo:
    """
    Downloading a file from the link.

    :param context: Context instance
    :param link: link to the file
    :param files_dir: path to dir of files
    :param file_name: file name
    :param save_file_function: Function for saving a file to the file system.
    The algorithm for downloading and saving the file will be executed in one place
    because they implement chunks download.
    It is important to save the file without closing the connection to the server.
    :return: iterator of file chunks
    """
    return await context.web.download_and_save_file(
        link, files_dir, file_name, save_file_function
    )


async def get_chunk_iterator(context: AContext, file_name: str) -> AsyncIterable:
    """
    Get a chunk iterator for the specified file.

    :param context: Context instance
    :param file_name: The path of the file to be streamed.
    :return: An iterator that yields chunks of the file.
    """
    file_path = context.FILES_DIR / file_name
    chunk_size = int(await context.env.get("CHUNK_SIZE"))
    return await context.files.get_chunk_iterator(file_path, chunk_size)
