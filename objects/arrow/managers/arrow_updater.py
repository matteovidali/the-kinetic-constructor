from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowUpdater:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def update_arrow(self, arrow_dict=None) -> None:
        if arrow_dict:
            self.arrow.attr_manager.update_attributes(arrow_dict)
        self.arrow.location_calculator.update_location()
        self.arrow.svg_manager.update_svg()
        self.arrow.mirror_manager.update_mirror()
        self.arrow.svg_manager.update_color()
        self.arrow.rot_angle_calculator.update_rotation()
