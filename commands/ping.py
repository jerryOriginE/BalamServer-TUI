# commands/ping.py

ALIAS = ["p"]

def run(app, args):
    app.notify("Pong!")
    app.notify(f"Arguments: {args}")
