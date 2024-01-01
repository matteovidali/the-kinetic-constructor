from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QWidget,
    QComboBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from typing import TYPE_CHECKING, List
from objects.motion.motion import Motion
from constants import CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON, ICON_DIR
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)

from widgets.graph_editor_tab.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_attr_box import IGAttrBox
    from widgets.graph_editor_tab.attr_panel.bast_attr_box import BaseAttrBox
    from widgets.graph_editor_tab.attr_panel.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )


class IGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "IGAttrBox") -> None:
        super().__init__(attr_box)
        self._initialize_ui()

    def _initialize_ui(self) -> None:
        super()._initialize_ui() 
        self.turnbox_hbox_frame: QFrame = self._create_turnbox_hbox_frame()
        self._setup_layout_frames()

    ### LAYOUTS ###



    def _setup_layouts(self) -> None:
        """Sets up the main and auxiliary layouts for the widget."""
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.header_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def _setup_layout_frames(self) -> None:
        """Adds the header and buttons to their respective frames."""
        self.header_layout.addWidget(self.turnbox_hbox_frame)

        self._add_widgets_to_layout(self.buttons, self.buttons_layout)

        self.header_frame = self._create_frame(self.header_layout)
        self.button_frame = self._create_frame(self.buttons_layout)

        self.layout.addWidget(self.header_frame)
        self.layout.addWidget(self.button_frame)



    ### WIDGETS ###

    def _create_clock_labels(self) -> None:
        """Creates and configures the clock labels for rotation direction."""
        self.clock_left, self.clock_right = QLabel(), QLabel()
        for clock in [self.clock_left, self.clock_right]:
            clock.setLayout(QVBoxLayout())
            clock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            clock.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

    def _create_turnbox_hbox_frame(self) -> None:
        """Creates the turns box and buttons for turn adjustments."""

        self.turnbox.currentTextChanged.connect(self._update_turns)
        self.buttons = [
            self._create_turns_button(text) for text in ["-1", "-0.5", "+0.5", "+1"]
        ]
        turnbox_frame = QFrame(self)

        turnbox_frame.setLayout(QHBoxLayout())

        self.header_label = QLabel("Turns")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turnbox_frame.layout().addWidget(self.header_label)
        turnbox_frame.layout().addWidget(self.turnbox)
        turnbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        turnbox_frame.layout().setContentsMargins(0, 0, 0, 0)
        turnbox_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().setSpacing(0)
        return turnbox_frame


    def _create_clock_pixmap(self, icon_path: str) -> QPixmap:
        """Load and scale a clock pixmap based on the initial size."""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Failed to load the icon from {icon_path}.")
            return QPixmap()
        return pixmap


    ### CALLBACKS ###




    ## UPDATE THESE TO WORK ON ALL PICTOGRAPHS IN THE SCROLL AREA

    def _add_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.add_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.subtract_turn()
            self.attr_box.update_attr_box(motion)

    def _add_half_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.add_half_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_half_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.subtract_half_turn()
            self.attr_box.update_attr_box(motion)

    ### UPDATE METHODS ###

    def update_turnbox(self, turns) -> None:
        turns_str = str(turns)
        for i in range(self.turnbox.count()):
            if self.turnbox.itemText(i) == turns_str:
                self.turnbox.setCurrentIndex(i)
                return
            elif turns == None:
                self.turnbox.setCurrentIndex(-1)

    def _update_turns(self, index: int) -> None:
        turns = str(index)
        if turns == "0" or turns == "1" or turns == "2" or turns == "3":
            motion: Motion = self.attr_box.pictograph.motions[self.attr_box.color]
            if motion and motion.arrow:
                if int(turns) != motion.turns:
                    motion.update_turns(int(turns))
                    self.attr_box.update_attr_box(motion)
                    self.attr_box.pictograph.update()
        elif turns == "0.5" or turns == "1.5" or turns == "2.5":
            motion: Motion = self.attr_box.pictograph.motions[self.attr_box.color]
            if motion:
                if float(turns) != motion.turns:
                    motion.update_turns(float(turns))
                    self.attr_box.update_attr_box(motion)
                    self.attr_box.pictograph.update()
        else:
            self.turnbox.setCurrentIndex(-1)

    ### EVENT HANDLERS ###

    def _update_widget_sizes(self) -> None:
        """Updates the sizes of the widgets based on the widget's size."""
        available_height = self.height()
        header_height = int(available_height * 2 / 3)
        turns_widget_height = int(available_height * 1 / 3)
        self.header_frame.setMaximumHeight(header_height)
        # self.button_frame.setMaximumHeight(self.button_frame.height())



    def _update_turnbox_size(self) -> None:
        self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

        self.spacing = self.attr_box.attr_panel.width() // 250

        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 3.25))

        self.turnbox.setMinimumHeight(int(self.attr_box.height() / 8))
        self.turnbox.setMaximumHeight(int(self.attr_box.height() / 8))
        box_font_size = int(self.attr_box.width() / 10)

        self.header_label.setContentsMargins(0, 0, self.spacing, 0)
        self.header_label.setFont(QFont("Arial", int(self.width() / 22)))

        self.turnbox.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow

        # Calculate the border radius as a fraction of the width or height
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25

        # Adjust the stylesheet to add padding inside the combo box on the left
        self.turnbox.setStyleSheet(
            f"""
            QComboBox {{
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 0px; /* make room for the arrow on the right */
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: {dropdown_arrow_width}px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* visually separate the arrow part */
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
            }}
            QComboBox::down-arrow {{
                image: url("{ICON_DIR}/combobox_arrow.png");
                width: {int(dropdown_arrow_width * 0.6)}px;
                height: {int(dropdown_arrow_width * 0.6)}px;
            }}
        """
        )
        self.turnbox_hbox_frame.setMinimumWidth(int(self.attr_box.width() / 3.25))
        self.turnbox_hbox_frame.setMaximumWidth(int(self.attr_box.width() / 3.25))

    def _update_button_size(self) -> None:
        for button in self.buttons:
            button_size = int(self.attr_box.width() / 7)
            if button.text() == "-0.5" or button.text() == "+0.5":
                button_size = int(button_size * 0.85)
            else:
                button_size = int(self.attr_box.width() / 6)
            button.update_custom_button_size(button_size)

    def resize_turns_widget(self):
        self._update_turnbox_size()
        self._update_button_size()
