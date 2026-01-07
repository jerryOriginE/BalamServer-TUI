# services/registry.py
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class Service:
    name: str
    unit: str

def load_services(config_path: Path) -> list[Service]:
    with config_path.open() as f:
        data = yaml.safe_load(f)

    services = []
    for entry in data.get("services", []):
        services.append(Service(
            name=entry["name"],
            unit=entry["unit"]      
        ))

    return services