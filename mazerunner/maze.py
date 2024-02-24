import time
from typing import Optional

from mazerunner.core import Line, Point, Window


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
        self.has_l_wall = True
        self.has_r_wall = True
        self.has_t_wall = True
        self.has_b_wall = True
        # spatial dimensions
        self._tl_corner = tl_corner  # Top-Left corner
        self._br_corner = br_corner  # Bottom Right corner
        self._win = win  # Window reference

    def draw(self) -> None:
        if not self._win:
            return
        line = None
        x1, y1 = self._tl_corner.x, self._tl_corner.y
        x2, y2 = self._br_corner.x, self._br_corner.y
        # TODO: Refactor this into a loop with a list booleans as wall representation instead
        if self.has_l_wall:
            line = Line(start=self._tl_corner, end=Point(x1, y2))
            self._win.draw_line(line=line, fill_colour="black")
        if self.has_r_wall:
            line = Line(start=Point(x2, y1), end=self._br_corner)
            self._win.draw_line(line=line, fill_colour="black")
        if self.has_t_wall:
            line = Line(start=self._tl_corner, end=Point(x2, y1))
            self._win.draw_line(line=line, fill_colour="black")
        if self.has_b_wall:
            line = Line(start=Point(x1, y2), end=self._br_corner)
            self._win.draw_line(line=line, fill_colour="black")

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


    def __str__(self) -> str:
        s = f"Maze with {self.__num_rows} rows and {self.__num_cols} columns, cell size {self.__cell_size}"
        return f"{s}. {'DRAWING' if self.__win else 'HEADLESS'} mode enabled"
