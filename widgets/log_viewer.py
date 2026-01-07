# widgets/log_viewer.py
from textual.widgets import Static
from textual.reactive import reactive
from services.journal import get_logs

class LogViewer(Static):
    current_unit = reactive(None)

    async def show_service(self, service):
        self.current_unit = service.unit
        self.update(f"[bold]Logs: {service.name}[/bold]\n\nLoading...")
        logs = await get_logs(service.unit)
        self.update(logs)