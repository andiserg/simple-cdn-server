from pathlib import Path

from src.abstract import adapters as abstract
from src.abstract.event_manager import AEventManager
from src.services.event_manager import EventManager
from tests.fake_src import adapters as fake_adapters


class FakeContext:
    web: abstract.AWebClient
    files: abstract.AFileManager
    env: abstract.AEnvManager
    servers: abstract.AServersManager
    events: AEventManager

    ROOT_DIR: Path
    FILES_DIR: Path

    def __init__(self):
        self.web = fake_adapters.FakeWebClient()
        self.files = fake_adapters.FakeFileManager()
        self.env = fake_adapters.FakeEnvManager()
        self.servers = fake_adapters.FakeServersManager()
        self.events = EventManager()

        self.ROOT_DIR = Path(__file__).parent.parent
        self.FILES_DIR = self.ROOT_DIR / "files"
