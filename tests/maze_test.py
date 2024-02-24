from mazerunner.maze import Maze


def test_maze_has_correct_number_of_cells() -> None:
    num_cols = 5
    num_rows = 6
    m1 = Maze(0, 0, num_rows, num_cols, 10)

    assert len(m1._cells) == num_rows  # do we have the correct number of rows
    # do we have the proper number of columns in all rows
    assert all(len(row) == num_cols for row in m1._cells)


def test_maze_can_create_entry_and_exit(dummy_maze: Maze) -> None:
    dummy_maze._break_entrance_and_exit()

    entry = dummy_maze._cells[0][0]
    out = dummy_maze._cells[-1][-1]

    assert entry.walls[0] is False
    assert out.walls[2] is False
