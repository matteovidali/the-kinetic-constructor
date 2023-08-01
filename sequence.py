from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QPushButton
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView
from PyQt5.QtCore import Qt, QPointF
from arrow import Arrow
from graphboard import Graphboard
from grid import Grid
from pictograph import Pictograph
from PyQt5.QtGui import QImage, QPainter
from staff import Staff

class Sequence_Manager:
    def __init__(self, scene, pictograph_generator, ui_setup, info_tracker):
        self.graphboard_scene = scene
        self.beats = [QGraphicsRectItem(QRectF(375, 0, 375, 375)) for i in range(4)]
        for i, section in enumerate(self.beats):
            # add a small buffer and update the x position
            section.setPos(QPointF(i * 375, 0))

        self.pictographs = [] 
        self.pictograph_generator = pictograph_generator
        self.ui_setup = ui_setup
        self.info_tracker = info_tracker

    def add_pictograph(self, pictograph):
        print("Adding pictograph")

        # Find the first section that doesn't have a pictograph
        for i, section in enumerate(self.beats):
            if i >= len(self.pictographs):
                pictograph.setPos(section.pos())
                self.pictographs.append(pictograph)
                self.graphboard_scene.addItem(pictograph)
                break

        print("Items in the scene:")
        for item in self.graphboard_scene.items():
            print(item)

    def add_to_sequence(self, graphboard):
        # Create a QImage to render the scene
        image = QImage(graphboard.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)

        graphboard.print_item_types()

        # deselect all items
        graphboard.clear_selection()

        # Render the scene
        graphboard.render(painter)
        painter.end()

        scaled_image = image.scaled(375, 375, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pictograph = Pictograph(graphboard.get_state(), scaled_image)
        print(pictograph.state)
        self.add_pictograph(pictograph)
        graphboard.clear()

        letter = self.info_tracker.get_current_letter()
        self.ui_setup.word_label.setText(self.ui_setup.word_label.text() + letter)

    def add_to_graphboard(self, pictograph: Pictograph, graphboard: Graphboard):
        state = pictograph.state
        graphboard.clear()
        
        for arrow_state in state['arrows']:
            arrow = Arrow(arrow_state['svg_file'])
            arrow.setPos(arrow_state['position'])
            arrow.setRotation(arrow_state['rotation'])
            arrow.color = arrow_state['color']
            arrow.quadrant = arrow_state['quadrant']
            graphboard.scene().addItem(arrow)

        for staff_state in state['staffs']:
            staff = Staff(staff_state['svg_file'])
            staff.setPos(staff_state['position'])
            staff.color = staff_state['color']
            graphboard.scene().addItem(staff)

        if state['grid']:
            grid = Grid(state['grid']['svg_file'])
            grid.setPos(state['grid']['position'])
            graphboard.scene().addItem(grid)

    def get_clear_sequence_button(self):
        self.clear_button = QPushButton("Clear Sequence")
        self.clear_button.clicked.connect(self.clear_sequence)
        return self.clear_button

    def clear_sequence(self):
        self.pictographs = []
        for item in self.graphboard_scene.items():
            self.graphboard_scene.removeItem(item)
        self.ui_setup.word_label.setText("My word: ")

class Sequence_Scene(QGraphicsScene):
    def __init__(self, manager=None, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 4 * 375, 375)

    def set_manager(self, manager):
        self.manager = manager

