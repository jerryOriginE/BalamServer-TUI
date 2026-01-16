# widgets/command_bar.py
from textual.widgets import Input
from textual.containers import Container

class CommandBar(Container):
    DEFAULT_CSS = """
    CommandBar {
            dock: bottom;
            height: 3;
            background: $panel;
            padding: 0 1;
            }
    """

    def compose(self):
        yield Input(placeholder=":", id="command-input")

    def on_mount(self):
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted):
        command = event.value
        self.app.handle_command(command)
        self.remove()

    def on_key(self, event):
        if event.key == "escape":
            self.remove()
