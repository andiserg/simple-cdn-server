import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from src.abstract.context import AContext
from src.abstract.event_manager import AEventManager
from src.bootstrap import subscribe_handlers
from src.context import Context
from src.routes import get_handlers
from src.services.event_manager import EventManager
from tests.fake_src.context import FakeContext
from tests.fake_src.event_manager import FakeEventManager


@pytest.fixture()
def cli(event_loop, aiohttp_client, fake_context) -> TestClient:
    """Getting the client for server testing."""
    # Note: This is a duplicate of the code in main.py.
    # If you call init_app(), pytest will hang during execution.
    app = web.Application()
    handlers = get_handlers(fake_context)
    app.add_routes(handlers)
    return event_loop.run_until_complete(aiohttp_client(app))


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
    return subscribe_handlers(FakeEventManager())
