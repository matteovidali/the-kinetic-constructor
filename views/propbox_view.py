from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt
from settings import GRAPHBOARD_SCALE




class PropBox_View(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        self.main_window = main_widget.main_window
        self.staff_manager = main_widget.staff_manager
        self.main_widget = main_widget
                
        self.propbox_scene = QGraphicsScene()
        self.propbox_frame = QFrame(self.main_window)
        self.setScene(self.propbox_scene)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)

        main_widget.propbox_view = self
        main_widget.propbox_scene = self.propbox_scene

        self.propbox_layout = QVBoxLayout()
        self.propbox_frame.setLayout(self.propbox_layout)
        self.propbox_layout.addWidget(self)
        self.propbox_frame.setFixedSize(int(500 * GRAPHBOARD_SCALE), int(400 * GRAPHBOARD_SCALE))

        

