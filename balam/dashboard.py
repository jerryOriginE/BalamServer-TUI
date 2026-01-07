# dashboard.py
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from importlib.resources import files
from balam.services.registry import load_services
from balam.widgets.service_list import ServiceList, ServiceSelected
from balam.widgets.log_viewer import LogViewer
from balam.widgets.status_bar import StatusBar
from balam.widgets.service_info import ServiceInfo
from balam.services.systemctl import service_action
import asyncio

class ServerDashboard(App):
    def __init__(self):
        super().__init__()
        self.current_service = None

    CSS = """
    ServiceList {
        width: 25%;
        border: tall $accent;
    }
    LogViewer {
        width: 50%;
        border: tall $primary;
    }
    StatusBar {
        height: 1;
        background: $panel;
        color: $text;
    }
    ServiceInfo {
        width: 25%;
        border: tall $secondary;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("escape", "focus_services", "Services"),
        Binding("f", "toggle_follow", "Follow Logs"),

        Binding("r", "restart_service", "Restart Service"),
        Binding("s", "stop_service", "Stop Service"),
        Binding("p", "start_service", "Start Service"),
    ]

    def action_focus_services(self):
        self.service_list.focus()

    def compose(self) -> ComposeResult:
        config_path = files("balam").joinpath("config.yaml")
        services = load_services(config_path)

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
        
