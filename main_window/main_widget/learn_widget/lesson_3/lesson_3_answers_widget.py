from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.learn_widget.base_classes.base_answers_widget import (
    BaseAnswersWidget,
)
from main_window.main_widget.learn_widget.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_3.lesson_3_widget import (
        Lesson3Widget,
    )


class Lesson3AnswersWidget(BaseAnswersWidget):
    """Widget responsible for displaying pictograph answers in Lesson 3."""

    def __init__(self, lesson_3_widget: "Lesson3Widget"):
        super().__init__(lesson_3_widget)
        self.lesson_3_widget = lesson_3_widget

        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.pictograph_views: list[QWidget] = []
        self.pictographs: dict[str, BasePictograph] = {}

    def display_answers(self, pictographs, correct_pictograph, check_answer_callback):
        """Display the pictographs as answer options."""
        self.clear()

        for pictograph_dict in pictographs:
            pictograph_key = (
                self.main_widget.pictograph_key_generator.generate_pictograph_key(
                    pictograph_dict
                )
            )
            pictograph = BasePictograph(self.main_widget)
            pictograph.view = LessonPictographView(pictograph)
            pictograph.disable_gold_overlay = False
            pictograph.updater.update_pictograph(pictograph_dict)
            pictograph.view.update_borders()
            self.pictographs[pictograph_key] = pictograph
            pictograph.view.setCursor(Qt.CursorShape.PointingHandCursor)
            pictograph.quiz_mode = True
            pictograph.view.mousePressEvent = (
                lambda event, opt=pictograph_dict: check_answer_callback(
                    opt, correct_pictograph
                )
            )

            self.pictograph_views.append(pictograph.view)

        for view in self.pictograph_views:
            self.layout.addWidget(view)

    def disable_answer(self, answer):
        """Disable a specific pictograph answer."""
        pictograph_key = (
            self.main_widget.pictograph_key_generator.generate_pictograph_key(answer)
        )
        wrong_answer = self.pictographs[pictograph_key]
        wrong_answer.view.setEnabled(False)
        wrong_answer.view.set_overlay_color("red")

    def clear(self):
        """Clear all the displayed pictographs."""
        for view in self.pictograph_views:
            self.layout.removeWidget(view)
            view.deleteLater()
        self.pictograph_views.clear()
        self.pictographs.clear()

    def resize_answers_widget(self):
        """Resize the pictograph views based on window size."""
        for view in self.pictograph_views:
            view.setFixedSize(
                self.main_widget.height() // 4, self.main_widget.height() // 4
            )
        spacing = self.main_widget.width() // 60
        self.layout.setSpacing(spacing)
