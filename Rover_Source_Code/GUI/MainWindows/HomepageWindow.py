import tkinter as Tk
from tkinter import font as tkFont
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
        self.select_button_font = tkFont.Font(size=18, weight='bold')

    def homepage(self):
        select_button_uv = Tk.Button(self, text="UPLC/UV Data File",
                                     command=lambda: self.browse_button("UPLCUV"),
                                     font=self.select_button_font)
        select_button_ms = Tk.Button(self, text="UPLC/MS Data File",
                                     command=lambda: self.browse_button("UPLCMS"),
                                     font=self.select_button_font)
        select_button_uv.grid(sticky=Tk.W, padx=10, pady=10)
        select_button_ms.grid(sticky=Tk.W, padx=10, pady=10)

    def start_data_processing(self, file_name, instrument_type):
        batch = cont(file_name, instrument_type)
        self.parent.display_batchpage(batch, instrument_type)

    def browse_button(self, instrument_type):
        filename = filedialog.askopenfilename(initialdir= r"T:\ANALYST WORK FILES\Peter\Rover\xml_data_files")
        self.start_data_processing(filename, instrument_type)



