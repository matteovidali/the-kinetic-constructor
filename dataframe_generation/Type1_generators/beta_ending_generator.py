from typing import Dict, List
from df_generator import DataFrameGenerator
from data.constants import *


class BetaEndingGenerator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["G", "H", "I", "J", "K", "L"])
        self.create_dataframes_for_beta_ending()

    def create_dataframes_for_beta_ending(self) -> None:
        for letter in self.letters:
            data = self.create_dataframe(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_dataframe(self, letter) -> List[Dict]:
        if letter in ["G", "J"]:
            return self.create_dataframes_for_letter(letter, "pro", "pro")
        elif letter in ["H", "K"]:
            return self.create_dataframes_for_letter(letter, "anti", "anti")
        elif letter in ["I", "L"]:
            data = self.create_dataframes_for_letter(letter, "pro", "anti")
            data += self.create_dataframes_for_letter(letter, "anti", "pro")
            return data

    def create_dataframes_for_letter(
        self, letter, red_motion_type, blue_motion_type
    ) -> List[Dict]:
        data = []
        handpath_tuple_map_collection = self.get_handpath_tuple_map_collection()

        for handpath, values in handpath_tuple_map_collection.items():
            handpath_tuples = handpath_tuple_map_collection[handpath]
            red_prop_rot_dir = self.get_prop_rot_dir(red_motion_type, handpath)
            if letter in ["G", "H", "L"]:
                blue_prop_rot_dir = red_prop_rot_dir
            elif letter in ["I", "J", "K"]:
                blue_prop_rot_dir = self.get_opposite_rot_dir(red_prop_rot_dir)

            for red_start_loc, red_end_loc in handpath_tuples:
                if letter in ["G", "H", "I"]:
                    blue_start_loc, blue_end_loc = red_start_loc, red_end_loc

                elif letter in ["J", "K", "L"]:
                    blue_start_loc = red_start_loc
                    blue_end_loc = self.get_opposite_location(red_end_loc)

                start_pos, end_pos = self.get_Type1_start_and_end_pos(
                    red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
                )

                data.append(
                    {
                        "letter": letter,
                        "start_position": start_pos,
                        "end_position": end_pos,
                        "blue_motion_type": blue_motion_type,
                        "blue_rot_dir": blue_prop_rot_dir,
                        "blue_start_loc": blue_start_loc,
                        "blue_end_loc": blue_end_loc,
                        "red_motion_type": red_motion_type,
                        "red_rot_dir": red_prop_rot_dir,
                        "red_start_loc": red_start_loc,
                        "red_end_loc": red_end_loc,
                    }
                )

        return data


beta_ending_generator = BetaEndingGenerator()
