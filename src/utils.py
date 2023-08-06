import string
from datetime import datetime
from random import choices

from src.context import Context


class Timer:
    """
    The class is designed for measuring the
    code execution time using the context manager construct.
    """

    def __init__(self):
        self.execution_time = None

    async def __aenter__(self):
        # starting the time measurements
        self.start_time = datetime.now()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # recording result
        self.execution_time = (datetime.now() - self.start_time).seconds


async def get_unique_filename(context: Context) -> str:
    filename = generate_filename()
    while await context.files.is_file_exists(context.FILES_DIR, filename):
        # If a file with that name already exists, generate a new one
        filename = generate_filename()
    return filename


def generate_filename() -> str:
    """Getting a unique file name in the format <random_part>_<timestamp>."""
    basename = "".join(choices(string.ascii_letters + string.digits, k=5))
    suffix = int(datetime.now().timestamp())
    return f"{basename}_{suffix}"
