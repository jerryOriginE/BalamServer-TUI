# widgets/service_command_list.py
from textual import work
from textual.widgets import ListView, ListItem, Label
from textual.message import Message
from modals.confirmation_box import CommandConfirmation

ACTIONS = {
        "start": {
            "icon": "",
            "desc": "Start the service",
            },
        "restart": {
            "icon":  "󰜉",
            "desc": "Restart the service",
            },
        "stop": {
            "icon": "",
            "desc": "Stop the service",
            },
        }


def get_service_commands(unit):
    return ACTIONS

class ServiceCommandSelected(Message):
    def __init__(self, command) -> None:
        self.command = command
        super().__init__()

class ServiceCommandConfirmed(Message):
    def __init__(self, command) -> None:
        super().__init__()
        self.command = command

class ServiceCommandList(ListView):
    BORDER_TITLE = "Service Command List"

    def __init__(self):
        super().__init__()
        self.unit: str | None = None
        self.active = False
        self.visible = False

    def execute_command(self, command):
        self.app.call_later(self._confirm_command, command)

    @work
    async def _confirm_command(self, command):
        confirmed = await self.app.push_screen_wait(
            CommandConfirmation(command)
        )

        if confirmed:
            self.app.notify(f"EXECUTING {command}")
            self.post_message(ServiceCommandConfirmed(command))
        else:
            self.app.notify("CANCELLED")

    def on_mount(self):
        self._refresh()

    def _refresh(self):
        self.clear()
        if not self.unit:
            return

        commands = get_service_commands(self.unit)

        if not commands or not self.active:
            self.visible = False 
            return
        self.visible = True

        for action, data in commands.items():

            action = data["icon"]
            description = data["desc"]
            label = Label(f"{action} - {description}")
            item = ListItem(label)
            item.command = action
            self.append(item)


    async def show_commands(self, service):
        self.unit = getattr(service, "unit", None)
        self.active = getattr(service, "active", False)
        self._refresh()

    def on_list_view_selected(self, event):
        self.post_message(ServiceCommandSelected(event.item.command))
