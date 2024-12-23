from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsTextItem
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.reversal_symbol_manager import (
    ReversalSymbolManager,
)

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_sheet.act_splitter.act_beat_scroll.act_beat_frame.act_beat_view import (
        ActBeatView,
    )
    from main_window.main_widget.act_tab.act_sheet.act_splitter.act_beat_scroll.act_beat_frame.act_beat_frame import (
        ActBeatFrame,
    )


class ActBeat(BasePictograph):
    def __init__(self, beat_frame: "ActBeatFrame", duration: Union[int, float] = 1):
        super().__init__(beat_frame.main_widget)
        self.main_widget = beat_frame.main_widget
        self.reversal_symbol_manager = ReversalSymbolManager(self)
        self.view: "ActBeatView" = None
        self.beat_number_item: QGraphicsTextItem = None
        self.duration = duration
        self.is_placeholder = False
        self.parent_beat = None
        self.beat_number = 0
        self.blue_reversal = False
        self.red_reversal = False

    def get_beat_number_text(self) -> str:
        """
        Return the beat number or range of numbers if this beat spans multiple beats.
        """
        if self.duration > 1:
            end_beat = self.beat_number + self.duration - 1
            return f"{self.beat_number},{end_beat}"
        else:
            return str(self.beat_number)
