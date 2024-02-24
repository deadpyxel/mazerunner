from mazerunner.core import Window
from mazerunner.maze import Maze


def main() -> int:
    win = Window(1280, 800)

    maze = Maze(x1=10, y1=10, num_rows=10, num_cols=15, cell_size=20, win=win)
    print(f"Maze created: {maze}")

    win.wait_for_close()

    return 0


if __name__ == "__main__":
    exit(main())
