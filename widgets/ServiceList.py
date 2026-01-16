# widgets/service_list.py
from textual.widgets import ListView, ListItem, Label
from textual.message import Message
from services.systemctl import get_service_status, get_last_log_line
import asyncio

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
    BORDER_TITLE = "Service List"
    REFRESH_INTERVAL = 5

    def __init__(self, services):
        super().__init__()
        self.services = services
        self._task: asyncio.Task | None = None

    def on_mount(self):
        self.refresh_status()
        self._task = asyncio.create_task(self.auto_refresh())

    async def auto_refresh(self):
        try:
            while True:
                await asyncio.sleep(self.REFRESH_INTERVAL)
                self.refresh_status()
        except asyncio.CancelledError:
            pass


    def refresh_status(self):
        self.clear()

        for service in self.services:
            status = get_service_status(service.unit)
            icon = STATUS_ICON.get(status, "?")
            color = STATUS_COLOR.get(status, "white")

            log = get_last_log_line(service.unit)
            log = (log or "").strip()
            log = log[:40]

            label = Label(f"[{color}]{icon}[/] {service.name} - {log}") 
            item = ListItem(label)
            item.service = service
            self.append(item)

    
    def on_list_view_selected(self, event):
        self.post_message(ServiceSelected(event.item.service))
