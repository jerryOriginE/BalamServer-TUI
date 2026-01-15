# services/systemctl.py
import subprocess

FIELDS = [
    "ActiveState",
    "SubState",
    "MainPID",
    "MemoryCurrent",
    "CPUUsageNSec",
    "TasksCurrent",
    "ExecMainStartTimestamp",
    "ExecMainExitTimestamp",
]

def service_action(unit: str, action: str):
    subprocess.run(
        ["systemctl", action, unit],
        check=False,
    )

def get_service_info(unit: str ) -> dict | None:
    result = subprocess.run(
        ["systemctl", "show", unit],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 or not result.stdout:
        return None

    info = {}
    for line in result.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in FIELDS:
            info[key] = value

    return info


def check_service_exists(unit: str):
    try:
        result = subprocess.run(
                ["systemctl", "is-active", unit],
                capture_output=True,
                text=True,
                check=False,
                )
    
        return result.returncode in [0, 3]
    except Exception:
        return False
    
def get_service_status(unit: str) -> str:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", unit],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else "failed"
    except Exception:
        return "unkown"

def get_last_log_line(unit: str) -> str:
    result = subprocess.run(
        ["journalctl", "-u", unit, "-n", "1", "--no-pager"],
        capture_output=True,
        text=True,
    )
    line = result.stdout.strip()
    return line.split("\n")[-1] if line else ""
