# modals/confirmation_box.py
from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label

class CommandConfirmation(Screen[bool]):

    DEFAULT_CSS = """
    Screen {
    align: center middle;
    background: $background 80%;
}

CommandConfirmation {
    width: 60;
    min-height: 12;
    padding: 1 2;
    background: $panel;
    border: round $primary;
}

Label {
    content-align: center middle;
    text-align: center;
    margin: 1 0 2 0;
    color: $text;
}

Button {
    width: 1fr;
    margin: 0 1;
}

Button#yes {
    background: $success;
    color: black;
}

Button#no {
    background: $error;
    color: black;
}

Horizontal {
    margin-top: 1;
}

    """

    def __init__(self, command) -> None:
        super().__init__()
        self.command = command

    def compose(self) -> ComposeResult:
        yield Label(f"Are you sure you want to execute {self.command}")
        yield Button("EXECUTE", id="yes",variant="success")
        yield Button("CANCEL", id="no",variant="error")

    @on(Button.Pressed, "#yes")
    def handle_yes(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#no")
    def handle_no(self) -> None:
        self.dismiss(False)

