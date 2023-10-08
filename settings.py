class Settings():
    SCALE_FACTOR = 1
    Second_Screen = False
    

STAFF_WIDTH = 25
STAFF_LENGTH = 250

MINI_STAFF_WIDTH = 12.5
MINI_STAFF_LENGTH = 125

RED = '#ed1c24'
BLUE = '#2e3192'

class Graphboard_Constants:
    def __init__(self, graphboard):
        self.graphboard = graphboard
        self.VERTICAL_OFFSET = (self.graphboard.height() - self.graphboard.width()) / 2