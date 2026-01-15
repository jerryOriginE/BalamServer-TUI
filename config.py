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
# BALAM Server Configuration
services:
  - name: BALAM Server
    unit: balam-server.service
  - name: Cloudflared
    unit: cloudflared.service

global_commands:
  - name: Start All Services 
    command:  systemctl start balam-server cloudflared
  - name: Stop All Services
    command:  systemctl stop balam-server cloudflared
  - name: Create a SQL Backup
    command:  backup
  - name: Update BALAM-SERVER backend
    command: deploy
  - name: Test System
    command: echo "system test"
 


        """
    )

def load_config() -> dict:
    ensure_config_exists()

    path = config_path()
    with path.open("r") as f:
        return yaml.safe_load(f) or {}
