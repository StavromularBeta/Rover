import tkinter as Tk
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
from MainWindows import HomepageWindow as Hpw
from MainWindows import BatchWindow as Btw


class MainWindow(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.HomepageWindow = Hpw.HomepageWindow(self)
        self.BatchWindow = Btw.BatchWindow(self)

    def clear_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.HomepageWindow = Hpw.HomepageWindow(self)
        self.BatchWindow = Btw.BatchWindow(self)

    def display_homepage(self):
        self.clear_main_window()
        self.HomepageWindow.homepage()
        self.HomepageWindow.grid()

    def display_batchpage(self, data):
        self.clear_main_window()
        self.BatchWindow.batch(data)
        self.BatchWindow.grid()
