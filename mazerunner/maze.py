from mazerunner.core import Line, Point, Window


class Cell:
    def __init__(self, tl_corner: Point, br_corner: Point, win: Window) -> None:
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
        center_self = self._find_cell_center()
        center_tgt = to_cell._find_cell_center()
        line = Line(center_self, center_tgt)
        self._win.draw_line(line, "gray" if undo else "red")

    def _find_cell_center(self) -> Point:
        # Find X and Y coordinates of the middle of the cell
        x = (self._tl_corner.x + self._br_corner.x) // 2
        y = (self._tl_corner.y + self._br_corner.y) // 2
        return Point(x, y)
