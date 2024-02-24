from mazerunner.maze import Maze


def test_maze_has_correct_number_of_cells() -> None:
    num_cols = 12
    num_rows = 10
    m1 = Maze(0, 0, num_rows, num_cols, 10)

    assert len(m1._cells) == num_rows  # do we have the correct number of rows
    # do we have the proper number of columns in all rows
    assert all(len(row) == num_cols for row in m1._cells)
