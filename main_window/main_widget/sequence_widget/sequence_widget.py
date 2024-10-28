from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from .sequence_clearer import SequenceClearer
from .sequence_widget_layout_manager import SequenceWidgetLayoutManager
from .sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter
from .beat_frame.sequence_widget_beat_frame import SequenceWidgetBeatFrame
from .add_to_dictionary_manager.add_to_dictionary_manager import AddToDictionaryManager
from .labels.current_word_label import CurrentWordLabel
from .labels.difficulty_label import DifficultyLabel
from .graph_editor.graph_editor import GraphEditor
from .beat_frame.layout_options_dialog import LayoutOptionsDialog
from .labels.sequence_widget_indicator_label import SequenceWidgetIndicatorLabel
from .sequence_widget_pictograph_factory import BeatFactory
from .sequence_widget_button_panel import SequenceWidgetButtonPanel
from .sequence_widget_scroll_area import SequenceWidgetScrollArea

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceWidget(QWidget):
    beat_frame_layout: QHBoxLayout
    indicator_label_layout: QHBoxLayout

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.json_manager = self.main_widget.json_manager
        self.default_beat_quantity = 16

        self._setup_components()
        self.layout_manager.setup_layout()

    def _setup_components(self):
        # Managers
        self.add_to_dictionary_manager = AddToDictionaryManager(self)
        self.autocompleter = SequenceAutoCompleter(self)
        self.sequence_clearer = SequenceClearer(self)
        self.layout_manager = SequenceWidgetLayoutManager(self)
        
        # Labels
        self.indicator_label = SequenceWidgetIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = DifficultyLabel(self)
        
        # Sections
        self.scroll_area = SequenceWidgetScrollArea(self)
        self.beat_frame = SequenceWidgetBeatFrame(self)
        self.button_panel = SequenceWidgetButtonPanel(self)
        self.graph_editor = GraphEditor(self)
        

    def show_options_panel(self):
        self.options_panel = LayoutOptionsDialog(self)
        self.options_panel.exec()

    def resize_sequence_widget(self) -> None:
        self.current_word_label.resize_current_word_label()
        self.button_panel.resize_button_frame()
        self.beat_frame.resize_beat_frame()
        self.graph_editor.resize_graph_editor()

    def resizeEvent(self, event):
        self.resize_sequence_widget()
        super().resizeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.current_word_label.update_current_word_label_from_beats()
