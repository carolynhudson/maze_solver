from tkinter import Tk, Canvas
from line import Line
from window import Window

class Wall():
    def __init__(self, window: Window, cell, line: Line, show_wall: bool = True):
        self.__window = window
        self.__line = line
        self.show = show_wall
        self.cells = [cell, None]
    
    def draw(self):
        if self.show: self.__window.draw_line(self.__line)

    def connect_to_cell(self, cell):
        self.cells[1] = cell

    def go(self, called_from_cell):
        return self.cells[1] if called_from_cell == self.cells[0] else self.cells[0] if called_from_cell == self.cells[1] else None