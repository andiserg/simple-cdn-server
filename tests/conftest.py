import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from src.context import Context
from src.routes import get_handlers
from tests.fake_src.context import FakeContext


@pytest.fixture()
def cli(event_loop, aiohttp_client) -> TestClient:
    """Getting the client for server testing."""
    # Note: This is a duplicate of the code in main.py.
    # If you call init_app(), pytest will hang during execution.
    context = Context()
    app = web.Application()
    handlers = get_handlers(context)
    app.add_routes(handlers)
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.fixture()
def context() -> Context:
    return Context()


@pytest.fixture()
def fake_context() -> FakeContext:
    return FakeContext()
