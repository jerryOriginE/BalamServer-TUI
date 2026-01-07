# widget/service_info.py
from textual.widgets import Static
from textual.app import App
from balam.services.systemctl import get_service_info
import time
import asyncio

class ServiceInfo(Static):
    REFRESH_INTERVAL = 5  # seconds

    def __init__(self, *args, **kwargs):
        super().__init__(markup=True, *args, **kwargs)
        self.unit: str | None = None
        self._task: asyncio.Task | None = None

    async def show_service(self, service):
        self.unit = service.unit
        await self._refresh()

        if not self._task:
            self._task = asyncio.create_task(self._auto_refresh())

    async def _auto_refresh(self):
        try:
            while True:
                await asyncio.sleep(self.REFRESH_INTERVAL)
                if self.unit:
                    await self._refresh()
        except asyncio.CancelledError: 
            pass

    async def _refresh(self):
            info = await asyncio.to_thread(get_service_info, self.unit)

            # -------- FALLBACK: SERVICE DOES NOT EXIST --------
            if not info:
                self.update(
                    f"[bold]{self.unit}[/bold]\n"
                    f"[red]not found[/red]\n\n"
                    f"This service is not loaded or does not exist.\n\n"
                    f"[dim]Controls disabled[/dim]"
                )
                return

            # -------- NORMAL PATH --------
            state = info.get("ActiveState", "unknown")
            substate = info.get("SubState", "unknown")
            pid = info.get("MainPID", "-")

            mem_bytes = int(info.get("MemoryCurrent", "0") or 0)
            mem_mb = mem_bytes / (1024 * 1024)

            cpu_nsec = int(info.get("CPUUsageNSec", "0") or 0)
            cpu_sec = cpu_nsec / 1e9

            tasks = info.get("TasksCurrent", "-")

            state_color = "green" if state == "active" else "red"

            self.update(
                f"[bold]{self.unit}[/bold]\n"
                f"[{state_color}]{state} ({substate})[/{state_color}]\n"
                f"PID: {pid}\n\n"
                f"[bold]Runtime[/bold]\n"
                f"CPU time: {cpu_sec:.1f}s\n"
                f"Memory: {mem_mb:.1f} MB\n"
                f"Threads: {tasks}\n\n"
                f"[bold]Controls[/bold]\n"
                f"[R] Restart   [S] Stop   [▶] Start"
            )

    async def on_unmount(self):
        if self._task:
            self._task.cancel()