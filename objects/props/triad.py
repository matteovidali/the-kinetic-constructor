import logging
from objects.props.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from objects.arrow import Arrow
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
from settings.string_constants import TRIAD_SVG_FILE_PATH

logging.basicConfig(
    filename="logs/staff.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


class Triad(Prop):
    arrow: "Arrow"
    svg_file: str

    def __init__(
        self,
        main_widget: "MainWidget",
        graphboard: "GraphBoard",
        attributes,
    ) -> None:
        svg_file = TRIAD_SVG_FILE_PATH
        super().__init__(main_widget, graphboard, svg_file, attributes)
        self._setup_attributes(main_widget, graphboard, attributes)
