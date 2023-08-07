from src.abstract.context import AContext
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
