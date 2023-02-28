from rich.console import Console
from rich.panel import Panel

from .error_panel import ErrorPanel

class CommandNotYetImplementedError(Exception):

    def __init__(self, message):

        self.message = message

        print()

        console = Console()

        console.print(ErrorPanel(
            self.message,
        ))

        print()