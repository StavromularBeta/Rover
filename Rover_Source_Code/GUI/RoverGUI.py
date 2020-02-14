import tkinter as Tk
import BannerWindow as Bb
import MainWindow as Mw


class MainApplication(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.BannerBar = Bb.BannerWindow(self)
        self.MainWindow = Mw.MainWindow(self)
        self.BannerBar.pack(side='top', fill='x', expand=False)
        self.BannerBar.pack_propagate(0)
        self.MainWindow.pack(side='bottom', fill='x', expand=True)
        self.MainWindow.pack_propagate(0)
        self.BannerBar.make_banner()
        self.MainWindow.display_homepage()


root = Tk.Tk()
root.geometry('1200x900')
MainApplication(root).grid()
root.mainloop()
