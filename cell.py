from line import Line
from point import Point
from window import Window
from enum import Enum
from wall import Wall

class WallType(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

class Cell():
    def __init__(self, window: Window, top_left_point: Point, cell_size: float, has_left_wall: bool = True, has_right_wall: bool = True, has_top_wall: bool = True, has_bottom_wall: bool = True ):
        self._win = window
        self._cell_center_point = top_left_point + (cell_size / 2)
        top_right_point = Point(top_left_point.x + cell_size, top_left_point.y)
        bottom_left_point = Point(top_left_point.x, top_left_point.y + cell_size)
        bottom_right_point = Point(top_left_point.x + cell_size, top_left_point.y + cell_size)
        self.walls = { WallType.TOP: Wall(window, self, Line(top_left_point, top_right_point), has_top_wall),
                       WallType.RIGHT: Wall(window, self, Line(top_right_point, bottom_right_point), has_right_wall),
                       WallType.BOTTOM: Wall(window, self, Line(bottom_right_point, bottom_left_point), has_bottom_wall),
                       WallType.LEFT: Wall(window, self, Line(bottom_left_point, top_left_point), has_left_wall)}

    def draw(self):
        for wall in self.walls.values():
            wall.draw()

    def connect_to(self, cell_right: "Cell", cell_below: "Cell"):
        self.walls[WallType.RIGHT].connect_to_cell(cell_right)
        cell_right.walls[WallType.LEFT] = self.walls[WallType.RIGHT]
        self.walls[WallType.BOTTOM].connect_to_cell(cell_below)
        cell_below.walls[WallType.TOP] = self.walls[WallType.BOTTOM]

    def draw_move(self, to_cell: WallType, undo: bool = False):
        self._win.draw_line(Line(self._cell_center_point, self.walls[to_cell].go(self)._cell_center_point), "grey" if undo else "red")