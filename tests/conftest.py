import os
from typing import AsyncGenerator

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from src.abstract.context import AContext
from src.abstract.event_manager import AEventManager
from src.bootstrap import subscribe_handlers
from src.context import Context
from src.routes import get_handlers
from src.services.event_manager import EventManager
from tests.fake_src.app import init_test_app
from tests.fake_src.context import FakeContext
from tests.fake_src.event_manager import FakeEventManager


@pytest.fixture()
def cli(event_loop, aiohttp_client, context) -> TestClient:
    """Getting the client for server testing."""
    # Note: This is a duplicate of the code in main.py.
    # If you call init_app(), pytest will hang during execution.
    app = web.Application()
    handlers = get_handlers(context)
    app.add_routes(handlers)
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.fixture()
def test_app():
    return init_test_app()


@pytest.fixture()
def test_server(test_app, aiohttp_server):
    return aiohttp_server(test_app, port=int(os.environ.get("TEST_SERVER_PORT")))


@pytest.fixture()
def context(event_manager) -> AContext:
    return Context(event_manager)


@pytest.fixture()
def fake_context(fake_event_manager) -> AContext:
    return FakeContext(fake_event_manager)


@pytest.fixture()
def event_manager() -> AEventManager:
    return subscribe_handlers(EventManager())


@pytest.fixture()
def fake_event_manager() -> AEventManager:
    return FakeEventManager()


@pytest.fixture()
def test_chunk_iterator_download() -> AsyncGenerator:
    async def test_chunks_iterator():
        test_data = b"Hello, World"
        chunk_size = 5

        for i in range(0, len(test_data), chunk_size):
            yield (test_data[i : i + chunk_size], False)

    return test_chunks_iterator()


@pytest.fixture()
def test_chunk_iterator_upload() -> AsyncGenerator:
    async def test_chunks_iterator():
        test_data = b"Hello, World"
        chunk_size = 1

        for i in range(0, len(test_data), chunk_size):
            yield test_data[i : i + chunk_size]

    return test_chunks_iterator()
