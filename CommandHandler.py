# CommandHandler.py
import os
import importlib.util

COMMANDS_DIR = "commands"

class CommandHandler():

    def __init__(self, app):
        self.app = app

    def load_commnd(self, command_name):
    
        for file in os.listdir(COMMANDS_DIR):
            if not file.endswith(".py") or file == "__init__.py":
                continue
    
            path = os.path.join(COMMANDS_DIR, file)
            module_name = file[:-3]
   
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
    
            aliases = getattr(module, "ALIAS", [])
    
            if command_name == module_name or command_name in aliases:
                return module
    
        return None
    
    def handle_command(self, input_string):
        parts = input_string.strip().split()
        if not parts:
            return
    
        command_name = parts[0]
        args = parts[1:]
    
        command = self.load_commnd(command_name)
    
        if not command:
            self.app.notify(f"Unkown command: {command_name}")
            return

        if not hasattr(command, "run"):
            self.app.notify(f"Command '{command_name}' has no run() function")
            return

        command.run(self.app, args)

        
