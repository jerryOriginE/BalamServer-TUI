# services/server.py
import os
import shutil

def server_summary():
    load = os.getloadavg()[0]
    disk = shutil.disk_usage("/")
    disk_pct = int((disk.used / disk.total) * 100)

    return {
        "load": round(load, 2),
        "disk": disk_pct,
    }