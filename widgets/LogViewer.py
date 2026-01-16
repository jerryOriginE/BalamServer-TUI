# widgets/logviewer.py
from textual.widgets import Static
from textual.containers import VerticalScroll
from services.journal import get_recent_logs
from collections import deque
import asyncio

from textual.widgets import Input

class LogViewer(VerticalScroll):
    BORDER_TITLE = "Log Viewer"
    MAX_LINES = 25
    REFRESH_INTERVAL = 3

    def __init__(self):
        super().__init__()
        self._task: asyncio.Task | None = None
        self.following = False

    def on_mount(self):
        self.lines = deque(maxlen=self.MAX_LINES)
        self.current_unit: str | None = None
        self.service = None
        self._task = asyncio.create_task(self.auto_refresh())
    
    async def auto_refresh(self):
        try:
            while True:
                if self.following:
                    await self.show_service(self.service)
                await asyncio.sleep(self.REFRESH_INTERVAL)
        except asyncio.CancelledError:
            pass

    async def show_service(self, service):
        self.current_unit = service.unit
        self.lines.clear()

        recent = await get_recent_logs(service.unit, lines=30)
        self.lines.extend(recent)

        self.refresh(layout=True)

    def toggle_follow(self):
        self.following = not self.following

    def set_service(self, service):
        self.service = service

    def write(self, text):
        self.following = False
        self.current_unit = "balam"
        self.lines.append(text)
        self.refresh()

    def render(self) -> str:
        if not self.current_unit:
            return "Select a service to view logs"

        header = f"{self.current_unit}"
        body = "\n".join(self.lines)
        return f"{header}\n{'─' * len(header)}\n{body}"
