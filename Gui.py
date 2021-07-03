from tkinter import *
from PIL import Image, ImageTk
import math

from GuiControls import GuiControls
from RunGame import Game, set_gui_controller, kill_gui_controller
from time import sleep


class GameFrame(Frame):
    def __init__(self, root, game_name, w):
        h = w * 1.4
        Frame.__init__(self, root, width=w, height=h, background="#000000", cursor='none')
        self.pack_propagate(0)

        if game_name != "":
            self.game_id = game_name
            with open("./GameConfigs/" + game_name + ".conf", 'r') as f:
                title = f.readline()
                fields = title.split(":")
                if len(fields) == 2:
                    title = fields[0] + ":\n" + fields[1]
                else:
                    title = "\n" + title
                self.title = Label(self, text=title, background="#000000", foreground="#00ff00")

            image = Image.open("./GameConfigs/" + game_name + ".jpg")
            ratio_x, ratio_y = (w - 10) / image.width, (h - 55) / image.height
            ratio = ratio_x if ratio_x < ratio_y else ratio_y
            self.photo = ImageTk.PhotoImage(
                image.resize((math.floor(image.width * ratio), math.floor(image.height * ratio)), Image.ANTIALIAS))
            self.photo_container = Label(self, image=self.photo)

            self.title.pack(side="top")
            self.photo_container.pack()
        else:
            self.title = Label(self, text="")
            self.game_id = None


class Application(Frame):
    def __init__(self, root, games_list, key_values, fullscreen):
        self.fs = fullscreen
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.attributes('-fullscreen', fullscreen)
        root.attributes("-topmost", True)
        #root.resizable(width=False, height=False)
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='black')
        
        Frame.__init__(self, root, background="#000000", cursor='none')
        self.root = root
        self.key_values = key_values
        self.pack()

        self.canvas = Canvas(self, width=root.winfo_screenwidth(), height=root.winfo_screenheight(),
                             borderwidth=0, background="#000000")
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview,
                             background="#00ff00", troughcolor="#000000")
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left")

        self.frame = Frame(self.canvas, background="#000000")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.game_widgets = []
        self.cols = 5
        self.create_widgets(self.frame, games_list, (root.winfo_screenwidth() - 10) / self.cols)
        self.selected_gf = 0
        self.set_selected()

        self.qjoypad = set_gui_controller(self.key_values)

        root.bind("<KeyRelease-Return>", self.key)
        root.bind("<Up>", self.up)
        root.bind("<Down>", self.down)
        root.bind("<Left>", self.left)
        root.bind("<Right>", self.right)
        root.bind("<KeyRelease-Delete>", self.quit_del)
        root.focus_set()

    def create_widgets(self, root, games_list, w):
        while len(games_list) % self.cols != 0:
            games_list.append("")

        for i, game in enumerate(games_list):
            gf = GameFrame(root, game, w)
            gf.grid(column=i % self.cols, row=math.floor(i / self.cols))
            self.game_widgets.append(gf)

    def on_frame_configure(self, _):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def key(self, event):
        if self.game_widgets[self.selected_gf].game_id is None:
            return

        self.root.withdraw()

        gui_controls = Toplevel(self.root)
        self.gui_controls = GuiControls(gui_controls, self, self.fs)
        
    def run_game_after_controls_gui_closes(self):
        Game(self.game_widgets[self.selected_gf].game_id, self.key_values).start_game()

        self.qjoypad = set_gui_controller(self.key_values)
        
        # KILL EVERYTHING after game is run
        self.quit()
        
        # the shell script will launch new stuff, everything is cleared
        #self.root.deiconify()
        #self.root.focus_set()

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
        kill_gui_controller(self.qjoypad)
        self.root.destroy()

    def clear_selected(self):
        self.game_widgets[self.selected_gf].configure(background="#000000")
        self.game_widgets[self.selected_gf].title.configure(background="#000000", foreground="#00ff00")

    def set_selected(self):
        self.game_widgets[self.selected_gf].configure(background="#00ff00")
        self.game_widgets[self.selected_gf].title.configure(background="#00ff00", foreground="#000000")
        self.canvas.yview_moveto(
            (self.selected_gf - self.selected_gf % self.cols - self.cols / 2) / len(self.game_widgets))
