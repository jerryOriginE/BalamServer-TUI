# widgets/service_list.py
from textual.widgets import ListView, ListItem, Label
from textual.message import Message
from balam.services.systemctl import get_service_status

STATUS_ICON = {
    "active": "●",
    "inactive": "○",
    "failed": "✖",
    "unknown": "?",
}

STATUS_COLOR = {
    "active": "green",
    "inactive": "yellow",
    "failed": "red",
    "unknown": "grey50",
}

class ServiceSelected(Message):
    def __init__(self, service):
        self.service = service
        super().__init__()

class ServiceList(ListView):
    def __init__(self, services):
        super().__init__()
        self.services = services

    def on_mount(self):
        self.refresh_status()
        self.set_interval(5, self.refresh_status)

    def refresh_status(self):
        self.clear()

        for service in self.services:
            status = get_service_status(service.unit)
            icon = STATUS_ICON.get(status, "?")
            color = STATUS_COLOR.get(status, "white")

            label = Label(f"[{color}]{icon}[/] {service.name}") 
            item = ListItem(label)
            item.service = service
            self.append(item)

    
    def on_list_view_selected(self, event):
        self.post_message(ServiceSelected(event.item.service))