from pathlib import Path

from src.abstract import adapters
from src.abstract.event_manager import AEventManager


class AContext:
    web: adapters.AWebClient
    files: adapters.AFileManager
    env: adapters.AEnvManager
    servers: adapters.AServersManager
    events: AEventManager

    ROOT_DIR: Path
    FILES_DIR: Path
