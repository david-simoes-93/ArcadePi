import os
import subprocess
import time
import signal
from pynput import keyboard
from pynput.keyboard import Key, Controller
from shutil import copyfile, move


def press(keyboard_, key_val):
    print("Pressing", key_val)
    keyboard_.press(key_val)


def release(keyboard_, key_val):
    print("Releasing", key_val)
    keyboard_.release(key_val)


def press_release(keyboard_, key_val):
    print("Typing", key_val)
    keyboard_.press(key_val)
    keyboard_.release(key_val)


def detect_endgame_key(key):
    if key == keyboard.Key.delete:
        return False


def get_key_from_string(key):
    if len(key) == 1:
        return key

    if key == 'Escape':
        return Key.esc
    elif key == 'space':
        return Key.space
    elif key == 'Return':
        return Key.enter
    elif key == 'Tab':
        return Key.tab
    elif key == 'F1':
        return Key.f1
    elif key == 'F2':
        return Key.f2
    elif key == 'F3':
        return Key.f3
    elif key == 'F4':
        return Key.f4
    elif key == 'F5':
        return Key.f5
    elif key == 'F6':
        return Key.f6
    elif key == 'F7':
        return Key.f7
    elif key == 'F8':
        return Key.f8
    elif key == 'F9':
        return Key.f9
    elif key == 'F10':
        return Key.f10
    elif key == 'F11':
        return Key.f11
    elif key == 'F12':
        return Key.f12
    elif key == 'Control_L':
        return Key.ctrl
    elif key == 'Left':
        return Key.left
    elif key == 'Right':
        return Key.right
    elif key == 'Up':
        return Key.up
    elif key == 'Down':
        return Key.down
    else:
        print("Unknown key: " + key + " (" + str(len(key)) + ")")
        return None


class Game:
    def __init__(self, name, keymaps):
        print("Loading game configs")
        self.id = str(name)
        self.keyboard_ = Controller()
        self.keymaps = keymaps

        self.cwd = os.getcwd()
        game_config_lines = []
        with open(self.cwd + '/GameConfigs/' + self.id + '.conf') as game_config:
            for line in game_config:
                game_config_lines.append(line.replace("\n", ""))

        self.game_name = game_config_lines[0]  # game title
        self.config_file = game_config_lines[1]  # dosbox config file
        self.game_path = game_config_lines[2]  # .EXE path

        print(self.config_file)
        print(self.game_path)

        self.game_config_lines = game_config_lines[3:]

        # when game is launched, read lyt and replace %key by value based on dictionary
        with open('./GameConfigs/' + self.id + '.lyt_', "w") as processed_lyt:
            with open('./GameConfigs/' + self.id + '.lyt') as lyt:
                for line in lyt:
                    while "%" in line:
                        try:
                            first_index = line.index("%")
                            next_space = line[first_index:].find(" ")
                            next_space = next_space if next_space != -1 else len(line)
                            next_comma = line[first_index:].find(",")
                            next_comma = next_comma if next_comma != -1 else len(line)
                            second_index = first_index + min(next_comma, next_space)
                            key_val = self.keymaps[line[first_index + 1:second_index].strip()]
                            line = line[0:first_index] + key_val + \
                                   (line[second_index:] if line[second_index:] != '' else '\n')
                        except:
                            print("Key not recognized:", "-" + line[first_index + 1:second_index] + "-")
                    # print(line)
                    processed_lyt.write(line)

    def start_game(self):
        print("Launching game", self.id)

        # Start QJoypad
        move(self.cwd + '/GameConfigs/' + self.id + '.lyt_', '/home/david/.qjoypad3/' + self.id + '.lyt')
        cmd = ['qjoypad '+self.id]
        p_joypad = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

        # Start game
        print(self.cwd + '/Games/' + self.id + '/' + self.game_path)
        cmd = ['dosbox', self.cwd + '/Games/' + self.id + '/' + self.game_path, '-conf',
               self.cwd + '/DosboxConfigs/' + self.config_file]
        print("Running ", cmd)
        game = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        # Run initial key setup
        for line in self.game_config_lines:
            command, var = line.replace("\n", "").split(" ")
            if command == 'sleep':
                time.sleep(float(var))
            elif command == 'key':
                press_release(self.keyboard_, get_key_from_string(var))
            elif command == 'hold':
                press(self.keyboard_, get_key_from_string(var))
            elif command == 'release':
                release(self.keyboard_, get_key_from_string(var))

        print("Done")

        # Wait for DEL key to be pressed
        with keyboard.Listener(
                on_release=detect_endgame_key) as listener:
            listener.join()

        # Kill processes
        game.terminate()
        os.killpg(os.getpgid(p_joypad.pid), signal.SIGTERM)

    def load_game(self):
        # http://xmodulo.com/how-to-checkpoint-and-restore-linux-process.html
        # https://criu.org/Installation
        pass
