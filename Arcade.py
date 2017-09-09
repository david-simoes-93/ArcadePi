import os
import pygame
import subprocess
import time
import pynput
from pynput import keyboard
from pynput.keyboard import Key, Controller
from shutil import copyfile

keyboard_ = Controller()
keybinds = []

def pressRelease(key_val):
    print("Pressing",key_val)
    keyboard_.press(key_val)
    keyboard_.release(key_val)

"""def on_press(key):
    try:
        print('alphanumeric key {0} {1} pressed'.format(key, key.char))
        if key.char == '1':
            keyboard_.press(keybinds[0])
        elif key.char == '2':
            keyboard_.press(keybinds[1])
        elif key.char == '3':
            keyboard_.press(keybinds[2])
        elif key.char == '4':
            keyboard_.press(keybinds[3])
        elif key.char == '5':
            keyboard_.press(keybinds[4])
        elif key.char == '6':
            keyboard_.press(keybinds[5])
        elif key.char == '7':
            keyboard_.press(keybinds[6])
        elif key.char == '8':
            keyboard_.press(keybinds[7])
        elif key.char == '9':
            keyboard_.press(keybinds[8])
        elif key.char == '0':
            keyboard_.press(keybinds[9])
    except AttributeError:
        print('special key {0} pressed'.format(key))
        if key == keyboard.Key.f1:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f2:
            keyboard_.press(Key.x)
        elif key == keyboard.Key.f3:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f4:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f5:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f6:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f7:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f8:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f9:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f10:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f11:
            keyboard_.press(Key.z)
        elif key == keyboard.Key.f12:
            keyboard_.press(Key.z)"""

def on_press(key):
    pass

def on_release(key):
    #print('{0} released'.format(key))
    if key == keyboard.Key.delete:
        # Stop listener
        return False

def get_key_from_string(key):
    if key=='esc':
        return Key.esc
    elif key=='space':
        return Key.space
    elif key=='return':
        return Key.enter
    elif key=='tab':
        return Key.tab
    elif key=='f1':
        return Key.f1
    elif key=='f2':
        return Key.f2
    elif key=='f3':
        return Key.f3
    elif key=='f4':
        return Key.f4
    elif key=='f5':
        return Key.f5
    elif key=='f6':
        return Key.f6
    elif key=='f7':
        return Key.f17
    elif key=='f8':
        return Key.f8
    elif key=='f9':
        return Key.f9
    elif key=='f10':
        return Key.f10
    elif key=='f11':
        return Key.f11
    elif key=='f12':
        return Key.f12
    elif key=='ctrl':
        return Key.ctrl
    else:
        print("Unknown key: "+var+" ("+str(len(var))+")")
        return None

def load_game(gameName):
    cwd = os.getcwd()
    game_config_lines=[]
    with open(cwd+'/GameConfigs/'+gameName+'.conf') as game_config:
        for line in game_config:
            game_config_lines.append(line.replace("\n",""))
    
    game_name = game_config_lines[0]              # game title
    #keybinds = game_config_lines[1].split(",")    # mapping from 0-9 and f1-f12 into game keys
    config_file = game_config_lines[1]            # dosbox config file
    game_path = game_config_lines[2]              # .EXE path
    
    #print(keybinds)
    print(config_file)
    print(game_path)

    # Start QJoypad
    copyfile(cwd+'/GameConfigs/'+gameName+'.lyt', '/home/david/.qjoypad3/'+gameName+'.lyt')
    cmd = ['./Qjoypad/qjoypad', gameName]
    pJoypad = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)    

    # Start game
    print(cwd+'/Games/'+gameName+'/'+game_path)
    cmd = ['dosbox', cwd+'/Games/'+gameName+'/'+game_path, '-conf', cwd+'/Configs/'+config_file]
    print("Running ",cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)    
    
    mod_ctrl = False
    for line in game_config_lines[3:]:
        command, var = line.replace("\n","").split(" ")
        if command=='sleep':
            time.sleep(float(var))
        elif command=='key':
            if len(var)==1:
                pressRelease(var)
            else:
                pressRelease(get_key_from_string(var))
                """for key in var.split("+"):
                    if key=='esc':
                        pressRelease(Key.esc)
                    elif key=='space':
                        pressRelease(Key.space)
                    elif key=='return':
                        pressRelease(Key.enter)
                    elif key=='tab':
                        pressRelease(Key.tab)
                    elif key=='f1':
                        pressRelease(Key.f1)
                    elif key=='f11':
                        pressRelease(Key.f11)
                    elif key=='ctrl':
                        mod_ctrl = True
                        keyboard_.press(Key.ctrl)
                    else:
                        print("Unknown key: "+var+" ("+str(len(var))+")")"""
        elif command=='hold':
            print("holding")
            keyboard_.press(get_key_from_string(var))
        elif command=='release': 
            print("releasing")   
            keyboard_.release(get_key_from_string(var))
    print("Done")

    
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    p.terminate()
    pJoypad.terminate()

load_game("DDerby")