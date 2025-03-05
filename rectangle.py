from tkinter import Tk, Canvas
from point import Point

class Rectangle():
    def __init__(self, corner_a : Point, corner_b : Point, fill_color : str = "white", border_color : str = "black", border_width: int = "1"):
        self._corner_a = corner_a
        self._corner_b = corner_b
        self.border_color = border_color
        self.fill_color = fill_color
        self.border_width = border_width

    def draw(self, canvas: Canvas, fill_color: str = None, border_color: str = None):
        if fill_color is None:
            fill_color = self.fill_color
        if border_color is None:
            border_color = self.border_color

        canvas.create_rectangle(*self._corner_a.coord(), *self._corner_b.coord(), 
                                activefill=fill_color, activeoutline=border_color, activewidth=self.border_width, 
                                fill=fill_color, outline=border_color, width=self.border_width)