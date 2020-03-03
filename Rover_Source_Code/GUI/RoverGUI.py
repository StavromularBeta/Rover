import tkinter as Tk
import BannerWindow as Bb
import MainWindow as Mw


class MainApplication(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.BannerBar = Bb.BannerWindow(self, width=1400)
        self.MainWindow = Mw.MainWindow(self)
        self.BannerBar.pack(side='top', fill='x', expand=True)
        self.BannerBar.pack_propagate(0)
        self.MainWindow.pack(side='bottom', fill='both', expand=True)
        self.MainWindow.pack_propagate(0)
        self.BannerBar.make_banner()
        self.MainWindow.display_homepage()


root = Tk.Tk()
root.geometry('1400x800')
MainApplication(root, height=800, width=1400).grid()
root.mainloop()
