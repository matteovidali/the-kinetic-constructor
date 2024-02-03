
from constants import *
from .base_location_calculator import BaseLocationCalculator

class ShiftLocationCalculator(BaseLocationCalculator):
    def calculate_location(self) -> str:
        direction_pairs = {
            frozenset({NORTH, EAST}): NORTHEAST,
            frozenset({EAST, SOUTH}): SOUTHEAST,
            frozenset({SOUTH, WEST}): SOUTHWEST,
            frozenset({WEST, NORTH}): NORTHWEST,
        }
        return direction_pairs.get(
            frozenset({self.arrow.motion.start_loc, self.arrow.motion.end_loc}), ""
        )
