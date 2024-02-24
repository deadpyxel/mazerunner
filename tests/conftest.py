import pytest

from mazerunner.maze import Maze


@pytest.fixture()
def dummy_maze() -> Maze:
    num_cols = 12
    num_rows = 10
    return Maze(0, 0, num_rows, num_cols, 10)
