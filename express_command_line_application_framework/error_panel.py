from rich.panel import Panel

class ErrorPanel(Panel):
    """A standard Panel format/template used to display errors."""

    def __init__(
        self,
        message: str = 'There was an error!',
        subtitle: str = '[bold bright_red]ERROR[/bold bright_red]',
        title: str = '[bold bright_red]Oops! There was an error...[/bold bright_red]',
    ):
        super().__init__(
            message,
            title=title,
            title_align='left',
            subtitle=subtitle,
            subtitle_align='right',
            expand=True,
            padding=1,
        )