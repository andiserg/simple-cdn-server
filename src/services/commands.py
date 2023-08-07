from pathlib import Path
from typing import Callable

from src.abstract.context import AContext
from src.domain.model import FileInfo


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
    :param save_file_function: Function for saving a file to the file system.
    The algorithm for downloading and saving the file will be executed in one place
    because they implement chunks download.
    It is important to save the file without closing the connection to the server.
    :return: iterator of file chunks
    """
    return await context.web.download_and_save_file(
        link, files_dir, file_name, save_file_function
    )


async def save_file(context: AContext, file: FileInfo) -> str:
    """
    Saving the file in the system and returning its name.
    :param context: Context instance
    :param file: bytes
    :return: file name
    """
    return await context.files.save_file(context.FILES_DIR, file)
