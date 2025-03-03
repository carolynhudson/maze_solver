from tkinter import Tk, Canvas
from point import Point

class Line():
    def __init__(self, start : Point, end : Point, color : str = "black", width: int = "2"):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
    
    def draw(self, canvas: Canvas, color: str = None):
        if color is None:
            color = self.color
        else:
            self.color = color

        canvas.create_line(*self.start.coord(), *self.end.coord(), fill=color, width=self.width)