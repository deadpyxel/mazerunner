import time
import random
from enum import IntEnum
from typing import Optional

from mazerunner.core import Line, Point, Window


class Wall(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class Cell:
    def __init__(
        self, tl_corner: Point, br_corner: Point, win: Optional[Window] = None
    ) -> None:
        """Cell constructor

        Parameters
        ----------
        tl_corner : Point
            top-left corner position of the cell
        br_corner : Point
            bottom-right corner position of the cell
        win : Window
            window object reference used for drawing
        """
        # a Cell has walls in all four sides by default
        # each wall presence is represented by a position in the `wall`  list
        # Top = 0, Right = 1, Bottom = 2, Left = 3
        self.walls = [True, True, True, True]
        # spatial dimensions
        self._tl_corner = tl_corner  # Top-Left corner
        self._br_corner = br_corner  # Bottom Right corner
        self._win = win  # Window reference
        self.visited = False

    def draw(self) -> None:
        if not self._win:
            return
        x1, y1 = self._tl_corner.x, self._tl_corner.y
        x2, y2 = self._br_corner.x, self._br_corner.y
        point_pos = {
            0: (self._tl_corner, Point(x2, y1)),
            1: (Point(x2, y1), self._br_corner),
            2: (self._br_corner, Point(x1, y2)),
            3: (Point(x1, y2), self._tl_corner),
        }
        for i, wall in enumerate(self.walls):
            st, end = point_pos[i]
            line = Line(start=st, end=end)
            self._win.draw_line(line=line, fill_colour="black" if wall else "#d9d9d9")

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        if self._win:
            center_self = self._find_cell_center()
            center_tgt = to_cell._find_cell_center()
            line = Line(center_self, center_tgt)
            self._win.draw_line(line, "gray" if undo else "red")

    def _find_cell_center(self) -> Point:
        # Find X and Y coordinates of the middle of the cell
        x = (self._tl_corner.x + self._br_corner.x) // 2
        y = (self._tl_corner.y + self._br_corner.y) // 2
        return Point(x, y)


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size: int,
        win: Optional[Window] = None,
        seed: Optional[int] = None,
    ) -> None:
        self.__x0 = x1
        self.__y0 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size = cell_size
        self.__win = win
        self._cells: list[list[Cell]] = [
            [Cell(Point(0, 0), Point(0, 0)) for _ in range(self.__num_cols)]
            for _ in range(self.__num_rows)
        ]
        random.seed(seed)

    def generate_maze(self) -> None:
        # instantiates the maze cells
        self._create_cells()
        # breaks wall at start and end of the maze
        self._break_entrance_and_exit()
        # generates the maze graph representation
        self.__maze_graph = self._generate_maze_graph()
        # updates cell walls with graph information and draw the maze
        self.__create_maze()
        # Resets the visited status for the maze
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                x = (j * self.__cell_size) + self.__x0
                y = (i * self.__cell_size) + self.__y0
                self._cells[i][j] = Cell(
                    tl_corner=Point(x, y),
                    br_corner=Point(x + self.__cell_size, y + self.__cell_size),
                    win=self.__win,
                )
                if self.__win:
                    self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        self._cells[i][j].draw()
        self._animate()

    def _animate(self) -> None:
        if self.__win:
            self.__win.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        entry_cell = self._cells[0][0]
        entry_cell.walls[Wall.TOP] = False
        exit_cell = self._cells[-1][-1]
        exit_cell.walls[Wall.BOTTOM] = False

        if self.__win:
            entry_cell.draw()
            exit_cell.draw()

    def _break_walls_between_cells(
        self, from_cell: tuple[int, int], to_cell: tuple[int, int]
    ) -> None:
        curr_i, curr_j = from_cell
        tgt_i, tgt_j = to_cell
        curr_cell = self._cells[curr_i][curr_j]
        tgt_cell = self._cells[tgt_i][tgt_j]

        wall_to_break_curr = self._find_relative_position_of_cell(
            curr=from_cell, tgt=to_cell
        )
        wall_to_break_tgt = self._find_relative_position_of_cell(
            curr=to_cell, tgt=from_cell
        )

        curr_cell.walls[wall_to_break_curr] = False
        tgt_cell.walls[wall_to_break_tgt] = False
        if self.__win:
            curr_cell.draw()
            tgt_cell.draw()

    def __create_maze(self) -> None:
        for node, neighbours in self.__maze_graph.items():
            for neighbour in neighbours:
                self._break_walls_between_cells(node, neighbour)

    def _reset_cells_visited(self) -> None:
        """
        Resets the 'visited' attribute of all cells in the grid to False.

        This method iterates through all cells in the grid and sets the 'visited' attribute of each cell to False.
        """

        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                self._cells[i][j].visited = False

    def _cell_is_out_of_bounds(self, pos: tuple[int, int]) -> bool:
        i, j = pos
        return (i < 0 or i >= self.__num_rows) or (j < 0 or j >= self.__num_cols)

    def _find_relative_position_of_cell(
        self, curr: tuple[int, int], tgt: tuple[int, int]
    ) -> Wall:
        if curr == tgt:
            raise ValueError("current and target positions cannot be equal")
        curr_i, curr_j = curr
        tgt_i, tgt_j = tgt
        if curr_i != tgt_i and curr_j != tgt_j:
            raise ValueError("diagonal adjacencies are not allowed")
        if curr_i != tgt_i:
            return Wall.TOP if curr_i > tgt_i else Wall.BOTTOM
        elif curr_j != tgt_j:
            return Wall.LEFT if curr_j > tgt_j else Wall.RIGHT
        else:
            raise ValueError(
                "unexpected condition: unable to determine relative position"
            )

    def _generate_maze_graph(self) -> dict[tuple[int, int], list[tuple[int, int]]]:
        graph = {
            (i, j): [] for i in range(self.__num_rows) for j in range(self.__num_cols)
        }
        visited = set()

        def dfs(node: tuple[int, int]) -> None:
            visited.add(node)
            i, j = node
            pos_neighbours = [(i, j - 1), (i + 1, j), (i, j + 1), (i - 1, j)]
            pos_neighbours = [
                pos for pos in pos_neighbours if not self._cell_is_out_of_bounds(pos)
            ]
            random.shuffle(pos_neighbours)
            for pos in pos_neighbours:
                if pos not in visited:
                    graph[node].append(pos)
                    graph[pos].append(node)
                    dfs(pos)

        dfs(node=(0, 0))

        if self._check_connectivity(graph, start_node=(0, 0)) is False:
            graph = self._generate_maze_graph()

        return graph

    def _check_connectivity(
        self,
        graph: dict[tuple[int, int], list[tuple[int, int]]],
        start_node: tuple[int, int],
    ) -> bool:
        visited = set()

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for neighbour in graph[node]:
                dfs(neighbour)

        dfs(start_node)
        return len(visited) == len(graph)

    def __str__(self) -> str:
        s = f"Maze with {self.__num_rows} rows and {self.__num_cols} columns, cell size {self.__cell_size}"
        return f"{s}. {'DRAWING' if self.__win else 'HEADLESS'} mode enabled"
