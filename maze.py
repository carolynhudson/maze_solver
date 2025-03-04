from tkinter import Tk, Canvas
from line import Line
from point import Point
from window import Window
from cell import Cell

class Maze():
    def __init__(self, window: Window, cells_across: int, cells_down: int, grid_upper_left_point: Point, cell_size: float):
        self._window = window
        self.grid_anchor = grid_upper_left_point
        self._grid = [[Cell(window, grid_upper_left_point + Point(x * cell_size, y * cell_size), cell_size) for y in range(cells_down)] for x in range(cells_across)]
        for x, y in [(x, y) for x in range(cells_across - 1) for y in range(cells_down - 1)]:
            self._grid[x][y].connect_to(self._grid[x+1][y], self._grid[x][y + 1])
        
    def draw(self):
        for cell in [cell for cell_col in self._grid for cell in cell_col]:
            cell.draw()