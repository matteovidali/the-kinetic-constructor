from typing import TYPE_CHECKING
from PyQt6.QtGui import QGuiApplication

if TYPE_CHECKING:
    from main import MainWindow


class WindowGeometryManager:
    def __init__(self, window: "MainWindow") -> None:
        self.window = window

    def set_dimensions(self) -> None:
        screens = QGuiApplication.screens()
        screen = screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        available_geometry = screen.availableGeometry()

        window_width = int((available_geometry.width() * 0.9))
        window_height = int((available_geometry.height() * 0.9))
        x = available_geometry.x() + int(
            ((available_geometry.width() - window_width) / 2)
        )
        y = available_geometry.y() + int(
            ((available_geometry.height() - window_height) / 2)
        )

        self.window.setGeometry(x, y, window_width, window_height)
