from enum import Enum
import time
from typing import Optional

from mazerunner.core import Line, Point, Window


class Wall(Enum):
    TOP = 0
    RIGHT = 1
    LEFT = 2
    BOTTOM = 3


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
        self._create_cells()
        self._break_entrance_and_exit()

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
        entry_cell.walls[0] = False
        exit_cell = self._cells[-1][-1]
        exit_cell.walls[2] = False

        if self.__win:
            entry_cell.draw()
            exit_cell.draw()

    def __str__(self) -> str:
        s = f"Maze with {self.__num_rows} rows and {self.__num_cols} columns, cell size {self.__cell_size}"
        return f"{s}. {'DRAWING' if self.__win else 'HEADLESS'} mode enabled"
