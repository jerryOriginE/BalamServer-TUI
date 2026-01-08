# widgets/log_viewer.py
from textual.widgets import Static
from services.journal import get_recent_logs
from collections import deque

class LogViewer(Static):
    BORDER_TITLE = "Log Viewer"
    MAX_LINES = 20

    def on_mount(self):
        self.lines = deque(maxlen=self.MAX_LINES)
        self.current_unit: str | None = None

    async def show_service(self, service):
        self.current_unit = service.unit
        self.lines.clear()

        recent = await get_recent_logs(service.unit, lines=30)
        self.lines.extend(recent)

        self.refresh(layout=True)

    def render(self) -> str:
        if not self.current_unit:
            return "Select a service to view logs"

        header = f"{self.current_unit}"
        body = "\n".join(self.lines)
        return f"{header}\n{'─' * len(header)}\n{body}"
