# app.py
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from services.registry import load_services
from widgets.service_list import ServiceList, ServiceSelected
from widgets.log_viewer import LogViewer
from widgets.status_bar import StatusBar

class ServerDashboard(App):
    CSS = """
    ServiceList {
        width: 30%;
        border: tall $accent;
    }
    LogViewer {
        width: 70%;
        border: tall $primary;
    }
    StatusBar {
        height: 1;
        background: $panel;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("escape", "focus_services", "Services"),
    ]

    def action_focus_services(self):
        self.service_list.focus()

    def compose(self) -> ComposeResult:
        services = load_services(Path("config.yaml"))

        self.service_list = ServiceList(services)
        self.log_viewer = LogViewer()

        yield Vertical(
            Horizontal(
                self.service_list,
                self.log_viewer
            ),
            StatusBar(),
        )
        

    async def on_service_selected(self, message: ServiceSelected):
        await self.log_viewer.show_service(message.service)

if __name__ == "__main__":
    ServerDashboard().run()