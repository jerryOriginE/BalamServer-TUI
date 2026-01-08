from textual.widgets import Static
from services.systemctl import get_service_info
import asyncio
import contextlib

def escape_markup(text: str) -> str:
    return text.replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")")

class ServiceInfo(Static):
    BORDER_TITLE = "Service Info"

    def __init__(self, *args, **kwargs):
        super().__init__(markup=True, *args, **kwargs)
        self.unit: str | None = None
        self._task: asyncio.Task | None = None
        self._refresh_lock = asyncio.Lock()

    async def show_service(self, service):
        self.unit = getattr(service, "unit", None)
        await self._safe_refresh()

    async def _safe_refresh(self):
        async with self._refresh_lock:
            try:
                await self._refresh()
            except Exception as e:
                msg = escape_markup(str(e))
                self.update(f"[red]Error updating service info:[/red] {msg}")

    async def _refresh(self):
        if not self.unit:
            self.update("[red]No service selected[/red]")
            return

        try:
            info = await asyncio.to_thread(get_service_info, self.unit)
        except Exception:
            info = None

        if not info:
            self.update(
                f"[bold]{escape_markup(str(self.unit))}[/bold]\n"
                f"[red]Service not found[/red]\n\n"
                f"[dim]Controls disabled[/dim]"
            )
            return

        state = escape_markup(str(info.get("ActiveState", "unknown")))
        substate = escape_markup(str(info.get("SubState", "unknown")))
        pid = escape_markup(str(info.get("MainPID", "-")))
        tasks = escape_markup(str(info.get("TasksCurrent", "-")))

        mem_bytes = int(info.get("MemoryCurrent", "0") or 0)
        mem_mb = mem_bytes / (1024 * 1024)

        cpu_nsec = int(info.get("CPUUsageNSec", "0") or 0)
        cpu_sec = cpu_nsec / 1e9

        state_color = "green" if state == "active" else "red"

        controls = "[>→] Start"
        if state == "active":
            controls = "[<O>] Restart   [■] Stop   [>→] Start"

        self.update(
            f"[bold]{escape_markup(self.unit)}[/bold]\n"
            f"[{state_color}]{state} ({substate})[/{state_color}]\n"
            f"PID: {pid}\n\n"
            f"[bold]Runtime[/bold]\n"
            f"CPU time: {cpu_sec:.1f}s\n"
            f"Memory: {mem_mb:.1f} MB\n"
            f"Threads: {tasks}\n\n"
            f"[bold]Controls[/bold] {controls}"
        )

    async def on_unmount(self):
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None
