from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class CurrentlyDisplayingIndicatorLabel(QLabel):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_message(self, description):
        self.setText(f"Currently displaying {description}.")

    def resize_currently_displaying_label(self):
        font = self.font()
        font.setPointSize(self.browser.width() // 65)
        self.setFont(font)
