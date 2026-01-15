# modals/confirmation_box.py
from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label

class CommandConfirmation(Screen[bool]):

    def __init__(self, command) -> None:
        super().__init__()
        self.command = command

    def compose(self) -> ComposeResult:
        yield Label(f"Are you sure you want to execute {self.command}",id="CommandConfirmation")
        yield Button("EXECUTE", id="yes",variant="success")
        yield Button("CANCEL", id="no",variant="error")
    @on(Button.Pressed, "#yes")
    def handle_yes(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#no")
    def handle_no(self) -> None:
        self.dismiss(False)

