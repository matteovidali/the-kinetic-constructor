from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from Enums.Enums import LetterType
from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from .option_picker_section_widget import OptionPickerSectionWidget

if TYPE_CHECKING:
    from .option_picker_scroll_area import OptionPickerScrollArea


class OptionPickerDisplayManager:
    SPACING = 5

    def __init__(self, scroll_area: "OptionPickerScrollArea") -> None:
        self.scroll_area = scroll_area
        self.section_indices = {}
        self.pictograph_count = 0

    def order_and_display_pictographs(self) -> None:
        for letter_type in LetterType:
            ordered_pictographs = self.get_ordered_pictographs_for_section(letter_type)
            for index, (key, pictograph) in enumerate(ordered_pictographs.items()):
                self.add_pictograph_to_layout(pictograph, index)

    def add_pictograph_to_layout(self, pictograph: BasePictograph, index: int) -> None:
        row, col = divmod(index, self.scroll_area.option_picker.COLUMN_COUNT)
        letter_type = self.scroll_area.section_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section = self.scroll_area.section_manager.get_section(letter_type)
        if section:
            section.pictograph_frame.layout.addWidget(pictograph.view, row, col)
            # pictograph.view.resize_pictograph_view()
            pictograph.view.show()
            # hide or show the reversal symbols depending on the context
            pictograph.reversal_symbol_manager.update_reversal_symbols()

    def remove_pictograph(self, pictograph_key: str) -> None:
        pictograph_to_remove: BasePictograph = self.scroll_area.pictograph_cache.pop(
            pictograph_key, None
        )
        if pictograph_to_remove:
            self.scroll_area.layout.removeWidget(pictograph_to_remove.view)

    def get_ordered_pictographs_for_section(
        self, letter_type: LetterType
    ) -> dict[str, BasePictograph]:
        last_beat = self.scroll_area.manual_builder.last_beat
        relevant_pictographs: dict[str, BasePictograph] = {}

        for key, cached_pictograph in self.scroll_area.pictograph_cache.items():
            if self.is_pictograph_relevant(cached_pictograph, last_beat):
                pictograph_letter_type = (
                    self.scroll_area.section_manager.get_pictograph_letter_type(
                        cached_pictograph.letter
                    )
                )
                if pictograph_letter_type == letter_type:
                    relevant_pictographs[key] = cached_pictograph

        return {
            k: v
            for k, v in sorted(
                relevant_pictographs.items(),
                key=lambda item: (
                    list(Letter).index(Letter(item[1].letter)),
                    item[1].start_pos,
                ),
            )
        }

    def is_pictograph_relevant(
        self, cached_pictograph: BasePictograph, last_beat: Beat
    ) -> bool:
        """Check if a pictograph is a valid next option based on the current_pictograph."""

        if not hasattr(last_beat, "end_pos"):
            return False

        if last_beat.end_pos == cached_pictograph.start_pos:
            return True

    def clear_all_section_layouts(self):
        """Clears all widgets from all section layouts."""
        for section in self.scroll_area.section_manager.sections.values():
            section.clear_pictographs()

    def add_pictograph_to_section_layout(self, pictograph: BasePictograph):
        """Add a pictograph to its corresponding section layout."""
        letter_type = self.scroll_area.section_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: OptionPickerSectionWidget = (
            self.scroll_area.section_manager.get_section(letter_type)
        )

        if section:
            section.add_pictograph(pictograph)
