import asyncio
from datetime import datetime

from src.abstract.context import AContext
from src.domain import events
from src.domain.events import FileReplicatedEvent
from src.domain.model import File, ReplicatedFileStatus


async def replication_file(context: AContext, file: File):
    """
    Replication saved file to servers
    :param context: Context instance
    :param file: saved File instance
    """
    servers = await context.servers.get_servers(context.ROOT_DIR)
    # create uploading tasks
    tasks = [context.web.upload_file(server, file) for server in servers]
    start_time = datetime.now()
    for task in asyncio.as_completed(tasks):
        # get result of finished task
        result = await task
        # get the task execution time
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        event = events.FileReplicatedEvent(file, result["server"], duration, end_time)
        # run event handlers
        await context.events.publish(context, event)


async def send_replicated_file_status(context: AContext, event: FileReplicatedEvent):
    """
    Send a message to the origin server about the successful replication of the file.
    :param context: Context instance
    :param event: file replicated event
    """
    files_url = await context.env.get("FILES_URL")
    status = ReplicatedFileStatus(
        file_url=f"{files_url}/files/{event.file.name}.{event.file.file_type}",
        origin_url=event.file.origin_url,
        server=event.server,
        duration=event.duration,
        time=event.time,
    )
    await context.web.send_file_status(await context.env.get("ORIGIN_URL"), status)


EVENT_HANDLERS = {
    events.FileSavedEvent: [replication_file],
    events.FileReplicatedEvent: [send_replicated_file_status],
}
