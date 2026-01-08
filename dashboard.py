# dashboard.py
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from services.registry import load_services
from widgets.service_list import ServiceList, ServiceSelected
from widgets.log_viewer import LogViewer
from widgets.status_bar import StatusBar
from widgets.service_info import ServiceInfo
from services.systemctl import service_action
import asyncio


class ServerDashboard(App):
    CSS = """
/* General dashboard styling */
ServiceList {
    width: 25%;
    border: round $accent;
    padding: 1 1;
    background: $panel;
}

LogViewer {
    width: 50%;
    border: round $primary;
    padding: 1 1;
    background: $panel;
}

ServiceInfo {
    width: 25%;
    border: round $secondary;
    padding: 1 1;
    background: $panel;
}

StatusBar {
    height: 1;
    background: $panel;
    color: $text;
    text-style: bold;
    padding: 0 1;
}

/* Optional: log header styling */
LogViewer > Static {
    text-style: bold;
    color: $primary;
}

/* Optional: selected service highlight */
ServiceList > Static.-selected {
    background: $accent;
    color: $text;
    text-style: bold;
}

/* Optional: hover effect on services */
ServiceList > Static:hover {
    background: $accent-darken-1;
}

/* Optional: colors for service states in ServiceInfo */
ServiceInfo > Static[state="active"] {
    color: green;
}

ServiceInfo > Static[state="inactive"] {
    color: red;
}

/* Optional: borders and padding for nice spacing */
Horizontal {
    padding: 1;
    gap: 1;
}

Vertical {
    padding: 1;
    gap: 1;
}
"""

    TITLE = "BALAM Server"
    
    def __init__(self):
        super().__init__()
        self.current_service = None

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("Q", "quit", "Quit"),
        Binding("escape", "focus_services", "Services"),
        Binding("f", "toggle_follow", "Follow Logs"),

        Binding("r", "restart_service", "Restart Service"),
        Binding("s", "stop_service", "Stop Service"),
        Binding("p", "start_service", "Start Service"),
    ]

    def action_focus_services(self):
        self.service_list.focus()

    def compose(self) -> ComposeResult:
        services = load_services(Path("config.yaml"))

        self.service_list = ServiceList(services)
        self.log_viewer = LogViewer()
        self.service_info = ServiceInfo()

        yield Vertical(
            Horizontal(
                self.service_list,
                self.log_viewer,
                self.service_info,
            ),
            StatusBar(),
        )
        

    async def on_service_selected(self, message: ServiceSelected):
        self.current_service = message.service
        await self.log_viewer.show_service(message.service)
        await self.service_info.show_service(message.service)

    async def action_toggle_follow(self):
        await self.log_viewer.toggle_follow()

    async def action_restart_service(self):
        if not self.current_service:
            return
        
        await asyncio.to_thread(
            service_action,
            self.current_service.unit,
            "restart",
        )

        await self.service_info.show_service(self.current_service)

    async def action_stop_service(self):
        if not self.current_service:
            return
        
        await asyncio.to_thread(
            service_action,
            self.current_service.unit,
            "stop",
        )

        await self.service_info.show_service(self.current_service)

    async def action_start_service(self):
        if not self.current_service:
            return
        
        await asyncio.to_thread(
            service_action,
            self.current_service.unit,
            "start",
        )

        await self.service_info.show_service(self.current_service)
        
