# BALAM-Server TUI - v0.2.0

A lightweight, single-binary **Terminal User Interface (TUI)** for monitoring and following systemd services on the official Balam Server.

BalamServer-TUI is designed for **BALAM-SERVER**: no virtual environments, no Python installation, no runtime dependency management. Download one binary, drop it on the server, and run it.

---

## ✨ Features

* Interactive TUI built with **Textual**
* Live **systemd service list**
* Follow service logs in real time (journalctl)
* System status bar:

  * Hostname
  * Machine uptime
  * Load average
  * Disk usage
  * Current log mode

* Keyboard-driven workflow (no mouse required)
* Designed for SSH usage

---

## 🧠 Design Philosophy

* **Single binary deployment**
* Zero setup on target servers
* Opinionated but extensible
* Server-first (systemd, journalctl)
* Fail gracefully when services are missing

This tool is intended to be copied directly onto production or lab servers without polluting them with Python environments.

---

## 📦 Installation

### Option 1: Download prebuilt binary (recommended)

From GitHub Releases:

```bash
curl -L https://github.com/jerryOriginE/BalamServer-TUI/releases/latest/download/balam -o balam
chmod +x balam
sudo mv balam /usr/local/bin/balam
```

Run it anywhere:

```bash
balam
```

---

### Option 2: Build from source

> Only needed if you want to modify or extend the project.

#### Requirements

* Python 3.13+
* pip
* Linux with systemd

```bash
python -m venv .venv
source .venv/bin/activate
pip install textual
pip install yaml
python balam/app.py
```

---

## 🧱 Project Structure

```
BalamServer-TUI/
├── balam/
│   ├── app.py                # Application entrypoint
│   ├── dashboard.py          # Main TUI layout
│   ├── config.py             # Config Handler
│   ├── widgets/              # Textual widgets
│   │   ├── health_bar.py
│   │   ├── log_viewer.py
│   │   ├── postgres_info.py
│   │   ├── service_info.py
│   │   ├── service_list.py
│   │   └── status_bar.py
│   ├── services/             # Backend service logic
│   │   ├── registry.py
│   │   ├── journal.py
│   │   ├── systemctl.py
│   │   └── server.py
│   └── __init__.py
├── build.sh                   # PyInstaller build script
└── README.md
```

---

## ⚙️ Configuration

The application uses a YAML configuration file defining the services to display.

### Default behavior

* `config.yaml` is bundled **inside the binary**
* Works out-of-the-box

### Recommended (external override)

You can extend the app to load config from:

* `~/.config/balam/config.yaml`
* `/etc/balam/config.yaml`

If present, the external config overrides the bundled one.

---

## ⌨️ Keybindings

| Key   | Action                      |
| ----- | --------------------------- |
| ↑ / ↓ | Navigate services           |
| Enter | Select service              |
| f     | Toggle FOLLOW / STATIC mode |
| q     | Quit                        |

---

## 🧩 Log Modes

### STATIC

* Displays historical logs
* No auto-scroll
* Safe for inspection

### FOLLOW

* Real-time `journalctl -f`
* Auto-scroll enabled
* Ideal for debugging live services

The current mode is always visible in the status bar.

---

## 🚀 Distribution & Deployment

BalamServer-TUI is packaged using **PyInstaller**:

```bash
pyinstaller --onefile \
  --name balam \
  --collect-all textual \
  --collect-all yaml \
  balam/app.py
```

The resulting binary:

* Lives in `dist/balam`
* Contains all Python code and dependencies
* Can be copied to any compatible Linux system

---

## 🛡️ Limitations

* Linux only
* Requires systemd and journalctl
* Binary must be built on a compatible libc version
* Configuration changes require rebuild (unless external config override is used)

---

## 🗺️ Roadmap

* External config override (no rebuild required)
* `--version` and `--help` flags

---

## 🤝 Contributing

Contributions are welcome.

* Keep the single-binary philosophy
* Avoid introducing runtime dependencies
* Prefer clarity over cleverness

---

## 🐆 About BALAM

BALAM is a server and infrastructure tooling ecosystem focused on **clarity**, **robustness**, and **operability**.

This TUI is one building block toward a unified server management experience.
