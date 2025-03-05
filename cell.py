from line import Line
from rectangle import Rectangle
from point import Point
from window import Window
from enum import Enum
from constants import *

class WallType(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
    def opposite(dir : "WallType"):
        return WallType._value2member_map_[(dir.value + 2) % 4]

class CellState(Enum):
    UNUSED = "Unused"
    WALKED = "Walked"
    ACTIVE = "Active"
    START = "Start"
    END = "End"


class Cell():
    class Wall():
        def __init__(self, window: Window, cell: "Cell", line: Line, connect_dir: WallType, show_wall: bool = True):
            self.__window = window
            self.__line = line
            self.show = show_wall
            self.cells = {connect_dir.opposite(): cell}
        
        def __repr__(self):
            return f"Wall({self.cells.keys()}, {('Visible' if self.show else 'Hidden') + (' exterior' if self.is_exterior() else ' interior')})"
        
        def draw(self): 
            self.__line.width = EXTERIOR_WALL_WIDTH if self.is_exterior() else WALL_WIDTH
            color = (EXTERIOR_WALL_COLOR if self.is_exterior() else WALL_COLOR) if self.show else BACKGROUND_COLOR
            self.__window.draw_line(self.__line, color)

        def connect_to_cell(self, cell: "Cell", connect_dir: WallType):
            self.cells[connect_dir.opposite()] = cell

        def go(self, direction: WallType) -> "Cell":
            return self.cells[direction]
        
        def is_exterior(self):
            return len(self.cells) < 2

    __SOLITARY_CELL_STATES = {CellState.ACTIVE, CellState.UNUSED, CellState.WALKED}
    __CELL_STATE_COLORS = {CellState.ACTIVE: (CELL_ACTIVE_COLOR, CELL_ACTIVE_BORDER, WALL_COLOR),
                           CellState.END: (CELL_END_FILL, CELL_END_BORDER, WALL_COLOR),
                           CellState.START: (CELL_START_FILL, CELL_START_BORDER, WALL_COLOR),
                           CellState.UNUSED: (CELL_UNUSED_COLOR, CELL_UNUSED_BORDER, CELL_UNUSED_BORDER),
                           CellState.WALKED: (CELL_WALKED_FILL, CELL_WALKED_BORDER, CELL_WALKED_BORDER)}

    def __init__(self, window: Window, top_left_point: Point, cell_size: float, has_left_wall: bool = True, has_right_wall: bool = True, has_top_wall: bool = True, has_bottom_wall: bool = True ):
        self._win = window
        self.grid_pos = (int((top_left_point.x - (top_left_point.x % cell_size)) / cell_size), int((top_left_point.y - (top_left_point.y % cell_size)) / cell_size))
        self.state = {CellState.UNUSED}
        self.fill_color, self.cell_border_color, self.wall_color = Cell.__CELL_STATE_COLORS[self.state]
        self._cell_center_point = top_left_point + (cell_size / 2)
        top_right_point = Point(top_left_point.x + cell_size, top_left_point.y)
        bottom_left_point = Point(top_left_point.x, top_left_point.y + cell_size)
        bottom_right_point = Point(top_left_point.x + cell_size, top_left_point.y + cell_size)
        self.walls = { WallType.TOP: Cell.Wall(window, self, Line(top_left_point, top_right_point), WallType.TOP, has_top_wall),
                       WallType.RIGHT: Cell.Wall(window, self, Line(top_right_point, bottom_right_point), WallType.RIGHT, has_right_wall),
                       WallType.BOTTOM: Cell.Wall(window, self, Line(bottom_right_point, bottom_left_point), WallType.BOTTOM, has_bottom_wall),
                       WallType.LEFT: Cell.Wall(window, self, Line(bottom_left_point, top_left_point), WallType.LEFT, has_left_wall)}
        self.body = Rectangle(top_left_point, bottom_right_point, self.fill_color, self.cell_border_color, CELL_BORDER_WIDTH)
    def __eq__(self, value : "Cell"):
        return self.grid_pos == value.grid_pos and self.state == value.state and self.walls == value.walls
    
    def __repr__(self):
        return f"Cell({self.grid_pos}, {self.state}, {self.walls})"
    
    def choices(self, include_all: bool = False) -> list[tuple[WallType, Wall]]:
        return [(wall, dir) for dir, wall in self.walls.items() if ((not wall.show) or include_all) and not wall.is_exterior()]
    
    def clear_all_walls(self):
        for wall in self.walls.values():
            if not wall.is_exterior(): wall.show = False

    def raise_all_walls(self):
        for wall in self.walls.values():
            if not wall.is_exterior(): wall.show = True

    def draw(self):
        state = CellState.UNUSED
        if CellState.START in self.state:
            state = CellState.START
        elif CellState.END in self.state:
            state = CellState.END
        else:
            state = self.state.pop()
            self.state.add(state)

        self._win.draw_rectangle(self.body, *Cell.__CELL_STATE_COLORS[state])
        draw_all = state in {CellState.ACTIVE, CellState.END, CellState.START}
        for wall in self.walls.values():
            if draw_all or wall.is_exterior(): wall.draw()

    def add_state(self, cell_state: CellState):
        if cell_state in Cell.__SOLITARY_CELL_STATES: 
            self.state -= Cell.__SOLITARY_CELL_STATES
        self.state.add(cell_state)

    def connect_to(self, cell_right: "Cell", cell_below: "Cell"):
        if cell_right is not None:
            self.walls[WallType.RIGHT].connect_to_cell(cell_right, WallType.LEFT)
            cell_right.walls[WallType.LEFT] = self.walls[WallType.RIGHT]
        if cell_below is not None:
            self.walls[WallType.BOTTOM].connect_to_cell(cell_below, WallType.TOP)
            cell_below.walls[WallType.TOP] = self.walls[WallType.BOTTOM]

    def draw_move(self, to_cell: WallType, undo: bool = False):
        self._win.draw_line(Line(self._cell_center_point, self.walls[to_cell].go(to_cell)._cell_center_point, width=WALK_WIDTH), WALKBACK_COLOR if undo else WALK_COLOR)

