from window import Window
from line import Line
from point import Point

def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(10, 10), Point(790, 10)))
    win.draw_line(Line(Point(790, 10), Point(790, 590)))
    win.draw_line(Line(Point(790, 590), Point(10, 590)))
    win.draw_line(Line(Point(10, 590), Point(10, 10)))
    win.wait_for_close()


main()