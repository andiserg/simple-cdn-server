import pytest

from src.domain.events import FileReplicatedEvent
from src.domain.model import File
from src.services.commands import replication_file


@pytest.mark.asyncio
async def test_replication_file_with_file_should_publish_event(fake_context):
    file = File(content=b"Hello world", file_type="txt")
    await replication_file(fake_context, file)

    assert isinstance(fake_context.events.events[-1], FileReplicatedEvent)
