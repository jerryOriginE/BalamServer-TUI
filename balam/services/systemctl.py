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

def get_service_info(unit: str ) -> dict:
    result = subprocess.run(
        ["systemctl", "show", unit, "--no-page"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    info = {}
    for line in result.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in FIELDS:
            info[key] = value

    return info

def get_service_status(unit: str) -> str:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", unit],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()
    except Exception:
        return "unkown"