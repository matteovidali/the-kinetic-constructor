from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import ReversalDetector


class ReversalProcessor:
    """Class to process reversals and update pictographs."""

    @staticmethod
    def process_reversals(sequence: list[dict], filled_beats: list["BeatView"]) -> None:
        """Process reversals and update pictographs before drawing."""
        sequence_so_far = []
        for i, (beat_dict, beat_view) in enumerate(zip(sequence[2:], filled_beats)):
            filtered_sequence_so_far = [
                beat
                for beat in sequence_so_far
                if not beat.get("sequence_start_position") and not beat.get("is_placeholder", False)
            ]

            # Detect reversal
            reversal_info = ReversalDetector.detect_reversal(
                filtered_sequence_so_far, beat_dict
            )

            # Access the pictograph from the beat_view
            pictograph = beat_view.beat

            # Reset reversal flags
            pictograph.blue_reversal = False
            pictograph.red_reversal = False

            # Set reversal flags based on detection
            pictograph.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.red_reversal = reversal_info.get("red_reversal", False)

            # Debug output to track reversal detection
            print(f"Reversal detected - Beat {i}: Blue: {pictograph.blue_reversal}, Red: {pictograph.red_reversal}")

            # Update the reversal symbols on the pictograph
            pictograph.reversal_symbol_manager.update_reversal_symbols()

            # Ensure beat_view reflects the changes
            beat_view.update()
            beat_view.repaint()

            # Add this beat to the processed sequence
            sequence_so_far.append(beat_dict)
