from window import Window
from point import Point
from maze import Maze
from cell import WallType
from constants import *

def main():
    win = Window(*WINDOW_SIZE)
    columns = 80
    rows = 60
    size = min([(WINDOW_SIZE[0] - 10) / columns, (WINDOW_SIZE[1] - 10) / rows])
    grid = Maze(win, columns, rows, Point(5, 5), size)    
    grid.draw_all()
    grid.solve()
    #grid._cells[1][1].draw_move(WallType.RIGHT)
    win.wait_for_close()


main()