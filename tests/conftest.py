import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from src.routes import get_routes


@pytest.fixture()
def cli(loop, aiohttp_client) -> TestClient:
    """Getting the client for server testing."""
    app = web.Application()
    app.add_routes(get_routes())
    return loop.run_until_complete(aiohttp_client(app))
