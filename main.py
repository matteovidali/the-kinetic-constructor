import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from profiler import Profiler
from settings_manager import SettingsManager
from utilities.window_manager import WindowGeometryManager
from widgets.main_widget.main_widget import MainWidget
from widgets.menu_bar.menu_bar import MainWindowMenuBar


class MainWindow(QMainWindow):
    def __init__(self, profiler: Profiler) -> None:
        super().__init__()
        self.profiler = profiler
        self.main_widget = MainWidget(self)
        self.settings_manager = SettingsManager(self)
        self.window_manager = WindowGeometryManager(self)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Sequence Constructor")
        self.menu_bar = MainWindowMenuBar(self.main_widget)
        self.setMenuBar(self.menu_bar)
        self.show()

    def exec_with_profiling(self, app: QApplication) -> int:
        for func in [app.exec, self.show]:
            self.profiler.runcall(func)
        return 0

    def closeEvent(self, event):
        self.settings_manager.save_settings()
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    profiler = Profiler()
    main_window = MainWindow(profiler)
    exit_code = main_window.exec_with_profiling(app)
    root_directory = os.path.dirname(os.path.abspath(__file__))
    profiler.write_profiling_stats_to_file("main_profiling_stats.txt", root_directory)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
