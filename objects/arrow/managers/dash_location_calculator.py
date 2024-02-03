from constants import *
from utilities.TypeChecking.MotionAttributes import Locations
from .base_location_calculator import BaseLocationCalculator


class DashLocationCalculator(BaseLocationCalculator):
    def calculate_location(self) -> str:
        if self.arrow.pictograph.letter in ["Φ-", "Ψ-"]:
            return self._get_Φ_dash_Ψ_dash_location()
        elif (
            self.arrow.pictograph.letter in ["Λ", "Λ-"] and self.arrow.motion.turns == 0
        ):
            return self._get_Λ_zero_turns_location()
        elif self.arrow.motion.turns == 0:
            return self._default_zero_turns_dash_location()
        else:
            return self._dash_location_non_zero_turns()

    def _get_Φ_dash_Ψ_dash_location(self) -> Locations:
        self.other_motion = self.arrow.pictograph.get.other_motion(self.arrow.motion)
        if self.arrow.motion.turns == 0 and self.other_motion.turns == 0:
            location_map = {
                (RED, (NORTH, SOUTH)): EAST,
                (RED, (EAST, WEST)): NORTH,
                (RED, (SOUTH, NORTH)): EAST,
                (RED, (WEST, EAST)): NORTH,
                (BLUE, (NORTH, SOUTH)): WEST,
                (BLUE, (EAST, WEST)): SOUTH,
                (BLUE, (SOUTH, NORTH)): WEST,
                (BLUE, (WEST, EAST)): SOUTH,
            }
            arrow_location = location_map.get(
                (
                    self.arrow.color,
                    (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                )
            )
            return arrow_location

        elif self.arrow.motion.turns == 0:
            return self.arrow.pictograph.get.opposite_location(
                self._dash_location_non_zero_turns()
            )
        elif self.arrow.motion.turns != 0:
            return self._dash_location_non_zero_turns()

    def _get_Λ_zero_turns_location(self) -> Locations:
        loc_map = {
            ((NORTH, SOUTH), WEST): EAST,
            ((EAST, WEST), SOUTH): NORTH,
            ((NORTH, SOUTH), EAST): WEST,
            ((WEST, EAST), SOUTH): NORTH,
            ((SOUTH, NORTH), WEST): EAST,
            ((EAST, WEST), NORTH): SOUTH,
            ((SOUTH, NORTH), EAST): WEST,
            ((WEST, EAST), NORTH): SOUTH,
        }
        arrow_location = loc_map.get(
            (
                (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                (self.other_motion.end_loc),
            )
        )
        return arrow_location

    def _default_zero_turns_dash_location(self) -> str:
        location_map = {
            (NORTH, SOUTH): EAST,
            (EAST, WEST): SOUTH,
            (SOUTH, NORTH): WEST,
            (WEST, EAST): NORTH,
        }
        return location_map.get(
            (self.arrow.motion.start_loc, self.arrow.motion.end_loc), ""
        )

    def _dash_location_non_zero_turns(self) -> str:
        loc_map = {
            CLOCKWISE: {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH},
            COUNTER_CLOCKWISE: {NORTH: WEST, EAST: NORTH, SOUTH: EAST, WEST: SOUTH},
        }
        return loc_map[self.arrow.motion.prop_rot_dir].get(
            self.arrow.motion.start_loc, ""
        )

    def _calculate_dash_location_based_on_shift(self) -> str:
        shift_arrow = self.arrow.pictograph.get.other_motion(self.arrow.motion).arrow
        shift_location = shift_arrow.loc
        dash_location_map = {
            (NORTH, NORTHWEST): EAST,
            (NORTH, NORTHEAST): WEST,
            (NORTH, SOUTHEAST): WEST,
            (NORTH, SOUTHWEST): EAST,
            (EAST, NORTHWEST): SOUTH,
            (EAST, NORTHEAST): SOUTH,
            (EAST, SOUTHEAST): NORTH,
            (EAST, SOUTHWEST): NORTH,
            (SOUTH, NORTHWEST): EAST,
            (SOUTH, NORTHEAST): WEST,
            (SOUTH, SOUTHEAST): WEST,
            (SOUTH, SOUTHWEST): EAST,
            (WEST, NORTHWEST): SOUTH,
            (WEST, NORTHEAST): SOUTH,
            (WEST, SOUTHEAST): NORTH,
            (WEST, SOUTHWEST): NORTH,
        }
        return dash_location_map.get((self.arrow.motion.start_loc, shift_location), "")
