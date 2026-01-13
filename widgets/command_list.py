# widgets/command_list.py
from textual.widgets import ListView, ListItem, Label

ACTIONS = {
        "start",
        "restart"
        "stop"
        "enable"
        "disable"
        }

def get_service_commands(unit):
    return ACTIONS

class CommandList(ListView):
    BORDER_TITLE = "Command List"

    def __init__(self):
        super().__init__()
        self.unit: str | None = None

    def on_mount(self):
        self._refresh()

    def _refresh(self):
        self.clear()
        if not self.unit:
            return

        commands = get_service_commands(self.unit)

        if not commands:
            
            return

        for command in commands:
            action = command
            description = "lorem ipsum"
            label = Label(f"{action} - {description}")
            item = ListItem(label)
            self.append(item)


    async def show_commands(self, service):
        self.unit = getattr(service, "unit", None)
        self._refresh()
