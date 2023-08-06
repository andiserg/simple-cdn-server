from pathlib import Path

from src import adapters
from src.abstract.context import AContext
from src.services.event_manager import EventManager


class Context(AContext):
    def __init__(self):
        self.web = adapters.WebClient()
        self.files = adapters.FileManager()
        self.env = adapters.EnvManager()
        self.servers = adapters.ServersManager()
        self.events = EventManager()

        self.ROOT_DIR = Path(__file__).parent.parent
        self.FILES_DIR = self.ROOT_DIR / "files"
