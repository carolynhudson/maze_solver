from window import Window
from line import Line
from point import Point
from maze import Maze
from cell import WallType

def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(10, 10), Point(790, 10)))
    win.draw_line(Line(Point(790, 10), Point(790, 590)))
    win.draw_line(Line(Point(790, 590), Point(10, 590)))
    win.draw_line(Line(Point(10, 590), Point(10, 10)))
    grid = Maze(win, 30, 20, Point(12, 12), 25)    
    grid.draw()
    grid._grid[1][1].draw_move(WallType.RIGHT)
    win.wait_for_close()


main()