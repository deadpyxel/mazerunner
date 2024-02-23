import random

from mazerunner.core import Line, Point, Window
from mazerunner.maze import Cell


def main() -> int:
    win = Window(1280, 800)

    c1 = Cell(Point(10, 10), Point(110, 110), win)
    c1.draw()
    c2 = Cell(Point(110, 10), Point(210, 110), win)
    c2.draw()
    c3 = Cell(Point(10, 110), Point(110, 210), win)
    c3.draw()
    c1.draw_move(c2)
    c1.draw_move(c3, undo=True)

    win.wait_for_close()

    return 0


if __name__ == "__main__":
    exit(main())
