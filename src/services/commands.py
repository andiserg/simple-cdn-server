from datetime import datetime
from pathlib import Path

from src.abstract.context import AContext
from src.domain import events
from src.domain.events import Event
from src.services.timer import Timer


async def publish_event(context: AContext, event: Event):
    """
    Publish an event to trigger the execution of handlers.

    :param context: Context instance
    :param event: The event to be published.
    """
    await context.events.publish(context, event)


async def download_and_save_file(
    context: AContext, link: str, files_dir: Path, file_name: str, *args, **kwargs
):
    """
    Downloading a file from the link.

    :param context: Context instance
    :param link: link to the file
    :param files_dir: path to dir of files
    :param file_name: file name
    :param args, kwargs: special utility functions for file storage
    """
    timer = Timer()
    # starting the timer for measuring the download time of the file
    async with timer:
        file_info = await context.web.download_and_save_file(
            link, files_dir, file_name, *args, **kwargs
        )
    event = events.FileSavedEvent(file_info, timer.execution_time, datetime.now())
    await publish_event(context, event)


async def save_file(context: AContext, file_name: str, *args, **kwargs) -> bool:
    """
    Save the file to the file system using streaming upload.

    :param context: Context instance
    :param file_name: file name
    :param args, kwargs: additional params for executing the file saving function
    :return: True if the file was saved successfully, False otherwise.
    """
    await context.files.save_file(context.FILES_DIR, file_name, *args, *kwargs)
    return True
