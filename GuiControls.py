from tkinter import *

from PIL import ImageTk, Image

from RunGame import *
from time import sleep


class GuiControls(Frame):
    def __init__(self, root, app):
        self.app = app

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.attributes('-fullscreen', True)
        root.attributes("-topmost", True)
        #root.resizable(width=False, height=False)
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='black')

        self.root = root
        Frame.__init__(self, root, width=w, height=h, background="#000000")
        # self.pack_propagate(0)

        self.title = [Label(self, text="START NEW", background="#000000", foreground="#00ff00", font=("Courier", 34)),
                      Label(self, text="CONTINUE", background="#000000", foreground="#00ff00", font=("Courier", 34))]
        self.selected = 0
        self.selection_max = 2
        self.set_selection()

        image = Image.open("Controls.png")
        self.photo = ImageTk.PhotoImage(image)
        self.photo_container = Label(self, image=self.photo)
        # enlarge photo to be screen size

        self.photo_container.pack()
        for title in self.title:
            title.pack()
        self.pack()

        self.joy1 = Label(self, text="WASD", background="#000000", foreground="#00ff00", font=("Courier", 34))
        self.joy1.place(relx=215/w, rely=(465)/h, anchor='c')
        self.joy2 = Label(self, text="WASD", background="#000000", foreground="#00ff00", font=("Courier", 34))
        self.joy2.place(relx=795 / w, rely=(465) / h, anchor='c')

        root.bind("<KeyRelease-Return>", self.quit_del)
        root.bind("<Up>", self.up)
        root.bind("<Down>", self.down)
        root.focus_set()

    def set_selection(self):
        for i, title in enumerate(self.title):
            if i != self.selected:
                title.configure(background="#000000", foreground="#00ff00")
            else:
                title.configure(background="#00ff00", foreground="#000000")

    def up(self, event):
        self.selected = (self.selected + 1) % self.selection_max
        self.set_selection()

    def down(self, event):
        self.selected = (self.selected - 1) if (self.selected - 1) >= 0 else self.selection_max - 1
        self.set_selection()

    def quit_del(self, event):
        self.root.destroy()
        kill_gui_controller(self.app.qjoypad)

        Game(self.app.game_widgets[self.app.selected_gf].game_id, self.app.key_values).start_game()

        #sleep(2)
        #self.app.root.geometry("%dx%d+0+0" % (self.app.root.winfo_screenwidth(), self.app.root.winfo_screenheight()))
        self.app.qjoypad = set_gui_controller(self.app.key_values)

        self.app.root.focus_set()
