import pytest
from aiohttp.test_utils import TestClient

from src.main import init_app


@pytest.fixture()
def cli(event_loop, aiohttp_client) -> TestClient:
    """Getting the client for server testing."""
    app = init_app()
    return event_loop.run_until_complete(aiohttp_client(app))
