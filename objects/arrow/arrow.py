from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
import re
from settings.string_constants import *
from data.start_end_location_mapping import start_end_location_mapping
from settings.numerical_constants import GRAPHBOARD_SCALE

class Arrow(QGraphicsSvgItem):
    def __init__(self, graphboard, attributes):
        super().__init__()
        if attributes:
            self.svg_file = self.get_svg_file(
                attributes.get(MOTION_TYPE), attributes.get(TURNS)
            )
            self.setup_svg_renderer(self.svg_file)
        self.setup_attributes(graphboard, attributes)
        self.setup_graphics_flags()

    ### SETUP ###

    def setup_attributes(self, graphboard, attributes):
        self.graphboard = graphboard
        if hasattr(graphboard, "infobox"):
            self.infobox = graphboard.infobox

        self.in_graphboard = False
        self.drag_offset = QPointF(0, 0)
        self.is_still = False
        self.staff = None
        self.is_mirrored = False
        self.previous_arrow = None

        self.color = None
        self.motion_type = None
        self.rotation_direction = None
        self.quadrant = None
        self.start_location = None
        self.end_location = None
        self.turns = None

        if attributes:
            self.update_attributes(attributes)
            self.update_appearance()
        self.center = self.boundingRect().center()

    def setup_graphics_flags(self):
        flags = [
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
            QGraphicsItem.GraphicsItemFlag.ItemIsFocusable,
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable,
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable,
        ]

        for flag in flags:
            self.setFlag(flag, True)

        self.setTransformOriginPoint(self.center)

    def setup_svg_renderer(self, svg_file):
        self.renderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.setSelected(True)

        for arrow in self.graphboard.arrows:
            if arrow != self:
                arrow.setSelected(False)

        self.drag_start_pos = self.pos()
        self.drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            scene_event_pos = self.mapToScene(event.pos())
            view_event_pos = self.graphboard.view.mapFromScene(scene_event_pos)
            in_view = self.graphboard.view.rect().contains(view_event_pos)
            new_pos = self.mapToScene(event.pos()) - self.boundingRect().center()
            self.setPos(new_pos)

            scene_pos = new_pos + self.center
            new_quadrant = self.graphboard.determine_quadrant(
                scene_pos.x(), scene_pos.y()
            )

            if self.quadrant != new_quadrant:
                if in_view:
                    self.update_for_new_quadrant(new_quadrant)

    def mouseReleaseEvent(self, event):
        self.graphboard.arrow_positioner.update_arrow_positions()

    ### GETTERS ###

    def get_svg_data(self, svg_file):
        with open(svg_file, CLOCKWISE) as f:
            svg_data = f.read()
        return svg_data.encode("utf-8")

    def get_rotation_angle(self, quadrant, motion_type, rotation_direction):
        quadrant_to_angle = self.get_quadrant_to_angle_map(
            motion_type, rotation_direction
        )
        return quadrant_to_angle.get(quadrant, 0)

    def get_quadrant_to_angle_map(self, motion_type, rotation_direction):
        if motion_type == PRO:
            return {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
            }.get(rotation_direction, {})
        elif motion_type == ANTI:
            return {
                CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            }.get(rotation_direction, {})
        elif motion_type == STATIC:
            return {
                CLOCKWISE: {NORTHEAST: 0, SOUTHEAST: 0, SOUTHWEST: 0, NORTHWEST: 0},
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 0,
                    SOUTHWEST: 0,
                    NORTHWEST: 0,
                },
            }.get(rotation_direction, {})

    def get_svg_file(self, attributes):
        if attributes:
            motion_type = attributes[MOTION_TYPE]
            turns = attributes.get(TURNS, None)

            if motion_type in [PRO, ANTI]:
                self.is_shift = True
                return SHIFT_DIR + motion_type + "_" + str(turns) + ".svg"
            elif motion_type in [STATIC]:
                self.is_static = True
                return None

    def get_attributes(self):
        return {attr: getattr(self, attr) for attr in ARROW_ATTRIBUTES}

    def get_start_end_locations(self, motion_type, rotation_direction, quadrant):
        return (
            start_end_location_mapping.get(quadrant, {})
            .get(rotation_direction, {})
            .get(motion_type, (None, None))
        )

    ### UPDATERS ###

    def update(self, attributes):
        self.update_attributes(attributes)
        self.update_appearance()
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)

    def update_appearance(self):
        self.update_color()
        self.update_rotation()

    def update_color(self):
        if self.motion_type in [PRO, ANTI]:
            new_svg_data = self.set_svg_color(self.svg_file, self.color)
            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)

    def update_rotation(self):
        angle = self.get_rotation_angle(
            self.quadrant, self.motion_type, self.rotation_direction
        )
        self.setRotation(angle)



    def update_attributes(self, attributes):
        for attr in ARROW_ATTRIBUTES:
            value = attributes.get(attr)
            if attr == TURNS:
                value = int(value)
            setattr(self, attr, value)

        self.attributes = {
            COLOR: attributes.get(COLOR, None),
            MOTION_TYPE: attributes.get(MOTION_TYPE, None),
            ROTATION_DIRECTION: attributes.get(ROTATION_DIRECTION, None),
            QUADRANT: attributes.get(QUADRANT, None),
            START_LOCATION: attributes.get(START_LOCATION, None),
            END_LOCATION: attributes.get(END_LOCATION, None),
            TURNS: attributes.get(TURNS, None),
        }

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self.setup_svg_renderer(svg_file)

    def get_svg_file(self, motion_type, turns):
        svg_file = f"{SHIFT_DIR}{motion_type}_{turns}.svg"
        return svg_file

    def update_for_new_quadrant(self, new_quadrant):
        self.quadrant = new_quadrant
        self.start_location, self.end_location = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )
        self.update_appearance()
        self.staff.location = self.end_location
        self.staff.update_attributes_from_arrow(self)
        self.graphboard.update()

    ### MANIPULATION ###

    def increment_turns(self):
        self.turns += 1
        if self.turns > 2:
            self.turns = 0
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.graphboard.update()

    def decrement_turns(self):
        self.turns -= 1
        if self.turns < 0:
            self.turns = 2
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.graphboard.update()

    def set_svg_color(self, svg_file, new_color):
        color_map = {RED: RED_HEX, BLUE: BLUE_HEX}
        new_hex_color = color_map.get(new_color)

        with open(svg_file, CLOCKWISE) as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)
        return svg_data.encode("utf-8")


class BlankArrow(Arrow):
    # init an arrow that is blank but carries the properties
    # of the arrow that was deleted
    def __init__(self, graphboard, attributes):
        super().__init__(graphboard, attributes)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.hide()


class GhostArrow(Arrow):
    def __init__(self, graphboard, attributes):
        super().__init__(graphboard, attributes)
        self.setOpacity(0.2)
        self.setTransformOriginPoint(self.center)

