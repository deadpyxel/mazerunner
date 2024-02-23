from tkinter import Tk, Canvas


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x  # x = 0, starting from the left of the screen
        self.y = y  # y = 0, starting from the top of the screen


class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def draw(self, c: Canvas, fill_colour: str) -> None:
        c.create_line(
            self.start.x,
            self.start.y,
            self.end.x,
            self.end.y,
            fill=fill_colour,
            width=2,
        )
        c.pack()


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Test")
        self.__canvas = Canvas()
        self.__canvas.pack()
        self.is_running = False

        # connects `close` class method to delete window action, stopping th eprogram once we close the window
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self) -> None:
        self.is_running = False

    def draw_line(self, line: Line, fill_colour: str) -> None:
        line.draw(self.__canvas, fill_colour)
