from pathlib import Path

from src import adapters
from src.abstract import adapters as abstract
from src.abstract.event_manager import AEventManager
from src.services.event_manager import EventManager


class Context:
    web: abstract.AWebClient
    files: abstract.AFileManager
    env: abstract.AEnvManager
    servers: abstract.AServersManager
    events: AEventManager

    ROOT_DIR: Path
    FILES_DIR: Path

    def __init__(self):
        self.web = adapters.WebClient()
        self.files = adapters.FileManager()
        self.env = adapters.EnvManager()
        self.servers = adapters.ServersManager()
        self.events = EventManager()

        self.ROOT_DIR = Path(__file__).parent.parent
        self.FILES_DIR = self.ROOT_DIR / "files"
