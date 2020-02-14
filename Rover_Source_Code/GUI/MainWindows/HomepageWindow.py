import tkinter as Tk
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
        self.batch_filename = Tk.Entry(self)

    def homepage(self):
        batch_entry_label = Tk.Label(self, text="Enter batch file name: ")
        batch_filename_button = Tk.Button(self, text="Process Data",
                                          command=lambda item=self.batch_filename.get():
                                          self.start_data_processing(self.batch_filename.get()))
        batch_entry_label.grid()
        self.batch_filename.grid()
        batch_filename_button.grid()

    def start_data_processing(self, file_name):
        batch = cont(file_name)
        self.parent.display_batchpage(batch)



