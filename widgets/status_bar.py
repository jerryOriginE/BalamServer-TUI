# widgets/status_bar.py
import os
import time
from textual.widgets import Static
from services.server import server_summary

class StatusBar(Static):
    def on_mount(self):
        self.start_time = time.time()
        self.set_interval(1, self.update_status)

    def update_status(self):
        uptime = int(time.time() - self.start_time)
        host = os.uname().nodename
        summary = server_summary()
        self.update(
            f" Host: {host} | Uptime: {uptime}s | Load: {summary['load']} | Disk: {summary['disk']}% | q: Quit "
        )