# widgets/status_bar.py
import os
from textual.widgets import Static
from services.server import server_summary

def get_uptime_seconds() -> int:
    try:
        with open("/proc/uptime") as f:
            return int(float(f.read().split()[0]))
    except Exception:
        return 0


def format_uptime(seconds: int) -> str:
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)

    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


class StatusBar(Static):
    def on_mount(self):
        self.set_interval(1, self.update_status)

    def update_status(self):
        host = os.uname().nodename
        uptime = format_uptime(get_uptime_seconds())

        try:
            summary = server_summary()
            load = summary.get("load", "?")
            disk = summary.get("disk", "?")
        except Exception:
            load = "?"
            disk = "?"

        # Defensive: log_viewer may not exist yet
        log_viewer = getattr(self.app, "log_viewer")
        mode = "STATIC"
        mode = "FOLLOW" if log_viewer.following else "STATIC"

        self.update(
            f"[bold]{host}[/bold]  "
            f"| ⏱ {uptime}  "
            f"| Load: {load}  "
            f"| Disk: {disk}%  "
            f"| Mode: [{ 'green' if mode == 'FOLLOW' else 'yellow' }]{mode}[/]  "
            f"| q Quit"
        )

    def set_text(self, text):
        pass
