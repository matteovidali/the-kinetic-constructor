from typing import TYPE_CHECKING
from Enums.letters import Letter

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.settings_manager.visibility_settings.visibility_settings import VisibilitySettings


class GlyphVisibilityManager:
    def __init__(self, visibility_settings: "VisibilitySettings") -> None:
        self.visibility_settings = visibility_settings
        self.main_window = visibility_settings.settings_manager.main_window

    def apply_visibility(self, glyph_type: str, pictograph: "BasePictograph"):
        visibility = self.visibility_settings.get_glyph_visibility(glyph_type)
        if glyph_type == "VTG":
            pictograph.vtg_glyph.setVisible(visibility)
        elif glyph_type == "TKA":
            pictograph.tka_glyph.setVisible(visibility)
        elif glyph_type == "Elemental":
            pictograph.elemental_glyph.setVisible(visibility)
        elif glyph_type == "Positions":
            pictograph.start_to_end_pos_glyph.setVisible(visibility)
        elif glyph_type == "Reversals":
            if pictograph.blue_reversal:
                pictograph.blue_reversal_symbol.setVisible(visibility)
            if pictograph.red_reversal:
                pictograph.red_reversal_symbol.setVisible(visibility)

    def apply_current_visibility_settings(self, pictograph: "BasePictograph"):
        for glyph_type in ["VTG", "TKA", "Elemental", "Positions", "Reversals"]:
            visibility = self.visibility_settings.get_glyph_visibility(glyph_type)
            self.apply_visibility(glyph_type, pictograph)

        if pictograph.letter in [Letter.α, Letter.β, Letter.Γ]:
            pictograph.start_to_end_pos_glyph.setVisible(False)

    def apply_glyph_visibility(self):
        # Apply current settings to all visible pictographs
        for pictograph_list in self.main_window.main_widget.pictograph_cache.values():
            for pictograph in pictograph_list.values():
                if pictograph.view:
                    if pictograph.view.isVisible():
                        self.apply_current_visibility_settings(pictograph)


    def should_glyph_be_visible(self, glyph_type: str) -> bool:
        """Check if a glyph type should be visible based on current settings."""
        return self.visibility_settings.get_glyph_visibility(glyph_type)
