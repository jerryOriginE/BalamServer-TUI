# services/registry.py
from dataclasses import dataclass
from pathlib import Path
from services.systemctl import get_service_status
import yaml

@dataclass
class Service:
    name: str
    unit: str
    active: bool 
    state: str | None = None
    last_log: str | None = None

@dataclass
class GlobalCommand:
    name: str
    command: str

def load_services(config_path: Path) -> list[Service]:
    with config_path.open() as f:
        data = yaml.safe_load(f)

    services = []
    for entry in data.get("services", []):
        services.append(Service(
            name=entry["name"],
            unit=entry["unit"],
            active=True if get_service_status(entry["unit"]) == "active" else False
            ))

    return services

def load_global_commands(config_path: Path) -> list[GlobalCommand]:
    with config_path.open() as f:
        data = yaml.safe_load(f)

    commands = []
    for entry in data.get("global_commands", []):
        commands.append(GlobalCommand(
            name=entry["name"],
            command=entry["command"]
            ))

    return commands
