import unittest

from maze import Maze
from point import Point

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(None,num_cols,num_rows, Point(0,0),10)

        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        
    def test_maze_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(None,num_cols,num_rows, Point(0,0),10)
        m1._cells[1][1].visited = True
        m1._cells[1][3].visited = True

        self.assertTrue(m1._cells[1][1].visited)
        self.assertTrue(m1._cells[1][3].visited)
        m1._reset_cells_visited()
        self.assertFalse(any([cell.visited for cell__col in m1._cells for cell in cell__col]))

if __name__ == "__main__":
    unittest.main()