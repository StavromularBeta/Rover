import tkinter as Tk


class BatchWindow(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent

    def batch(self, data):
        recovery_label = Tk.Label(self, text="Blank Data")
        recovery_label.grid(row=0, column=0)
        recovery_text = Tk.Text(self, width=18, height=20)
        recovery_text.insert(Tk.END, data.dm.min_value_blank_data_frame.to_string())
        recovery_text.grid(row=1, column=0)
        recovery_label = Tk.Label(self, text="Standard Recovery Data")
        recovery_label.grid(row=0, column=1)
        recovery_text = Tk.Text(self, width=120, height=20)
        recovery_text.insert(Tk.END, data.dm.best_recovery_qc_data_frame.to_string())
        recovery_text.grid(row=1, column=1)


