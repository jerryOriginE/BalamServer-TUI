# widgets/global_command_list.py
from textual import work
from textual.widgets import ListView, ListItem, Label
from textual.message import Message
from modals.confirmation_box import CommandConfirmation

class CommandSelected(Message):
    def __init__(self, command) -> None:
        self.command = command
        super().__init__()

class CommandConfirmed(Message):
    def __init__(self, command) -> None:
        super().__init__()
        self.command = command

class GlobalCommandList(ListView):
    BORDER_TITLE = "Global Commands"

    def __init__(self, commands):
        super().__init__()
        self.commands = commands

    def execute_command(self, command):
        self.app.call_later(self._confirm_command, command)

    @work
    async def _confirm_command(self, command):
        confirmed = await self.app.push_screen_wait(
            CommandConfirmation(command)
        )

        if confirmed:
            self.app.notify(f"EXECUTING {command}")
            self.post_message(CommandConfirmed(command))
        else:
            self.app.notify("CANCELLED")


    def on_mount(self):
        self.load_commands()

    def load_commands(self):
        self.clear()

        for command in self.commands:
            label = Label(f"[yellow]{command.name}[/]")
            item = ListItem(label)
            item.command = command
            self.append(item)

    def on_list_view_selected(self, event):
        self.post_message(CommandSelected(event.item.command))
