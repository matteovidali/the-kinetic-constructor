from PyQt6.QtWidgets import (
    QWidget,
)
from typing import TYPE_CHECKING

from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_auto_builder_frame import (
    BaseAutoBuilderFrame,
)

from .freeform_auto_builder import FreeFormAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.auto_builder import (
        AutoBuilder,
    )


class FreeformAutoBuilderFrame(BaseAutoBuilderFrame):
    def __init__(self, auto_builder: "AutoBuilder") -> None:
        super().__init__(auto_builder, "freeform")
        self.builder = FreeFormAutoBuilder(self)

        # Attach specific action for sequence creation
        self.create_sequence_button.clicked.connect(self._on_create_sequence)
        self._load_settings()

    def _on_create_sequence(self):
        """Trigger sequence creation for Freeform."""
        self.builder.build_sequence(
            self.sequence_length_spinbox.value(),
            float(self.max_turn_intensity_combo.currentText()),
            self.sequence_level_combo.currentData(),
            self.continuous_rotation_checkbox.isChecked(),
        )
        self.auto_builder.sequence_builder.manual_builder.option_picker.update_option_picker()
