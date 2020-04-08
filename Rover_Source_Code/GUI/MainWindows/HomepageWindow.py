import tkinter as Tk
from tkinter import filedialog
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)

from Pre_Generate.pre_generate_controller import PreGenerateController as cont


class HomepageWindow(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

    def homepage(self):
        select_button = Tk.Button(self, text="Select data file", command=self.browse_button)
        select_button.grid()

    def start_data_processing(self, file_name):
        batch = cont(file_name)
        self.parent.display_batchpage(batch)

    def browse_button(self):
        filename = filedialog.askopenfilename(initialdir= r"T:\ANALYST WORK FILES\Peter\Rover\xml_data_files")
        self.start_data_processing(filename)



