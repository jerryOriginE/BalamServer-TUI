# config.py
from pathlib import Path
import yaml

APP_NAME = "balam"

def config_path() -> Path:
    return Path.home() / ".config" / APP_NAME / "config.yaml"

def ensure_config_exists():
    path = config_path()

    if path.exists():
        return True
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        """# BALAM Server Configuration
services:
  - name: BALAM Server
    unit: balam-server.service
  - name: Cloudflared
    unit: cloudflared.service
"""
    )

def load_config() -> dict:
    ensure_config_exists()

    path = config_path()
    with path.open("r") as f:
        return yaml.safe_load(f) or {}
