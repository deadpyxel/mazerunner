import random

from mazerunner.core import Line, Point, Window
from mazerunner.maze import Cell


def main() -> int:
    win = Window(1280, 800)
    lines = []
    for _ in range(16):
        p1 = Point(x=random.randint(0, 400), y=random.randint(0, 300))
        p2 = Point(x=random.randint(400, 800), y=random.randint(300, 600))
        lines.append(Line(start=p1, end=p2))

    for line in lines:
        win.draw_line(
            line,
            fill_colour=random.choice(
                ["red", "green", "blue", "yellow", "cyan", "magenta", "black", "white"]
            ),
        )

    c = Cell(Point(10, 10), Point(150, 150), win)
    c.draw()

    win.wait_for_close()

    return 0


if __name__ == "__main__":
    exit(main())
