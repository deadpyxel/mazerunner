import pytest

from mazerunner.maze import Maze, Wall


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

    assert entry.walls[Wall.TOP] is False
    assert out.walls[Wall.BOTTOM] is False


@pytest.mark.parametrize(
    "pos",
    [
        pytest.param((-1, -1), id="both_negative"),
        pytest.param((999, 999), id="large_positives"),
        pytest.param((-1, 0), id="negative_row"),
        pytest.param((0, -1), id="negative_column"),
    ],
)
def test_check_for_out_of_bounds_returns_true_for_invalid_positions(
    dummy_maze: Maze, pos: tuple[int, int]
) -> None:
    assert dummy_maze._cell_is_out_of_bounds(pos) is True


@pytest.mark.parametrize(
    "pos",
    [
        pytest.param((1, 1), id="inside_position"),
        pytest.param((0, 0), id="corner_position"),
    ],
)
def test_check_for_out_of_bounds_returns_false_for_valid_positions(
    dummy_maze: Maze, pos: tuple[int, int]
) -> None:
    assert dummy_maze._cell_is_out_of_bounds(pos) is False


def test_diagnal_adjacency_raises_error(dummy_maze: Maze) -> None:
    curr = (0, 0)
    tgt = (1, 1)
    with pytest.raises(ValueError):
        dummy_maze._find_relative_position_of_cell(curr, tgt)


def test_same_cell_positions_raises_error(dummy_maze: Maze) -> None:
    curr = (0, 0)
    tgt = (0, 0)
    with pytest.raises(ValueError):
        dummy_maze._find_relative_position_of_cell(curr, tgt)


@pytest.mark.parametrize(
    "cell_positions,expected",
    [
        pytest.param(((0, 0), (1, 0)), Wall.BOTTOM, id="target_is_bottom"),
        pytest.param(((1, 0), (0, 0)), Wall.TOP, id="target_is_top"),
        pytest.param(((0, 0), (0, 1)), Wall.RIGHT, id="target_is_right"),
        pytest.param(((0, 1), (0, 0)), Wall.LEFT, id="target_is_left"),
    ],
)
def test_cell_adjacency_is_correctly_identified(
    dummy_maze: Maze,
    cell_positions: tuple[tuple[int, int], tuple[int, int]],
    expected: Wall,
) -> None:
    curr, tgt = cell_positions
    assert dummy_maze._find_relative_position_of_cell(curr, tgt) == expected


def test_maze_resets_visited_cells() -> None:
    maze = Maze(0, 0, num_rows=5, num_cols=5, cell_size=10)

    for row in maze._cells:
        for cell in row:
            cell.visited = True

    maze._reset_cells_visited()

    assert all(cell.visited is False for row in maze._cells for cell in row)


@pytest.mark.parametrize(
    "dim",
    [
        pytest.param((1, 1), id="1by1"),
        pytest.param((2, 2), id="2by2"),
        pytest.param((4, 4), id="4by4"),
        pytest.param((8, 8), id="8by8"),
        pytest.param((16, 16), id="16by16"),
        pytest.param((16, 8), id="16by8"),
        pytest.param((8, 16), id="8by16"),
    ],
)
def test_maze_graph_is_always_connected(dim: tuple[int, int]) -> None:
    rows, cols = dim
    maze = Maze(0, 0, num_rows=rows, num_cols=cols, cell_size=10, seed=0)

    graph = maze._generate_maze_graph()

    assert maze._check_connectivity(graph, start_node=(0, 0)) is True


def test_maze_solve_method_returns_true_for_valid_maze() -> None:
    rows, cols = 4, 4
    maze = Maze(0, 0, num_rows=rows, num_cols=cols, cell_size=1, seed=0)

    maze.generate_maze()

    assert maze.solve() is True


def test_maze_solve_method_returns_false_for_invalid_maze() -> None:
    maze = Maze(0, 0, num_rows=2, num_cols=2, cell_size=1, seed=0)

    maze.generate_maze()
    # remove the connections for start of the maze
    maze._maze_graph[(0, 0)] = []

    assert maze.solve() is False
