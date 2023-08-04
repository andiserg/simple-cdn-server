from pathlib import Path

from src import adapters
from src.abstract import adapters as abstract


class Context:
    web: abstract.AWebClient
    files: abstract.AFileManager
    env: abstract.AEnvManager
    FILES_DIR: Path

    def __init__(self):
        self.web = adapters.WebClient()
        self.files = adapters.FileManager()
        self.env = adapters.EnvManager()
        self.FILES_DIR = Path(__file__).parent.parent / "files"
