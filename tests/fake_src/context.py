from pathlib import Path

from src.abstract.context import AContext
from src.abstract.event_manager import AEventManager
from tests.fake_src import adapters as fake_adapters


class FakeContext(AContext):
    def __init__(self, event_manager: AEventManager):
        self.web = fake_adapters.FakeWebClient()
        self.files = fake_adapters.FakeFileManager()
        self.env = fake_adapters.FakeEnvManager()
        self.servers = fake_adapters.FakeServersManager()
        self.events = event_manager

        self.ROOT_DIR = Path(__file__).parent.parent
        self.FILES_DIR = self.ROOT_DIR / "files"
