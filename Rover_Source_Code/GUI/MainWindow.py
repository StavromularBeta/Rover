import tkinter as Tk
from MainWindows import HomepageWindow as Hpw


class MainWindow(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.HomepageWindow = Hpw.HomepageWindow(self)

    def clear_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.HomepageWindow = Hpw.HomepageWindow(self)

    def display_homepage(self):
        self.clear_main_window()
        self.HomepageWindow.homepage()
        self.HomepageWindow.grid()
