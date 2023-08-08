from datetime import datetime


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
