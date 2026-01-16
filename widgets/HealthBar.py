# widgets/health_bar.py
from textual.widgets import Static
from services.systemctl import get_service_status

class HealthBar(Static):
    def __init__(self, services):
        super().__init__()
        self.services = services

    def on_mount(self):
        self.refresh()

    def render(self) -> str:
        total = len(self.services)

        active = sum(
            1 for s in self.services
            if get_service_status(s.unit) == "active"
        )

        failed = sum(
            1 for s in self.services
            if get_service_status(s.unit) == "failed"
        )

        inactive = total - active - failed

        return (
            f"[b]BALAM SERVER[/b]  "
            f"[green]● {active} active[/]  "
            f"[yellow]○ {inactive} inactive[/]  "
            f"[red]✖ {failed} failed[/]"
        )
