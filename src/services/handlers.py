import asyncio
from dataclasses import asdict
from datetime import datetime

from src.abstract.context import AContext
from src.domain import events
from src.domain.events import FileProcessedEvent, FileReplicatedEvent, FileSavedEvent
from src.domain.model import FileInfo, Server


async def replicate_file(context: AContext, event: FileSavedEvent):
    """
    Initiate tasks for file replication to servers
    and publish an event upon replication completion
    :param context: Context instance
    :param event: file saved event
    """
    # get all servers without current server
    servers = [
        server
        for server in await context.servers.get_servers(context.ROOT_DIR)
        if server.name != await context.env.get("NAME")
    ]
    # create tasks for file replication to each server
    tasks = [
        context.web.upload_file(server, context.FILES_DIR, event.file_info)
        for server in servers
    ]
    # Indicates completion of all tasks, including the last one.
    # 'is_last_server' flag is added to the event after the final task.
    completed_tasks = []
    # start the timer to measure the duration of file replication.
    start_time = datetime.now()
    for task in asyncio.as_completed(tasks):
        # get result of finished task
        result = await task
        completed_tasks.append(task)
        # create FileReplicatedEvent
        replicated_event = create_file_replicated_event(
            start_time, tasks, completed_tasks, event.file_info, result["server"]
        )
        # run event handlers
        await context.events.publish(context, replicated_event)


def create_file_replicated_event(
    start_time: datetime,
    tasks: list,
    completed_tasks: list,
    file_info: FileInfo,
    server: Server,
) -> FileReplicatedEvent:
    """Create a FileReplicatedEvent based on the data."""
    # get the task execution time
    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    return events.FileReplicatedEvent(
        file_info,
        duration,
        end_time,
        server,
        # if True, indicates the last task has finished.
        len(completed_tasks) == len(tasks),
    )


async def send_saved_file_status(context: AContext, event: FileSavedEvent):
    """
    Send a message to the origin server about the successful saving of the file.
    :param context: Context instance
    :param event: file saved event
    """
    files_url = await context.env.get("FILES_URL")
    status = event_to_dict(event, files_url)
    status["type"] = "saved"
    status["server"] = get_current_server_data(context)
    await context.web.send_file_status(await context.env.get("ORIGIN_URL"), status)


async def send_replicated_file_status(context: AContext, event: FileReplicatedEvent):
    """
    Send a message to the origin server about the successful replication of the file.
    :param context: Context instance
    :param event: file replicated event
    """
    files_url = await context.env.get("FILES_URL")
    status = event_to_dict(event, files_url)
    status["type"] = "replicated"
    status["from_server"] = get_current_server_data(context)
    status["to_server"] = asdict(event.server)
    await context.web.send_file_status(await context.env.get("ORIGIN_URL"), status)


async def get_current_server_data(context: AContext):
    """Get information about the current server"""
    return {
        "name": await context.env.get("NAME"),
        "ip": await context.env.get("IP"),
        "zone": await context.env.get("ZONE"),
    }


def event_to_dict(event: FileProcessedEvent, files_url: str) -> dict:
    """
    Convert event to a dictionary and add additional fields
    :param event: instance of a child class of the FileProcessedEvent
    :param files_url: URL of the file servers domain
    :return: status in dict format
    """
    file_name = f"{event.file_info.name}.{event.file_info.file_type}"
    status = asdict(event)
    status["file_url"] = f"{files_url}/files/{file_name}"
    status["time"] = event.time.strftime("%Y/%m/%d %H:%M:%S")
    return status


# Dictionary of events and their handlers
# {event: [handler1, handler2]...}
EVENT_HANDLERS = {
    events.FileSavedEvent: [replicate_file, send_saved_file_status],
    events.FileReplicatedEvent: [send_replicated_file_status],
}
