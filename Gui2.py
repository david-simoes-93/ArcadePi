from tkinter import *


class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.root = parent
        self.pack()

    def key(self, event):
        pass

    def quit_del(self, event):
        self.root.destroy()
