from typing import List, Optional, Dict, Any

from .flag import Flag

class Command:
    """Represents a command that can be called."""

    def __init__(
        self,
        name: str,
        callback: Optional[Any] = None,
        description: str = '',
        flags: Optional[List[Flag]] = None,
        options: List[str] = []
    ) -> None:

        self.callback: Optional[Any] = callback

        self.description = description
        """A description of the command."""

        self.flags: Optional[List[Flag]] = flags
        """A list of Flag objects that represent flags that can be passed to the
        command. The key represents the flag and the value represents the
        description of the flag.
        """

        self.name: str = name
        """The name of the command. Represents how the command is called by the
        user.
        """

        self.options: List[str] = []

    def execute(
        self,
        # callback: callable
    ) -> None:
        """Executes the command."""
        if self.callback is not None:
            self.callback()
        raise ValueError(
            f'No callback has been provided for this command: {self.name}'
        )

    def run(self) -> None:
        """Alias for execute() method."""
        self.execute()