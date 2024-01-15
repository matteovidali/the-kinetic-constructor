from PyQt6.QtWidgets import QVBoxLayout, QFrame
from typing import TYPE_CHECKING, List, Literal, Union
from constants import *
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.TypeChecking import AdjustmentNum, AdjustmentStr, PropRotDirs, Turns
from ...adjust_turns_button import AdjustTurnsButton

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from ..base_turns_widget.base_turns_widget import BaseTurnsWidget
    from ......filter_frame.attr_box.color_attr_box import ColorAttrBox
    from ......filter_frame.attr_box.motion_type_attr_box import MotionTypeAttrBox
    from ......filter_frame.attr_box.lead_state_attr_box import LeadStateAttrBox


class TurnAdjustmentManager:
    def __init__(self, attr_box, parent_widget: "BaseTurnsWidget") -> None:
        self.attr_box: Union[
            "ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"
        ] = attr_box
        self.parent_widget = parent_widget

    ### SETUP ###

    def setup_adjustment_buttons(self) -> None:
        """Create and setup adjustment buttons."""
        self._setup_button_frames()
        adjustments = [(-1, "-1"), (-0.5, "-0.5"), (1, "+1"), (0.5, "+0.5")]
        self.adjust_turns_buttons: List[AdjustTurnsButton] = [
            self._create_and_add_button(adj, text) for adj, text in adjustments
        ]

    def _setup_button_frames(self) -> None:
        self.negative_buttons_frame = QFrame()
        self.positive_buttons_frame = QFrame()
        self.negative_buttons_layout = QVBoxLayout(self.negative_buttons_frame)
        self.positive_buttons_layout = QVBoxLayout(self.positive_buttons_frame)

    def _create_and_add_button(
        self, adjustment: AdjustmentNum, text: AdjustmentStr
    ) -> AdjustTurnsButton:
        """Create an adjust turns button and add it to the appropriate layout."""
        button = AdjustTurnsButton(self.parent_widget, text)
        button.setContentsMargins(0, 0, 0, 0)
        button.setMinimumWidth(button.fontMetrics().boundingRect(text).width() + 10)
        button.clicked.connect(lambda _, adj=adjustment: self.adjust_turns(adj))

        layout = (
            self.negative_buttons_layout
            if adjustment < 0
            else self.positive_buttons_layout
        )
        layout.addWidget(button)
        return button

    ### GETTERS ###

    def is_motion_relevant(self, motion: "Motion") -> bool:
        attr_type = self.attr_box.attribute_type
        return getattr(motion, attr_type) == getattr(self.attr_box, attr_type)

    ### FLAGS ###

    def unpress_vtg_buttons(self) -> None:
        """Unpress the vtg buttons."""
        if hasattr(self.attr_box, "same_button"):
            self.attr_box.same_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=False)
            )
            self.attr_box.opp_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=False)
            )

    ### UPDATE ###

    def update_motion_properties(self, motion: "Motion", new_turns: Turns) -> None:
        self._update_turns_and_rotation(motion, new_turns)
        self.update_pictograph(motion, new_turns)

    def update_pictograph(self, motion: "Motion", new_turns: Turns) -> None:
        pictograph_dict = {f"{motion.color}_turns": new_turns}
        motion.scene.update_pictograph(pictograph_dict)

    ### PRIVATE METHODS ###

    def _adjust_turns_for_pictograph(
        self, pictograph: Pictograph, adjustment: Turns
    ) -> None:
        """Adjust turns for each relevant motion in the pictograph."""
        for motion in pictograph.motions.values():
            if self.is_motion_relevant(motion):
                new_turns = self._calculate_new_turns(motion.turns, adjustment)
                self.update_motion_properties(motion, new_turns)

    def _calculate_new_turns(self, current_turns: Turns, adjustment: Turns) -> Turns:
        """Calculate new turns value based on adjustment."""
        new_turns = max(0, min(3, current_turns + adjustment))
        return int(new_turns) if new_turns.is_integer() else new_turns

    def _update_turns_and_rotation(self, motion: "Motion", new_turns: Turns) -> None:
        """Update motion's turns and rotation properties based on new turn value."""
        if motion.motion_type in [DASH, STATIC]:
            self._handle_static_dash_motion(motion, new_turns)
        motion.set_motion_turns(new_turns)

    def _handle_static_dash_motion(self, motion: "Motion", new_turns: Turns) -> None:
        """Handle specific logic for static or dash motion types."""
        if new_turns == 0:
            motion.prop_rot_dir = NO_ROT
            self.unpress_vtg_buttons()
        elif motion.turns == 0:
            self._set_prop_rot_dir_based_on_vtg_state(motion)

    def _set_prop_rot_dir_based_on_vtg_state(self, motion: "Motion") -> None:
        """Set the rotation direction of the motion based on the vtg directional relationship."""
        other_motion = self._get_other_motion(motion)
        self._update_vtg_button_styles()
        motion.prop_rot_dir = self._determine_prop_rot_dir(other_motion)

    def _get_other_motion(self, motion: "Motion") -> "Motion":
        """Get the other motion based on color."""
        return motion.scene.motions[RED if motion.color == BLUE else BLUE]

    def _update_vtg_button_styles(self) -> None:
        """Update the vtg button styles."""
        same_pressed = self.attr_box.vtg_dir_btn_state[SAME]
        opp_pressed = self.attr_box.vtg_dir_btn_state[OPP]
        self.attr_box.same_button.setStyleSheet(
            self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=same_pressed)
        )
        self.attr_box.opp_button.setStyleSheet(
            self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=opp_pressed)
        )

    def _determine_prop_rot_dir(self, other_motion: "Motion") -> PropRotDirs:
        """Determine the property rotation direction."""
        if (
            not self.attr_box.vtg_dir_btn_state[SAME]
            and not self.attr_box.vtg_dir_btn_state[OPP]
        ):
            self._set_vtg_dir_state_default()
        if self.attr_box.vtg_dir_btn_state[SAME]:
            return other_motion.prop_rot_dir
        if self.attr_box.vtg_dir_btn_state[OPP]:
            return (
                COUNTER_CLOCKWISE
                if other_motion.prop_rot_dir == CLOCKWISE
                else CLOCKWISE
            )

    def _set_vtg_dir_state_default(self) -> None:
        """Set the vtg direction state to default."""
        self.attr_box.vtg_dir_btn_state[SAME] = True
        self.attr_box.vtg_dir_btn_state[OPP] = False

    def _clamp_turns(self, turns: Turns) -> Turns:
        """Clamp the turns value to be within allowable range."""
        return max(0, min(3, turns))

    ### PUBLIC METHODS ###

    def adjust_turns(self, adjustment: Turns) -> None:
        """Adjust turns for a given pictograph based on the attribute type."""
        turns = self.parent_widget.turn_display_manager.turns_display.text()
        turns = self.parent_widget._convert_turns_from_str_to_num(turns)
        turns = self._clamp_turns(turns + adjustment)
        self.parent_widget.turn_display_manager.update_turns_display(str(turns))

        for pictograph in self.attr_box.pictographs.values():
            self._adjust_turns_for_pictograph(pictograph, adjustment)

    def set_turns(self, new_turns: Turns) -> None:
        self.parent_widget.turn_display_manager.update_turns_display(new_turns)
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if self.is_motion_relevant(motion):
                    self.update_motion_properties(motion, new_turns)
