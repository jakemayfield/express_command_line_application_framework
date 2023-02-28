from prompt_toolkit.completion import WordCompleter
from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import List, Optional

from .command import Command

class Route:

    def __init__(
        self,
        name: str,
        keys: List[str],
        path: str,
        description: Optional[str] = None,
    ) -> None:

        self.keys: List[str] = keys
        """A list of "keys" of which this route can be accessed by."""

        self.commands: List[Command] = []
        """A list of commands specific to this route."""

        self.command_completer: WordCompleter

        self.description: Optional[str] = description
        """A description of what this route represents."""

        self.name = name
        """The name of the location."""

        self.path = path
        """The path that this location can be accessed at."""

        self.register_commands()
        """Register any commands that are specific to this route."""

        self.set_command_completer()

    def display(self):
        """Represents what will be displayed when the user switches to this
        location the first time.
        """
        pass

    def register_commands(self) -> None:
        """Register commands specific to this route. This should be called
        by the subclass.
        """
        pass

    def render(self) -> None:
        """Currently an alias to display() method."""
        self.display()

    def render_help(self) -> None:
        """Renders the help menu for this route. This should be called by the
        subclass."""

        print()

        table = Table(
            expand=True,
            box=None,
            padding=1,
            leading=True,
            show_header=False,
            show_footer=False
        )

        # Add columns to the table.
        table.add_column(
            justify="left",
            style="grey42",
            no_wrap=False
        )
        table.add_column(
            style=''
        )

        table.add_row(
            'Path: ' + self.path,
            self.description
        )

        table.add_row(
            '[bold royal_blue1]Commands Available[/bold royal_blue1]',
            ''
        )

        # Loop through all commands and add them to the table.
        for command in self.commands:
            usage_string = ''
            if command.flags is not None:
                for flag in command.flags:
                    if '--' in flag.keys[0] or '-' in flag.keys[0]:
                        usage_string += f' {flag.keys[0]} [i]arg[/i]'
                    else:
                        usage_string += f' {flag.keys[0]}'
            # Show basic information about the command.
            table.add_row(
                f'[bold dark_orange]{command.name}[/bold dark_orange]'
                f'{usage_string}',
                f'[bold]{command.description}[/bold]'
            )
            # List all flags for this command.
            if command.flags is not None:
                for flag in command.flags:
                    key = ''
                    for index, key_name in enumerate(flag.keys):
                        if index != 0:
                            key += ' | '
                        key += key_name
                    table.add_row(key, flag.description)

        console = Console()
        console.print(Panel(
            table,
            title=f'Help for [bold red]"{self.name}"[/bold red]',
            title_align='left',
            # subtitle="This is a subtitle",
            # subtitle_align='right',
            expand=True,
            padding=0
        ))

        print()

    def set_command_completer(self) -> None:

        commands = []
        for command in self.commands:
            commands.append(command.name)

        self.command_completer = WordCompleter(commands)