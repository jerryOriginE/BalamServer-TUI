from dashboard import ServerDashboard
import sys

VERSION = "v0.1.0"

if "--version" in sys.argv or "-v" in sys.argv:
    print(f"BALAM Server TUI - Initial Release - {VERSION}")
    sys.exit(0)

def main():
    app = ServerDashboard()
    app.run()

if __name__ == "__main__":
    main()