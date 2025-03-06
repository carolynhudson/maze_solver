from point import Point
from window import Window
from cell import Cell, WallType, CellState
import time 
import random
class Maze():
    def _create_cells(self):
        self._cells = tuple([tuple([Cell(self._window, self._grid_anchor + Point(x * self._cell_size, y * self._cell_size), self._cell_size) for y in range(self._rows)]) for x in range(self._columns)])
        for x, y in [(x, y) for x in range(self._columns) for y in range(self._rows)]:
            walls = {w: (self._cells[x + xs][y + ys] if 0 <= (x + xs) < self._columns and 0 <= (y + ys) < self._rows else None) 
                     for w, xs, ys in [(WallType.TOP, 0, -1), (WallType.RIGHT, 1, 0), (WallType.BOTTOM, 0, 1), (WallType.LEFT, -1, 0)]}
            self._cells[x][y].connect_to(walls)

    def _reset_cells_visited(self):
        for cell in [cell for cell_col in self._cells for cell in cell_col]:
            cell.visited = False

    def _break_entrance_and_exit(self):
        self._start_cell.walls[WallType.TOP].show = False
        self._start_cell.draw()
        self._end_cell.walls[WallType.BOTTOM].show = False
        self._end_cell.draw()

    def draw_all(self):
        for cell in [cell for cell_col in self._cells for cell in cell_col]:
            cell.draw()

    def _draw_cell(self, x: int, y: int):
        self._cells[x][y].draw()

    def _animate(self):
        now = time.perf_counter()
        if (now - self._last_animate) > 0.02:
            self._window.redraw()
            self.__last_animate = time.perf_counter
    
    def _wilson_maze_gen(self):
        cell_choices = []
        for cell in [cell for cell_col in self._cells for cell in cell_col]:
            cell.add_state(CellState.UNUSED)
            cell.raise_all_walls()
            cell.draw()
            cell_choices.append(cell)

        target = cell_choices.pop(random.randint(0, len(cell_choices) - 1))
        target.add_state(CellState.ACTIVE)
        target.draw()
        self._animate()

        while len(cell_choices) > 0:
            start = random.choice(cell_choices)
            start.add_state(CellState.WALKED)
            start.draw()
            walk_path = [start]
            self._animate()
            choices = start.choices(True)
            choice = random.choice(choices + [c for c in choices if CellState.ACTIVE not in c[0].go(c[1]).state])
            walk_steps = [choice[0]]
            current = choice[0].go(choice[1])

            while CellState.UNUSED in current.state:
                current.add_state(CellState.WALKED)
                current.draw()
                walk_path.append(current)
                self._animate()
                choice = random.choice([c for c in current.choices(True) if c[0] != walk_steps[-1]])
                walk_steps.append(choice[0])
                current = choice[0].go(choice[1])

                if CellState.ACTIVE in current.state:
                    for cell, wall in [(walk_path[i], walk_steps[i]) for i in range(len(walk_path))]:
                        wall.show = False
                        cell.add_state(CellState.ACTIVE)
                        cell.draw()
                    cell_choices = [cell for cell_col in self._cells for cell in cell_col if not CellState.ACTIVE in cell.state]
                    self._animate()
                elif CellState.WALKED in current.state:
                    current.add_state(CellState.UNUSED)
                    current.draw()
                    while walk_path[-1] != current and len(walk_path) > 0:
                        loop = walk_path.pop(-1)
                        loop.add_state(CellState.UNUSED)
                        loop.draw()
                        walk_steps.pop(-1)

                    if len(walk_path) > 1:
                        walk_path.pop(-1)
                        walk_steps.pop(-1)
                    else:
                        choices = start.choices(True)
                        choice = random.choice(choices + [c for c in choices if CellState.ACTIVE not in c[0].go(c[1]).state])
                        walk_steps = [choice[0]]
                        current = choice[0].go(choice[1])

                    self._animate()

            if CellState.ACTIVE in current.state and len(walk_path) > 0:
                for cell, wall in [(walk_path[i], walk_steps[i]) for i in range(len(walk_path))]:
                    wall.show = False
                    cell.add_state(CellState.ACTIVE)
                    cell.draw()
                cell_choices = [cell for cell_col in self._cells for cell in cell_col if not CellState.ACTIVE in cell.state]
                self._animate()
    
    def solve(self):
        self.solve_worker(self._start_cell)

    def solve_worker(self, cell : Cell):
        cell.visited = True
        if cell == self._end_cell:
            return True
        for wall, dir in cell.choices():
            cell.draw_move(dir)
            self._animate()
            if self.solve_worker(wall.go(dir)):
                return True
            else:
                cell.draw_move(dir, True)
                self._animate()
        return False


    def __init__(self, window: Window, columns: int, rows: int, grid_upper_left_point: Point, cell_size: float, random_seed : int = None):
        if random_seed is not None:
            random.seed(random_seed)

        self._window = window
        self._grid_anchor = grid_upper_left_point
        self._columns = columns
        self._rows = rows
        self._cell_size = cell_size
        self._cells = tuple()
        self._create_cells()
        self._start_cell = self._cells[0][0]
        self._start_cell.add_state(CellState.START)
        self._end_cell = self._cells[columns - 1][rows - 1]
        self._end_cell.add_state(CellState.END)
        self._break_entrance_and_exit()
        self._last_animate = time.perf_counter()
        self._wilson_maze_gen()

