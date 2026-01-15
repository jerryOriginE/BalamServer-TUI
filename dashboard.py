# dashboard.py
from sys import stderr, stdout
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from services.registry import load_services, load_global_commands
from widgets.service_list import ServiceList, ServiceSelected
from widgets.log_viewer import LogViewer
from widgets.status_bar import StatusBar
from widgets.service_info import ServiceInfo
from widgets.health_bar import HealthBar
from services.systemctl import service_action
from widgets.postgres_info import PostgresInfo
from widgets.logo import BalamLogo
from widgets.service_command_list import ServiceCommandConfirmed, ServiceCommandList, ServiceCommandSelected
from widgets.global_command_list import CommandSelected, GlobalCommandList, CommandConfirmed
from config import config_path
import asyncio
from textual import work

class ServerDashboard(App):
    CSS = """
#main {
layout: horizontal;
height: 1fr;
}
#right-panel {
width: 25%;
}
Screen {
    background: $background 10%;
    layout: vertical;
}

/* Panels */
ServiceList, GlobalCommandList, ServiceCommandList, LogViewer, ServiceInfo, PostgresInfo {
    padding: 1;
    border: round $accent;
    background: $panel 10%;
}

/* Specific sizing */
ServiceList {
    width: 100%;
}
GlobalCommandList {
        width: 100%;
        }

LogViewer {
    width: 50%;
    overflow-y: auto;
}

ServiceInfo, PostgresInfo {
    width: 100%;
    border: round green;
}
PostgresInfo {
    width: 100%;
    border: round blue;
}
ServiceCommandList {
    width: 100%;
    border: round pink;
}
BalamLogo {
    width: 100%;
    border: round white;
}
/* Status bar */
StatusBar {
    height: 1;
    background: $boost;
    color: $text;
}

/* Health bar */
HealthBar {
    height: 1;
    padding-left: 1;
    padding-right: 1;
    color: $text;
    background: $boost;
}

/* Focus styles */
ServiceList:focus-within,
GlobalCommandList:focus-within,
ServiceCommandList:focus-within,
ServiceInfo:focus-within {
    border: round $primary;
}

/* Confirmation Modal */

Screen {
    align: center middle;
}

CommandConfirmation {
        width: 60;
        min-height: 12;
        padding: 1 2;
        background: $panel;
        border: round $primary;
        }

Label#CommandConfirmation {
        content-align: center middle;
        text-align: center;
        margin: 1 0 2 0;
        color: $text;
        }

Button {
        width: 1fr;
        margin: 0 1;
        }

Button#yes {
        background: $success;
        color: black;
        }

Button#no {
        background: $error;
        color: black;
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
        Binding("tab", "focus_commands", "Tabs"),
        Binding("f", "toggle_follow", "Follow Logs"),

    ]

    def action_focus_services(self):
        self.service_list.focus()

    def action_focus_commands(self):
        self.global_command_list.focus()

    def compose(self) -> ComposeResult:
        services = load_services(config_path())
        commands = load_global_commands(config_path())


        self.service_list = ServiceList(services)
        self.log_viewer = LogViewer()
        self.service_info = ServiceInfo()
        self.health_bar = HealthBar(services)
        self.status_bar = StatusBar()
        self.postgres_info = PostgresInfo()
        self.logo = BalamLogo()
        self.global_command_list = GlobalCommandList(commands)
        self.service_command_list = ServiceCommandList()

        yield self.health_bar

        yield Horizontal(
            Vertical(
                self.service_list,
                self.global_command_list,
                id="left-panel"),
            self.log_viewer,
            Vertical(
                self.service_info,
                self.postgres_info,
                self.service_command_list,
#                self.logo,
                id="right-panel",
            ),
            id="main",
        )

        yield self.status_bar

    async def on_service_selected(self, message: ServiceSelected):
        self.current_service = message.service
        await self.log_viewer.show_service(message.service)
        await self.service_info.show_service(message.service)
        self.log_viewer.following = False
        await self.service_command_list.show_commands(message.service)
        #await self.postgres_info.show_for_service(message.service)

    def on_command_selected(self, message: CommandSelected):
        self.global_command_list.execute_command(message.command)

    def on_command_confirmed(self, message: CommandConfirmed):
        self.run_global_command(message.command)

    def on_service_command_selected(self, message: ServiceCommandSelected):
        self.service_command_list.execute_command(message.command)

    def on_service_command_confirmed(self, message: ServiceCommandConfirmed):
        self.run_service_command(message.command)

    @work
    async def run_global_command(self, command):
        self.status_bar.set_text(f"Running {command.name}")

        self.log_viewer.lines.clear()
        self.log_viewer.write(f"$ {command.command}\n")

        process = await asyncio.create_subprocess_shell(
                command.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
        )

    @work
    async def run_service_command(self, command):
        self.status_bar.set_text(f"Running {command.name}")

        self.log_viewer.lines.clear()
        self.log_viewer.write(f"$ {command.name}\n")

        process = await asyncio.create_subprocess_shell(
                command.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
                )

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            self.log_viewer.write(line.decode().rstrip())

        code = await process.wait()

        if code == 0:
            self.status_bar.set_text(f"{command.name} completed")
        else:
            self.status_bar.set_text(f"{command.name} failed (code {code})")

    def action_toggle_follow(self):
        if not self.current_service:
            return

        self.log_viewer.set_service(self.current_service)
        self.log_viewer.toggle_follow()


    # OLD

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
        
