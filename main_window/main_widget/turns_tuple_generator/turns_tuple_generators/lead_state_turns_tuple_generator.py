from typing import TYPE_CHECKING
from main_window.main_widget.turns_tuple_generator.turns_tuple_generators.base_turns_tuple_generator import (
    BaseTurnsTupleGenerator,
)

if TYPE_CHECKING:
    pass


class LeadStateTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        leading_motion = self.pictograph.get.leading_motion()
        trailing_motion = self.pictograph.get.trailing_motion()
        if leading_motion:
            return f"({leading_motion.turns}, {trailing_motion.turns})"
        else:
            return f"({self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"