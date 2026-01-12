# widgets/logo.py
from textual.widgets import Static
from pathlib import Path

CREDITS = """\
BALAM-SERVER TUI
CREADO POR: GERARDO L. GUIZAR
GITHUB: github.com/jerryOriginE
ESTUDIANTE DE PREPATEC ZONA ESMERALDA
INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY
2024 - 2026
CAPITAN DE PROGRAMACION
"""

class BalamLogo(Static):
    BORDER_TITLE = "BALAM"
    DEFAULT_CSS = """
    BalamLogo {
        border: heavy $primary;
        padding: 1 2;
        color: $text;
    }
    """

    def __init__(self):
        super().__init__()

    def on_mount(self) -> None:
        self.update(CREDITS)