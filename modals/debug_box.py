# modals/debug_box.py
from textual import color, on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label

class DebugBox(Screen[bool]):

    DEFAULT_CSS = """
    Label {
            color: $text
            }
    """

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Label(self.message)
        yield Button("Bruh", id = "yes", variant="success")
       
    @on(Button.Pressed, "#yes")
    def handle_yes(self) -> None:
        self.dismiss(True)

