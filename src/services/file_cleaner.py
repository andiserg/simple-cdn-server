import asyncio

from src.abstract.context import AContext


async def start_file_cleaner(context: AContext):
    """Initiate the file cleaner."""
    # time threshold for file deletion in seconds.
    expired_time = int(await context.env.get("FILE_EXPIRED_TIME"))
    # pause between iterations in seconds.
    sleep_time = int(await context.env.get("CLEANER_SLEEP_TIME"))
    while True:
        await file_clean_process(context, expired_time)
        await asyncio.sleep(sleep_time)


async def file_clean_process(context: AContext, expired_time: int):
    """System cleanup of old files."""
    old_files = await context.files.get_old_files(context.FILES_DIR, expired_time)
    if old_files:
        await context.files.delete_files(context.FILES_DIR, old_files)
