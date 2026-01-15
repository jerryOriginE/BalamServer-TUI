from dashboard import ServerDashboard
import sys
from config import ensure_config_exists

VERSION = "v0.2.6"

if "--version" in sys.argv or "-v" in sys.argv:
    print(f"BALAM Server TUI - Initial Release - {VERSION}")
    sys.exit(0)

if "--make-config" in sys.argv or "-mc" in sys.argv:
    if ensure_config_exists():
        print("Configuration files already created at ~/.config/balam")
    else:
        print("Creating configuration files in ~/.config/balam")

    sys.exit(0)

if "--author" in sys.argv or "-a" in sys.argv:
    print("This utility was created by jerry.origin")
    sys.exit(0)

def main():
    app = ServerDashboard()
    app.run()

if __name__ == "__main__":
    main()
