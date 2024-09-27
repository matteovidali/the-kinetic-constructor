from data.constants import *
from objects.motion.managers.handpath_calculator import (
    HandpathCalculator,
)
from .base_rot_angle_calculator import BaseRotAngleCalculator


class FloatRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
        direction_map = self._float_direction_map()
        loc = self.arrow.loc
        handpath_direction = self.handpath_calculator.get_hand_rot_dir_from_locs(
            self.arrow.motion.start_loc, self.arrow.motion.end_loc
        )
        return direction_map.get(handpath_direction, {}).get(loc, 0)

    def _float_direction_map(self):
        return {
            CLOCKWISE: {
                NORTH: 315,
                EAST: 45,
                SOUTH: 135,
                WEST: 225,
                NORTHEAST: 0,
                SOUTHEAST: 90,
                SOUTHWEST: 180,
                NORTHWEST: 270,
            },
            COUNTER_CLOCKWISE: {
                NORTH: 315,
                EAST: 225,
                SOUTH: 135,
                WEST: 45,
                NORTHEAST: 180,
                SOUTHEAST: 270,
                SOUTHWEST: 0,
                NORTHWEST: 90,
            },
        }
