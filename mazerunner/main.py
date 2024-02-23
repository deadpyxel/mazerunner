from mazerunner.core import Window


def main() -> int:
    win = Window(800, 600)
    win.wait_for_close()

    return 0


if __name__ == "__main__":
    exit(main())
