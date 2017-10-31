from tkinter import *
from PIL import Image, ImageTk
import math
from RunGame import Game


class GameFrame(Frame):
    def __init__(self, parent, game_name, w):
        h = w*1.4
        Frame.__init__(self, parent, width=w, height=h, background="#ffffff")
        self.pack_propagate(0)

        self.game_id = game_name
        with open("./GameConfigs/" + game_name + ".conf", 'r') as f:
            self.title = Label(self, text=f.readline(), background="#ffffff", foreground="#000000")

        image = Image.open("./GameConfigs/" + game_name + ".jpg")
        ratio_x, ratio_y = (w-10) / image.width, (h-45) / image.height
        ratio = ratio_x if ratio_x < ratio_y else ratio_y
        self.photo = ImageTk.PhotoImage(
            image.resize((math.floor(image.width * ratio), math.floor(image.height * ratio)), Image.ANTIALIAS))
        self.photo_container = Label(self, image=self.photo)

        self.title.pack(side="top")
        self.photo_container.pack()


class Application(Frame):
    def __init__(self, parent, games_list, key_values):
        Frame.__init__(self, parent)
        self.root = parent
        self.key_values = key_values
        self.pack()

        self.canvas = Canvas(self, width=1280, height=720, borderwidth=0, background="#ffffff")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left")

        self.frame = Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.game_widgets = []
        self.cols = 5
        self.create_widgets(self.frame, games_list, parent.winfo_screenwidth()/self.cols)
        self.selected_gf = 0
        self.set_selected()

    def create_widgets(self, root, games_list, w):
        for i, game in enumerate(games_list):
            gf = GameFrame(root, game, w)
            gf.grid(column=i % self.cols, row=math.floor(i / self.cols))
            self.game_widgets.append(gf)

    def on_frame_configure(self, _):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def key(self, event):
        Game(self.game_widgets[self.selected_gf].game_id, self.key_values).start_game()

    def right(self, event):
        self.clear_selected()
        col = self.selected_gf % self.cols
        self.selected_gf = (self.selected_gf - col) + (col + 1) % self.cols
        self.set_selected()

    def left(self, event):
        self.clear_selected()
        col = self.selected_gf % self.cols
        self.selected_gf = (self.selected_gf - col) + (col - 1 if col - 1 >= 0 else self.cols - 1)
        self.set_selected()

    # wont work correctly if there isn't a 'square' number of games
    def down(self, event):
        self.clear_selected()
        self.selected_gf = (self.selected_gf + self.cols) % len(self.game_widgets)
        self.set_selected()

    # wont work correctly if there isn't a 'square' number of games
    def up(self, event):
        self.clear_selected()
        col = self.selected_gf % self.cols
        self.selected_gf = (self.selected_gf - self.cols) if (self.selected_gf - self.cols) >= 0 else \
            len(self.game_widgets) - self.cols + col
        self.set_selected()

    def quit_del(self, event):
        self.root.destroy()

    def clear_selected(self):
        self.game_widgets[self.selected_gf].configure(background="#ffffff")
        self.game_widgets[self.selected_gf].title.configure(background="#ffffff", foreground="#000000")

    def set_selected(self):
        self.game_widgets[self.selected_gf].configure(background="#000000")
        self.game_widgets[self.selected_gf].title.configure(background="#000000", foreground="#ffffff")
        self.canvas.yview_moveto((self.selected_gf-self.selected_gf % self.cols)/len(self.game_widgets))
