from tkinter import Tk, Canvas


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
