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
    
    def __repr__(self):
        return f"{self.name.title()}"
        

class CellState(Enum):
    UNUSED = "Unused"
    WALKED = "Walked"
    ACTIVE = "Active"
    START = "Start"
    END = "End"


class Cell():
    class Wall():
        def __init__(self, window: Window, cell_a: "Cell", cell_b: "Cell", line: Line, connect_dir: WallType, show_wall: bool = True):
            self.__window = window
            self.__line = line
            self.show = show_wall
            self.cells = {connect_dir.opposite(): cell_a, connect_dir: cell_b}
            self.shown_color = WALL_COLOR
            self.hidden_color = BACKGROUND_COLOR
            self.__is_exterior = cell_b is None
            
        
        def __repr__(self):
            return f"Wall({self.cells.keys()}, {('Visible' if self.show else 'Hidden') + (' exterior' if self.is_exterior() else ' interior')})"
        
        def draw(self, wall_color: str = None, cell_edge_color: str = None):
            if wall_color is not None:
                self.shown_color = wall_color
            if cell_edge_color is not None:
                self.hidden_color = cell_edge_color

            is_exterior = self.is_exterior()     
            self.__line.width = EXTERIOR_WALL_WIDTH if is_exterior else WALL_WIDTH
            color = (EXTERIOR_WALL_COLOR if is_exterior else self.shown_color) if self.show else self.hidden_color
            self.__window.draw_line(self.__line, color)

        def connect_to_cell(self, cell: "Cell", connect_dir: WallType):
            self.cells[connect_dir.opposite()] = cell

        def go(self, direction: WallType) -> "Cell":
            return self.cells[direction]
        
        def is_exterior(self):
            return self.__is_exterior

    __SOLITARY_CELL_STATES = {CellState.ACTIVE, CellState.UNUSED, CellState.WALKED}
    __CELL_STATE_COLORS = {CellState.ACTIVE: (CELL_ACTIVE_COLOR, CELL_ACTIVE_BORDER, WALL_COLOR),
                           CellState.END: (CELL_END_FILL, CELL_END_BORDER, WALL_COLOR),
                           CellState.START: (CELL_START_FILL, CELL_START_BORDER, WALL_COLOR),
                           CellState.UNUSED: (CELL_UNUSED_COLOR, CELL_UNUSED_BORDER, CELL_START_BORDER),
                           CellState.WALKED: (CELL_WALKED_FILL, CELL_WALKED_BORDER, CELL_WALKED_BORDER)}

    def __init__(self, window: Window, top_left_point: Point, cell_size: float, has_left_wall: bool = True, has_right_wall: bool = True, has_top_wall: bool = True, has_bottom_wall: bool = True ):
        self._win = window
        self.grid_pos = (int((top_left_point.x - (top_left_point.x % cell_size)) / cell_size), int((top_left_point.y - (top_left_point.y % cell_size)) / cell_size))

        self.state = {CellState.UNUSED}
        self.fill_color, self.cell_border_color, self.wall_color = Cell.__CELL_STATE_COLORS[CellState.UNUSED]

        self._cell_center_point = top_left_point + (cell_size / 2)
        top_right_point = Point(top_left_point.x + cell_size, top_left_point.y)
        bottom_left_point = Point(top_left_point.x, top_left_point.y + cell_size)
        bottom_right_point = Point(top_left_point.x + cell_size, top_left_point.y + cell_size)

        self.walls = { WallType.TOP: Line(top_left_point, top_right_point, self.wall_color),
                       WallType.RIGHT: Line(top_right_point, bottom_right_point, self.wall_color),
                       WallType.BOTTOM: Line(bottom_right_point, bottom_left_point, self.wall_color),
                       WallType.LEFT: Line(bottom_left_point, top_left_point, self.wall_color)}

        self.body = Rectangle(top_left_point, bottom_right_point, self.fill_color, self.cell_border_color, CELL_BORDER_WIDTH)
        self.visited = False

    def __get_highest_state(self):
        state = CellState.UNUSED
        if CellState.START in self.state:
            state = CellState.START
        elif CellState.END in self.state:
            state = CellState.END
        else:
            state = self.state.pop()
            self.state.add(state)
        return state

    def __eq__(self, value : "Cell"):
        return self.grid_pos == value.grid_pos and self.state == value.state and self.walls == value.walls
    
    def __repr__(self):
        return f"Cell({self.grid_pos}, {self.state}, {self.walls})"
    
    def choices(self, include_all: bool = False) -> list[tuple[Wall, WallType]]:
        return [(wall, dir) for dir, wall in self.walls.items() if ((not wall.is_exterior()) and ((not (wall.show or wall.go(dir).visited)) or include_all))]
    
    def clear_all_walls(self):
        for wall in self.walls.values():
            if not wall.is_exterior(): wall.show = False

    def raise_all_walls(self):
        for wall in self.walls.values():
            if not wall.is_exterior(): wall.show = True

    def draw(self):
        if self._win is not None:
            state = self.__get_highest_state()

            self._win.draw_rectangle(self.body, self.fill_color, self.cell_border_color)
            #draw_all = state in {CellState.ACTIVE, CellState.END, CellState.START}
            draw_all = True
            for wall in self.walls.values():
                if draw_all or wall.is_exterior(): wall.draw()

    def add_state(self, cell_state: CellState):
        if cell_state in Cell.__SOLITARY_CELL_STATES: 
            self.state -= Cell.__SOLITARY_CELL_STATES
        self.state.add(cell_state)

        state = self.__get_highest_state()
        self.fill_color, self.cell_border_color, self.wall_color = Cell.__CELL_STATE_COLORS[state]

    def connect_to(self, boundry_cell_dict : dict[WallType: "Cell"]):
        for direction, cell, line in [(direction, cell, self.walls[direction]) for direction, cell in boundry_cell_dict.items()]:
            if cell is None:
                self.walls[direction] = Cell.Wall(self._win, self, cell, line, direction, True)
            elif type(line) is Line:
                self.walls[direction] = Cell.Wall(self._win, self, cell, line, direction, True)
                cell.walls[direction.opposite()] = self.walls[direction]

    def draw_move(self, to_cell: WallType, undo: bool = False):
        self._win.draw_line(Line(self._cell_center_point, self.walls[to_cell].go(to_cell)._cell_center_point, width=WALK_WIDTH), WALKBACK_COLOR if undo else WALK_COLOR)

