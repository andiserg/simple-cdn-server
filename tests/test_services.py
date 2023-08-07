import asyncio

import pytest

from src.abstract.context import AContext
from src.domain.events import Event, FileReplicatedEvent
from src.domain.model import File
from src.services.commands import replication_file
from src.services.event_manager import EventManager


@pytest.mark.asyncio
async def test_replication_file_with_file_should_publish_event(fake_context):
    file = File(content=b"Hello world", file_type="txt", origin_url="test")
    await replication_file(fake_context, file)

    assert isinstance(fake_context.events.events[-1], FileReplicatedEvent)


@pytest.mark.asyncio
async def test_event_manager_publish_with_handlers_should_process(fake_context):
    # create event class
    class TestEvent(Event):
        def __init__(self):
            # contains the names of handlers that processed the event
            self.processed_handlers = []

    # create handler
    async def handler(context: AContext, event: TestEvent):
        event.processed_handlers.append("handler")

    event_manager = EventManager()
    # subscribe handler to TestEvent
    await event_manager.subscribe(TestEvent, handler)

    event = TestEvent()
    await event_manager.publish(fake_context, event)
    # Provide control to the handler
    # and wait until it completes its task
    await asyncio.sleep(0.001)

    assert "handler" in event.processed_handlers
