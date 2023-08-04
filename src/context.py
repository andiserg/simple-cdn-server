from pathlib import Path

from src import adapters
from src.abstract import adapters as abstract


class Context:
    web: abstract.AWebClient
    files: abstract.AFileManager
    FILES_DIR: Path

    def __init__(self):
        self.web = adapters.WebClient()
        self.files = adapters.FileManager()
        self.FILES_DIR = Path(__file__).parent.parent / "files"
