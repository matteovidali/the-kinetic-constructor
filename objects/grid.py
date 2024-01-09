import json
from typing import TYPE_CHECKING, List, Dict, Union
from xml.etree import ElementTree as ET
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtGui import QTransform
from PyQt6.QtWidgets import QGraphicsSceneWheelEvent
from typing import Dict, Literal
from PyQt6.QtCore import QPointF, QEvent
from constants import (
    BOX,
    DIAMOND,
    GRID_DIR,
    NORTH,
    EAST,
    NORTHEAST,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    WEST,
)
from utilities.TypeChecking.TypeChecking import GridModes

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )
    from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import (
        PropBox,
    )
    from objects.pictograph.pictograph import Pictograph


class GridItem(QGraphicsSvgItem):
    def __init__(self, path) -> None:
        super().__init__(path)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(100)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent | None) -> None:
        return super().wheelEvent(event)

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()


class Grid:
    def __init__(self, grid_scene: Union["ArrowBox", "PropBox", "Pictograph"]) -> None:
        self.items = {}
        self.grid_mode = DIAMOND
        self.circle_coordinates_cache = self._load_circle_coordinates()
        self._create_grid_items(grid_scene)
        self.center = self.circle_coordinates_cache["center_point"]

    def _load_circle_coordinates(self) -> Dict[str, str | Dict[str, str | Dict[str, Dict[str, str]]]]:
        # Load the JSON file containing the circle coordinates
        with open("F:\\CODE\\tka-app\\tka-sequence-constructor\\data\\circle_coords.json", "r") as file:
            data: Dict[str, Union[str,Dict[str, Union[str, Dict[str, Dict[str, str]]]]]] = json.load(file)
        # Convert string coordinates to QPointF
        for section, values in data.items():
            if section in ["hand_points", "layer2_points", "outer_points"]:
                for mode, types in values.items():
                    # if types is a dict
                    if isinstance(types, dict):
                        for type_name, points in types.items():
                            for point_id, coords in points.items():
                                x, y = map(float, coords.strip("()").split(", "))
                                data[section][mode][type_name][point_id] = QPointF(x, y)
            elif section == "center_point":
                x, y = map(float, data[section].strip("()").split(", "))
                data[section] = QPointF(x, y)
        return data

    def _create_grid_items(self, grid_scene: "Pictograph") -> None:
        # Paths for each grid mode
        paths = {
            DIAMOND: f"{GRID_DIR}diamond_grid.svg",
            BOX: f"{GRID_DIR}box_grid.svg",
        }

        for mode, path in paths.items():
            item = GridItem(path)
            grid_scene.addItem(item)
            self.items[mode] = item
            # Set initial visibility based on the grid mode
            item.setVisible(mode == self.grid_mode)

    def _get_svg_file_path(self, circle_id: str) -> str:
        # Check if SVG file path is cached
        if circle_id in self.svg_file_path_cache:
            return self.svg_file_path_cache[circle_id]

        # Determine the correct SVG file based on the circle ID
        if "diamond" in circle_id or "center" in circle_id or "outer" in circle_id:
            path = f"{GRID_DIR}diamond_grid.svg"
        elif "box" in circle_id:
            path = f"{GRID_DIR}box_grid.svg"

        self.svg_file_path_cache[circle_id] = path
        return path

    def setPos(self, position: QPointF) -> None:
        for item in self.items.values():
            item.setPos(position)

    def scale_grid(self, scale_factor: float) -> None:
        grid_center = QPointF(self.grid_scene.width() / 2, self.grid_scene.height() / 2)
        for item in self.items.values():
            item.setTransform(QTransform())
            item_center = item.boundingRect().center()
            transform = (
                QTransform()
                .translate(item_center.x(), item_center.y())
                .scale(scale_factor, scale_factor)
                .translate(-item_center.x(), -item_center.y())
            )
            item.setTransform(transform)
            relative_pos = (item.pos() - grid_center) * scale_factor
            item.setPos(grid_center + relative_pos - item_center * scale_factor)

    def toggle_element_visibility(self, element_id: str, visible: bool) -> None:
        if element_id in self.items:
            self.items[element_id].setVisible(visible)

    def toggle_grid_mode(self, grid_mode: GridModes) -> None:
        self.grid_mode = grid_mode
        self.items[DIAMOND].setVisible(grid_mode == DIAMOND)
        self.items[BOX].setVisible(grid_mode == BOX)

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()  # Ignore the event to let it propagate
        return False  # Return False to continue event propagation
