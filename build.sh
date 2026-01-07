pyinstaller --onefile --name balam --collect-all textual --collect-all yaml --add-data "balam/config.yaml:balam" balam/app.py
