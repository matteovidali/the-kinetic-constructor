from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from settings.numerical_constants import GRAPHBOARD_SCALE
from settings.string_constants import *


class DragPreview(QWidget):
    def __init__(self, drag, target_arrow):
        super().__init__()

        self.drag = drag
        self.main_window = drag.main_window
        self.graphboard = drag.graphboard
        self.target_arrow = target_arrow
        pixmap = self.create_pixmap(target_arrow)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.setFixedHeight(pixmap.height())
        self.label.setPixmap(pixmap)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.center = pixmap.rect().center() * GRAPHBOARD_SCALE

        self.color = target_arrow.color
        self.motion_type = target_arrow.motion_type
        self.quadrant = target_arrow.quadrant
        self.rotation_direction = target_arrow.rotation_direction
        self.turns = target_arrow.turns

        (
            self.start_location,
            self.end_location,
        ) = target_arrow.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )

        self.in_graphboard = False
        self.has_entered_graphboard_once = False
        self.current_rotation_angle = 0

    def create_pixmap(self, dragged_arrow):
        new_svg_data = dragged_arrow.set_svg_color(
            dragged_arrow.svg_file, dragged_arrow.color
        )
        renderer = QSvgRenderer(new_svg_data)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)
        return pixmap

    def get_attributes(self):
        start_location, end_location = self.target_arrow.attributes.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )

        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: self.quadrant,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: start_location,
            END_LOCATION: end_location,
            TURNS: self.turns,
        }

    def move_to_cursor(self, arrowbox, event_pos, target_arrow):
        local_pos = arrowbox.view.mapTo(self.main_window, event_pos)
        self.move(local_pos - (target_arrow.center).toPoint() * GRAPHBOARD_SCALE)

    def update_rotation_for_quadrant(self, new_quadrant):
        self.in_graphboard = True
        self.quadrant = new_quadrant
        self.rotate()

    def rotate(self):
        renderer = QSvgRenderer(self.target_arrow.svg_file)
        scaled_size = renderer.defaultSize() * GRAPHBOARD_SCALE
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.target_arrow.get_rotation_angle(
            self.quadrant,
            self.motion_type,
            self.rotation_direction,
        )

        unrotate_transform = QTransform().rotate(-self.current_rotation_angle)
        unrotated_pixmap = self.label.pixmap().transformed(unrotate_transform)

        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

        self.current_rotation_angle = angle
        self.label.setPixmap(rotated_pixmap)

        (
            self.start_location,
            self.end_location,
        ) = self.target_arrow.get_start_end_locations(
            self.motion_type,
            self.rotation_direction,
            self.quadrant,
        )

    def delete(self):
        self.deleteLater()
        self = None
