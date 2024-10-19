from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QGridLayout, QApplication
from data.beat_frame_layouts import DEFAULT_BEAT_FRAME_LAYOUTS

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatFrameLayoutManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame
        self.selection_manager = beat_frame.selection_overlay
        self.settings_manager = beat_frame.main_widget.main_window.settings_manager

    def setup_layout(self) -> None:
        layout: QGridLayout = QGridLayout(self.beat_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.beat_frame.start_pos_view.start_pos.initializer.set_nonradial_points_visibility(
            False
        )
        layout.addWidget(self.beat_frame.start_pos_view, 0, 0)
        for i, beat in enumerate(self.beat_frame.beats):
            row, col = divmod(i, 8)
            layout.addWidget(beat, row + 1, col + 1)
        self.beat_frame.layout = layout
        self.configure_beat_frame(16)

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        return DEFAULT_BEAT_FRAME_LAYOUTS.get(beat_count, (1, beat_count))

    def get_cols(self):
        layout = self.beat_frame.layout
        cols = 0
        for i in range(layout.columnCount()):
            if layout.itemAtPosition(0, i):
                cols += 1
        return cols - 1

    def get_rows(self):
        layout = self.beat_frame.layout
        rows = 0
        for i in range(layout.rowCount()):
            if layout.itemAtPosition(i, 1):
                rows += 1
        return rows

    def configure_beat_frame(self, num_beats, override_grow_sequence=False):
        if not override_grow_sequence:
            grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
            if grow_sequence:
                num_filled_beats = self.beat_frame.get.next_available_beat() or 0
                num_beats = num_filled_beats
        columns, rows = self.calculate_layout(num_beats)

        self.beat_frame.sequence_widget.scroll_area.verticalScrollBarPolicy = (
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            if rows > 4
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.rearrange_beats(num_beats, columns, rows)

    def rearrange_beats(self, num_beats, columns, rows):
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beats
        for row in range(rows):
            for col in range(1, columns + 1):
                if index < num_beats:
                    beat_view = beats[index]
                    self.beat_frame.layout.addWidget(beat_view, row, col)
                    beat_view.remove_beat_number()
                    beat_view.add_beat_number(str(index + 1))
                    beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1

        self.beat_frame.adjustSize()
        selected_beat = self.selection_manager.selected_beat
        if selected_beat:
            self.selection_manager.deselect_beat()
            self.selection_manager.select_beat(selected_beat)
            self.selection_manager.update_overlay_position()

    def adjust_layout_to_sequence_length(self):
        last_filled_index = self.beat_frame.get.next_available_beat()
        self.configure_beat_frame(last_filled_index)