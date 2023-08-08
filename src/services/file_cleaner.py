import asyncio

from src.abstract.context import AContext


async def start_file_cleaner(context: AContext):
    expired_time = int(await context.env.get("FILE_EXPIRED_TIME"))
    sleep_time = int(await context.env.get("CLEANER_SLEEP_TIME"))
    while True:
        await file_clean_process(context, expired_time)
        await asyncio.sleep(sleep_time)


async def file_clean_process(context: AContext, expired_time: int):
    old_files = await context.files.get_old_files(context.FILES_DIR, expired_time)
    if old_files:
        await context.files.delete_files(context.FILES_DIR, old_files)
