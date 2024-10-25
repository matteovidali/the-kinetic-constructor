from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import Qt, QPropertyAnimation
from main_window.main_widget.learn_widget.base_classes.base_question_widget import (
    BaseQuestionWidget,
)


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import (
        Lesson1Widget,
    )


class Lesson1QuestionWidget(BaseQuestionWidget):
    """Widget for displaying the pictograph and managing its size and alignment."""

    def __init__(self, lesson_1_widget: "Lesson1Widget"):
        super().__init__(lesson_1_widget)
        self.lesson_1_widget = lesson_1_widget
        self.main_widget = lesson_1_widget.main_widget
        self.pictograph = None
        self._setup_label()
        self._setup_layout()

        # Animation-related properties
        self.fade_out_animation = None
        self.fade_in_animation = None

    def _setup_label(self):
        self.question_label = QLabel("What letter matches the pictograph?")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.question_label)

        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(self.spacer)

        self.setLayout(self.layout)

    def load_pictograph(self, pictograph_dict) -> None:
        """Load and display the pictograph."""
        super().load_pictograph(pictograph_dict)
        if self.pictograph:
            self.pictograph.tka_glyph.setVisible(False)

    def clear(self) -> None:
        """Remove the current pictograph view."""
        if self.pictograph:
            self.layout.removeWidget(self.pictograph.view)
            self.pictograph.view.deleteLater()
            self.pictograph = None

    def _resize_question_widget(self) -> None:
        self._resize_question_label()
        self._resize_pictograph()
        self._resize_spacer()

    def _resize_pictograph(self) -> None:
        if self.pictograph:
            self.pictograph.view.setFixedSize(
                self.main_widget.height() // 3, self.main_widget.height() // 3
            )

    def fade_out_pictograph(self):
        """Animate the fade-out effect on the pictograph view."""
        if self.pictograph and self.pictograph.view:
            opacity_effect = QGraphicsOpacityEffect()
            self.pictograph.view.setGraphicsEffect(opacity_effect)

            self.fade_out_animation = QPropertyAnimation(opacity_effect, b"opacity")
            self.fade_out_animation.setDuration(500)
            self.fade_out_animation.setStartValue(1)  # Start fully visible
            self.fade_out_animation.setEndValue(0)  # End invisible

            self.fade_out_animation.start()

    def fade_in_pictograph(self):
        """Animate the fade-in effect on the pictograph view."""
        if self.pictograph and self.pictograph.view:
            opacity_effect = QGraphicsOpacityEffect()
            self.pictograph.view.setGraphicsEffect(opacity_effect)

            self.fade_in_animation = QPropertyAnimation(opacity_effect, b"opacity")
            self.fade_in_animation.setDuration(500)
            self.fade_in_animation.setStartValue(0)  # Start invisible
            self.fade_in_animation.setEndValue(1)  # End fully visible

            self.fade_in_animation.start()
