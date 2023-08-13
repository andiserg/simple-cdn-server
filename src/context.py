from pathlib import Path

from src import adapters
from src.abstract.context import AContext
from src.abstract.event_manager import AEventManager


class Context(AContext):
    """
    The context holds all external tools for operation.
    It implements an abstract class AContext upon which
    both the service layer and infrastructure depend.
    """

    def __init__(self, event_manager: AEventManager):
        self.web = adapters.WebClient()
        self.files = adapters.FileManager()
        self.env = adapters.EnvManager()
        self.servers = adapters.ServersManager()
        self.events = event_manager

        self.ROOT_DIR = Path(__file__).parent.parent
        self.FILES_DIR = self.ROOT_DIR / "files"
