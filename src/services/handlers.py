from src.abstract.context import AContext
from src.domain.events import FileReplicatedEvent
from src.domain.model import ReplicatedFileStatus

EVENT_HANDLERS = {}


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
