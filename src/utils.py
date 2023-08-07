import string
from datetime import datetime
from random import choices

from src.abstract.context import AContext


async def get_unique_filename(context: AContext) -> str:
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
