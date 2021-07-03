from tkinter import *

from PIL import ImageTk, Image

from RunGame import *
from time import sleep
import threading


class GuiControls(Frame):
    def __init__(self, root, app, fullscreen):
        self.app = app

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.attributes('-fullscreen', fullscreen)
        root.attributes("-topmost", True)
        # root.resizable(width=False, height=False)
        root.geometry("%dx%d+0+0" % (w, h))
        root.configure(background='black')

        self.root = root
        
        Frame.__init__(self, root, width=w, height=h, background="#000000", cursor='none')
        self.canvas = Canvas(self, width=w, height=h, borderwidth=0, background="#000000")

        self.title = [
            Label(self.canvas, text="START NEW", background="#000000", foreground="#00ff00", font=("Courier", 34)),
            Label(self.canvas, text="CONTINUE", background="#000000", foreground="#00ff00", font=("Courier", 34))]
        self.selected = 0
        self.selection_max = 2
        self.set_selection()

        image = Image.open("Controls.png")
        image_ratio = (w / image.width)
        #image_ratio = 0.5
        self.photo = ImageTk.PhotoImage(image.resize((int(image.width * image_ratio), int(image.height * image_ratio)),
                                                     Image.ANTIALIAS))

        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        for i, title in enumerate(self.title):
            self.canvas.create_window(w / (len(self.title) + 1) * (i + 1), h, anchor="s", window=title)
        self.canvas.pack()
        self.pack()

        p1_movs = ["Move", "Space", "Escape", "1", "2", "3", "4", "5", "6", "7", "8"]
        p2_movs = ["Move", "Kill", "Return", "1", "2", "3", "4", "5", "6", "7", "8"]

        with open('./GameConfigs/' + self.app.game_widgets[self.app.selected_gf].game_id + '.lyt') as lyt:
            for line in lyt:
                if "Joystick 1" in line:
                    movs = p1_movs
                elif "Joystick 2" in line:
                    movs = p2_movs

                lines = line.split("#")
                if len(lines) > 1:
                    key = lines[1].strip()
                    # print(lines[0], key)

                    if "Axis" in lines[0]:
                        movs[0] = key
                    elif "Button 1:" in lines[0]:
                        movs[1] = key
                    elif "Button 2:" in lines[0]:
                        movs[3] = key
                    elif "Button 3:" in lines[0]:
                        movs[4] = key
                    elif "Button 4:" in lines[0]:
                        movs[5] = key
                    elif "Button 5:" in lines[0]:
                        movs[6] = key
                    elif "Button 8:" in lines[0]:
                        movs[7] = key
                    elif "Button 9:" in lines[0]:
                        movs[8] = key
                    elif "Button 10:" in lines[0]:
                        movs[9] = key
                    elif "Button 11:" in lines[0]:
                        movs[10] = key
                    elif "Button 12:" in lines[0]:
                        movs[2] = key

        height_joy = int(435*image_ratio)
        self.joy1 = Label(self.canvas, text=p1_movs[0], background="#000000", foreground="#00ff00",
                          font=("Courier", 34))
        self.joy1.place(relx=int(215*image_ratio)/w, rely=height_joy/h, anchor='c')
        self.joy2 = Label(self.canvas, text=p2_movs[0], background="#000000", foreground="#00ff00",
                          font=("Courier", 34))
        self.joy2.place(relx=int(795*image_ratio)/w, rely=height_joy/h, anchor='c')

        height_bot_row = int(580*image_ratio)
        self.but_left = Label(self.canvas, text=p1_movs[1], background="#000000", foreground="#00ff00",
                              font=("Courier", 34))
        self.but_left.place(relx=int(100*image_ratio)/w, rely=height_bot_row/h, anchor='w')
        self.but_right = Label(self.canvas, text=p2_movs[2], background="#000000", foreground="#00ff00",
                               font=("Courier", 34))
        self.but_right.place(relx=int(1180*image_ratio)/w, rely=height_bot_row/h, anchor='e')

        self.but_center_left = Label(self.canvas, text=p1_movs[2], background="#000000", foreground="#00ff00",
                                     font=("Courier", 34))
        self.but_center_left.place(relx=int(580*image_ratio)/w, rely=height_bot_row/h, anchor='e')
        self.but_center_right = Label(self.canvas, text=p2_movs[1], background="#000000", foreground="#00ff00",
                                      font=("Courier", 34))
        self.but_center_right.place(relx=int(700*image_ratio)/w, rely=height_bot_row/h, anchor='w')

        height_but_top = int(235 * image_ratio)
        height_but_bot = int(365 * image_ratio)
        self.p1_buts = []
        self.p2_buts = []
        for i in range(4):
            self.p1_buts.append(
                self.canvas.create_text(int((385 + i * 66) * image_ratio), height_but_top,
                                        anchor="w", font=("Courier", 15), angle=45, fill="#00ff00",
                                        text=p1_movs[i + 3]))
            self.p2_buts.append(
                self.canvas.create_text(int((960 + i * 66) * image_ratio), height_but_top,
                                        anchor="w", font=("Courier", 15), angle=45, fill="#00ff00",
                                        text=p2_movs[i + 3]))
        for i in range(4):
            self.p1_buts.append(
                self.canvas.create_text(int((385 + i * 66) * image_ratio), height_but_bot,
                                        anchor="w", font=("Courier", 15), angle=-45, fill="#00ff00",
                                        text=p1_movs[i + 7]))
            self.p2_buts.append(
                self.canvas.create_text(int((960 + i * 66) * image_ratio), height_but_bot,
                                        anchor="w", font=("Courier", 15), angle=-45, fill="#00ff00",
                                        text=p2_movs[i + 7]))

        root.bind("<KeyRelease-Return>", self.quit_del)
        root.bind("<Up>", self.up)
        root.bind("<Down>", self.down)
        root.bind("<Left>", self.up)
        root.bind("<Right>", self.down)
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
        # despite destroying, nothing gets refreshed until this method ends
        self.destroy()
        self.root.destroy()
        kill_gui_controller(self.app.qjoypad)
        
        self.app.run_game_after_controls_gui_closes()
