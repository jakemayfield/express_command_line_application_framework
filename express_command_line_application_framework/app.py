from typing import Any, List

from prompt_toolkit.buffer import Buffer
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style

from .custom_prompt_toolkit import NestedCompleter, WordCompleter

from prompt_toolkit import prompt
from rich.console import Console
from rich import print

from .invalid_location_error import InvalidLocationError
from .command import Command
from .route import Route

from .command_not_yet_implemented_error import CommandNotYetImplementedError

class App():

    def __init__(self):

        self.is_authenticated = False
        """A boolean value that determines whether the user is authenticated.
        Default is False and default credentials are 'admin' and 'admin'."""

        self.commands = []
        """A list of "global" commands, represented by Command objects, that are
        available to be called from anywhere within the application.
        """

        self.available_commands: List[Command] = []
        """A list of Command objects that are available to the user at
        the current time.
        """

        self.command_completer: NestedCompleter | WordCompleter

        self.display_buffer = Buffer()

        self.route: Route
        """The current route/location/path of the user in the application. This
        is used to track which commands are available to the user. All locations
        should be prefixed with a forward slash.
        """

        self.routes: List[Route] = []

        self.locations: List[Route] = []
        """A list of locations available to switch to."""

        self.history = InMemoryHistory()

        self.session = PromptSession(
            history=self.history,
            enable_history_search=True
        )

        self.requires_authentication = False
        """Whether or not this application requires authentication."""

        # Register routes for this application.
        self.register_routes()

        # Register the starting or default commands.
        self.register_commands()

        # Update the available commands.
        self.update_available_commands()

        self.loop()

    def authenticate(self, username: str, password: str) -> None:
        """Add simple demo authentication."""
        # Check username and password provided.
        if username == 'admin' and password == 'admin':
            # Authenticated.
            self.is_authenticated = True
            return
        self.is_authenticated = False
        self.display_buffer.reset()

    def exit(self) -> None:
        # Print some exit message before we go.
        print('Goodbye!')
        exit()

    def _extract_location(self, input: str) -> str:
        """Extracts the location from the input if it's a valid location."""
        location = input.split(' ')[0]
        # TODO: Restore this.
        # if location not in self.locations:
        #     raise InvalidLocationError(
        #         f'"{location}" is not a valid location. Location was not found '
        #         f'in the list of valid locations.'
        #     )
        return location

    def loop(self):

        style = Style.from_dict(
            {
                "username": "#aaaaaa italic",
                "path": "#ffffff bold",
                "branch": "bg:#666666",
                "branch exclamation-mark": "#ff0000",
                "env": "bg:#666666",
                "left-part": "bg:#444444",
                "right-part": "bg:#444444",
                "padding": "bg:#444444",
            }
        )
        """The main loop of the application."""

        # Print some welcome message.
        # self.display_welcome_message()

        while True:
            try:

                if self.requires_authentication \
                and self.is_authenticated is False:
                    self.prompt_for_authentication()
                    if self.is_authenticated is False:
                        continue

                # Await user input.
                input = prompt(
                    self.get_prompt,
                    completer=self.command_completer,
                    style=style,
                    refresh_interval=1
                )

                # Process user input.
                self.process_input(input)

                continue

            except KeyboardInterrupt:
                # pass # Ctrl-C pressed. Try again.
                continue
            except InvalidLocationError as e:
                # Invalid location.
                print(e.message)
                continue
            except CommandNotYetImplementedError:
                # Return to prompt.
                continue
            else:
                break

    def get_prompt(self) -> Any:
        """Build the prompt dynamically every time its rendered."""
        return [
            ('fg: purple', f'{self.route.path} '),
            ('#ffffff', f'$ ')
        ]

    def _is_valid_command(self) -> None:
        raise NotImplementedError('Not implemented yet.')
        # Checks if command is a valid command.
        # ...
        pass

    def process_input(self, input: str) -> None:
        """Process the user's input."""

        # * This is a two step process:
        # * 1. Handle any commands that are "actions" that need to be taken.
        # * 2. Print out the visual that should be displayed to the user after
        # * running the command.

        # TODO: Match the input to a command.
        # ? How best to do this?

        # Split command by spaces.
        command_bits = input.split(' ')
        command = command_bits[0]

        # Check for "exit" command.
        exit_commands = ['exit', 'quit', 'q']
        if command in exit_commands:
            self.exit()
            return

        # Check if the input is route-switching command.
        key = self._extract_location(command)
        for route in self.routes:
            if key in route.keys:
                self.update_route(route)
                # Since we are switching our route. We need to update the
                # command to be the second index of the command bits.
                try:
                    command = command_bits[1]
                except IndexError:
                    # Update the commands available to the user.
                    self.update_available_commands()
                    return

        # Update the commands available to the user.
        self.update_available_commands()

        # Check for "help" command.
        if command == '?':
            self.route.render_help()
            return

        for available_command in self.available_commands:
            if command == available_command.name:
                available_command.run()

        self.route.render()

        # console = Console()
        # console.print(f":megaphone: {input}")
        # console.print(f"🔳 task 1")

        # ? How best to automatically load this logic and keep it DRY?

        # Load pane logic based on current location.
        # ...

    def prompt_for_authentication(self) -> None:
        """Prompt the user for authentication."""
        print('Sign In')
        console = Console()
        console.print(":lock: [bold red]Sign In[/bold red]")
        # Await user input.
        username = prompt(
            'Username: ',
            refresh_interval=.5
        )
        password = prompt(
            'Password: ',
            refresh_interval=.5,
            is_password=True
        )
        self.authenticate(username, password)

    def register_commands(self) -> None:
        """Registers any "global" commands that are available to the user
        throughout the application.
        """

        # Default commands.
        default_commands = [
            '?', '..', 'quit', 'q', '/'
        ]

        for command in default_commands:
            command = Command(name=command)
            if command == '..':
                # TODO: Create callback that will go back to the previous route.
                pass
            self.commands.append(command)

    def register_routes(self) -> None:
        """This method is called and registers the routes or "locations" for
        this application.
        """

        # START: Add your own custom routes here. The first route your add will
        # be the default or starting route.

        # Add/register custom routes here.

        # STOP: Do not edit anything after here.

        # Set starting/default route.
        self.route = self.routes[0]

    def set_command_completer(self) -> None:
        """Builds the nested dictionary required to provide to NestedCompleter
        class from the `available_commands` instance attribute list.
        """

        # Return early if there is nothing to do here.
        if len(self.available_commands) == 0: return

        available_commands = dict()

        # Start with the "global" commands.
        for command in self.available_commands:
            available_commands[command.name] = None

        # Add all commands for route switching.
        for route in self.routes:
            for key in route.keys:
                # If route has its own commands, add them to the completer.
                if len(route.commands) > 0:
                    available_commands[key] = {}
                    for command in route.commands:
                        available_commands[key][command.name] = None
                else:
                    available_commands[key] = None

        # Add any commands from the current route.
        for command in self.route.commands:
            available_commands[command.name] = None

        # Comment out when not debuggin.
        # print(available_commands)

        # TODO: Remove any duplicate Commands in the list.
        # self.available_commands = list(dict.fromkeys(self.available_commands))

        # Set/update the command completer.
        self.command_completer = NestedCompleter.from_nested_dict(
            available_commands
        )

    def update_available_commands(self) -> None:
        """Updates the list of available commands. This method combines all of
        the Commands from root level and the current route. The purpose of this
        method is mostly to build of list of commands available to the user for
        the auto-complete feature.
        """

        # Start with a clean list.
        self.available_commands = []

        # Start with the "global" commands.
        for command in self.available_commands:
            self.available_commands.append(command)

        # Add all commands for route switching.
        for route in self.routes:
            for key in route.keys:
                # Create temp Command object to handle route switching.
                command = Command(name=key)
                self.available_commands.append(command)

        # Add any commands from the current route.
        for command in self.route.commands:
            self.available_commands.append(command)

        # Comment this out when not debugging.
        # Print out the available commands.
        # for command in self.available_commands:
        #     print(command.name)

        self.set_command_completer()

    def update_route(self, route: Route) -> None:
        self.route = route
