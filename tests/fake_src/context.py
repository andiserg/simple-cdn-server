from pathlib import Path

from src.abstract.context import AContext
from src.services.event_manager import EventManager
from tests.fake_src import adapters as fake_adapters


class FakeContext(AContext):
    def __init__(self):
        self.web = fake_adapters.FakeWebClient()
        self.files = fake_adapters.FakeFileManager()
        self.env = fake_adapters.FakeEnvManager()
        self.servers = fake_adapters.FakeServersManager()
        self.events = EventManager()

        self.ROOT_DIR = Path(__file__).parent.parent
        self.FILES_DIR = self.ROOT_DIR / "files"
