# widgets/log_viewer.py
from textual.widgets import Static
from balam.services.journal import get_recent_logs, follow_logs
from collections import deque
import asyncio
import contextlib

class LogViewer(Static):
    MAX_LINES = 200

    def on_mount(self):
        self.lines = deque(maxlen=self.MAX_LINES)
        self.current_unit: str | None = None
        self.following: bool = True
        self._follow_task: asyncio.Task | None = None

    async def show_service(self, service):
        await self.stop_following()

        self.current_unit = service.unit
        self.lines.clear()

        recent = await get_recent_logs(service.unit, lines=30)
        self.lines.extend(recent)

        self.refresh(layout=True)

        if self.following:
            self._start_following()

    def _start_following(self):
        if not self.current_unit or self._follow_task:
            return
        self._follow_task = asyncio.create_task(self._follow())

    async def _follow(self):
        try:
            async for line in follow_logs(self.current_unit):
                self.lines.append(line.rstrip())
                self.refresh()
        except asyncio.CancelledError:
            pass

    async def toggle_follow(self):
        self.following = not self.following

        if self.following:
            self._start_following()
        else:
            await self.stop_following()

        self.refresh(layout=True)

    async def stop_following(self):
        if self._follow_task:
            self._follow_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._follow_task
            self._follow_task = None

    def render(self) -> str:
        if not self.current_unit:
            return "Select a service to view logs"

        header = (
            f"[ FOLLOWING ] {self.current_unit}"
            if self.following
            else f"[ PAUSED ] {self.current_unit}"
        )

        body = "\n".join(self.lines)
        return f"{header}\n{'─' * len(header)}\n{body}"

    async def on_unmount(self):
        await self.stop_following()
