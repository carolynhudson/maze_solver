from tkinter import Tk, BOTH, Canvas
from line import Line
from rectangle import Rectangle
from constants import *
class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, height=height, width=width, background=BACKGROUND_COLOR, highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR, borderwidth=BORDER_WIDTH)
        self.__canvas.pack()
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_rectangle(self, rectangle: Rectangle, fill_color: str = None, border_color: str = None):
        rectangle.draw(self.__canvas, fill_color, border_color)
        
    def draw_line(self, line : Line, color: str = None):
        line.draw(self.__canvas, color)