import subprocess
import os
import time
from shlex import split
from sys import exit
import pynput
from dotenv import load_dotenv
from class_helpers import *

load_dotenv("customizations.env")

TOS_TOWN_MEMBERS = 15
TOS_NOTEPAD_WINDOW_NAME = "TOS-Notepad"
TERMINAL_NAME : str = None
match os.environ["TERMINAL"]:
    case "wezterm":
        TERMINAL_NAME = "wezterm"
    case "gnome-terminal":
        TERMINAL_NAME = "Terminal"
TERMINAL_COMMAND_FOR_NAME : dict[str,str]= {
    "wezterm" : f'flatpak run org.wezfurlong.wezterm cli spawn --new-window --cwd {os.path.dirname(os.path.abspath(__file__))} -- bash -c " vim assets/temp_tos.txt ; sleep 86400"',
    "gnome-terminal" : "gnome-terminal -e 'vim assets/temp_tos.txt'"
}
ACTION_STRING = os.environ["ACTION_STRING"]
TERMINAL_POSITION = [os.environ["TERMINAL_POSITION_X"],os.environ["TERMINAL_POSITION_Y"],os.environ["TERMINAL_WIDTH"],os.environ["TERMINAL_HEIGHT"]]
vote1_locations_dict = {}
vote2_locations_dict = {}
button_dict = {}
notepad_hidden: bool= False
MouseController = pynput.mouse.Controller


def get_current_windows_infos() -> list[WindowInfo]:
    command_stdout = subprocess.run(["wmctrl", "-lG"],capture_output=True)
    return [WindowInfo(unreadableWindowInfo) for unreadableWindowInfo in str(command_stdout.stdout).split(r"\n") if len(unreadableWindowInfo) >= 8]

def decide_tos_vote_positions(current_windows_infos):
    global vote1_locations_dict
    global vote2_locations_dict
    global button_dict
    result = False
    for windowInfo in current_windows_infos:
        if "Town" in windowInfo.window_name:
            result = True
            ending_y_position = (windowInfo.height/1.038) + windowInfo.position_y
            vote1_x_position = (windowInfo.width/1.031)+windowInfo.position_x
            vote2_x_position = (windowInfo.width/1.059)
            y_margin_between_votes = windowInfo.height/33.75
            for i in range(TOS_TOWN_MEMBERS,0,-1):
                vote1_locations_dict[i] = (vote1_x_position,ending_y_position-((TOS_TOWN_MEMBERS-i)*y_margin_between_votes))
                vote2_locations_dict[i] = (vote2_x_position,ending_y_position-((TOS_TOWN_MEMBERS-i)*y_margin_between_votes))
            button_dict["show_all"] = ScreenCoordinates(windowInfo,1.33,1.17)
            button_dict["show_alive"] = ScreenCoordinates(windowInfo,1.33,1.69)
            button_dict["inno"] = ScreenCoordinates(windowInfo,1.66,1.52)
            button_dict["guilty"] = ScreenCoordinates(windowInfo,2.53,1.52) 
            button_dict["ability"] = ScreenCoordinates(windowInfo,1.17,4.86) 
            button_dict["open_chat_filter"] = ScreenCoordinates(windowInfo,5.48,6.31)
            button_dict["filter_only"] = ScreenCoordinates(windowInfo,11.85,5.09)
            button_dict["open_chat"] = ScreenCoordinates(windowInfo,3.04,1.97)
            button_dict["clear_chat"] = ScreenCoordinates(windowInfo,3.16,6.39)
            chat_filter_margin = windowInfo.height/33.76
            for i in range(1,TOS_TOWN_MEMBERS+1):
                button_dict[f"chatlog{i}"] = ScreenCoordinates(windowInfo,5.59,5.29,add_y=i*chat_filter_margin)

    if result == False:
        print("Could not find TOS2 window.")

def move_mouse_to(pos_x:float | int,pos_y:float | int):
    MouseController.move(MouseController(),-3000,-3000)
    MouseController.move(MouseController(),pos_x,pos_y)

def click_button(button_num: int):
    if button_num == 1:
        MouseController.click(MouseController(),pynput.mouse.Button.left)
    if button_num == 2:
        MouseController.click(MouseController(),pynput.mouse.Button.right)

def show_all_members():
    move_mouse_to(*button_dict["show_all"].position)
    click_button(1)

def show_alive_members():
    move_mouse_to(*button_dict["show_alive"].position)
    click_button(1)

def vote1_tos(num):
    show_all_members()
    time.sleep(DELAY_TIME/3)
    move_mouse_to(*vote1_locations_dict[num])
    click_button(1)
    time.sleep(DELAY_TIME/3)
    show_alive_members()

def vote2_tos(num):
    show_all_members()
    time.sleep(DELAY_TIME/3)
    move_mouse_to(*vote2_locations_dict[num])
    click_button(1)
    time.sleep(DELAY_TIME/3)
    show_alive_members()

def decide_verdict_tos(verdict: bool):
    if verdict == True:
        move_mouse_to(*button_dict["guilty"].position)
    elif verdict == False:
        move_mouse_to(*button_dict["inno"].position)
    click_button(1)

def click_ability():
    move_mouse_to(*button_dict["ability"].position)
    click_button(1)

def filter_chat_by_number(num: int):
    move_mouse_to(*button_dict["open_chat"].position)
    click_button(1)
    time.sleep(DELAY_TIME)
    clear_chat_filter()
    time.sleep(DELAY_TIME)
    move_mouse_to(*button_dict["open_chat_filter"].position)
    click_button(1)
    time.sleep(DELAY_TIME)
    move_mouse_to(*button_dict[f"chatlog{num}"].position)
    click_button(1)
    time.sleep(DELAY_TIME)
    move_mouse_to(*button_dict["filter_only"].position)
    click_button(1)

def clear_chat_filter():
    move_mouse_to(*button_dict["clear_chat"].position)
    click_button(1)
    
def stop_program():
    print("Stopping program..")
    close_notepad(get_current_windows_infos())
    exit()

def open_tos_notepad():
    global notepad_hidden
    subprocess.run(split("cp assets/tos_template.txt assets/temp_tos.txt"))
    subprocess.run(split(TERMINAL_COMMAND_FOR_NAME[TERMINAL_NAME]))
    notepad_hidden = False

def modify_notepad_window(current_windows_infos: list[WindowInfo]):
    for WindowInstance in current_windows_infos:
        if WindowInstance.window_name == TERMINAL_NAME:
            WindowInstance.change_window_name(TOS_NOTEPAD_WINDOW_NAME)
            WindowInstance.change_window_dimensions(*TERMINAL_POSITION)
            WindowInstance.toggle_always_on_top(True)

def close_notepad(current_windows_infos: list[WindowInfo]):
    for WindowInstance in current_windows_infos:
        if WindowInstance.window_name == TOS_NOTEPAD_WINDOW_NAME:
            WindowInstance.soft_close_window() 

def toggle_notepad_minimized(toggle: bool | None = None):
    global notepad_hidden
    current_windows_infos = get_current_windows_infos()
    for WindowInstance in current_windows_infos:
        if WindowInstance.window_name == TOS_NOTEPAD_WINDOW_NAME:
            if toggle == None:
                WindowInstance.toggle_hidden(not notepad_hidden)
                notepad_hidden = not notepad_hidden
            else:
                WindowInstance.toggle_hidden(toggle)
                notepad_hidden = toggle


def restart_notepad():
    current_windows_infos = get_current_windows_infos()
    close_notepad(current_windows_infos)
    open_tos_notepad()
    time.sleep(DELAY_TIME)
    current_windows_infos = get_current_windows_infos()
    modify_notepad_window(current_windows_infos)

word_to_function = {
    os.environ["STOP_PROGRAM_PREFIX"]: {"func": stop_program,"args": []},
    os.environ["RESTART_PROGRAM_PREFIX"]: {"func": restart_notepad,"args": []},
    os.environ["GUILTY_PREFIX"]: {"func": decide_verdict_tos,"args": [True]},
    os.environ["INNOCENT_PREFIX"]: {"func": decide_verdict_tos,"args": [False]},
    os.environ["TOGGLE_MINIMIZED"]: {"func": toggle_notepad_minimized,"args": []},
    os.environ["MINIMIZE"]: {"func": toggle_notepad_minimized,"args": [True]},
    os.environ["UNMINIMIZE"]: {"func": toggle_notepad_minimized,"args": [False]},
    os.environ["ABILITY"]: {"func": click_ability,"args": []},
    os.environ["CLEAR_FILTER"]: {"func": clear_chat_filter,"args": []}
}

for i in range(1,TOS_TOWN_MEMBERS+1): #keep this
    word_to_function[f"{os.environ["VOTE1_PREFIX"]}{i}"] = {"func": vote1_tos,"args": [i]} 
    word_to_function[f"{os.environ["VOTE2_PREFIX"]}{i}"] = {"func": vote2_tos,"args": [i]}  
    word_to_function[f"{os.environ["FILTER_CHAT"]}{i}"] = {"func": filter_chat_by_number,"args": [i]}  

word_cached = ""
MAX_WORD_CACHED_LENGTH = 15
def _pynput_on_press(key):
    global word_cached
    try:
        if key == pynput.keyboard.KeyCode.from_char(ACTION_STRING):
            for func_word in list(word_to_function.keys()):
                if func_word in word_cached[-1*len(func_word):]:
                    print(f"Triggered event: {func_word}")
                    for _ in range(len(func_word)+1):
                        pynput.keyboard.Controller.press(pynput.keyboard.Controller(),pynput.keyboard.Key.backspace)
                        pynput.keyboard.Controller.release(pynput.keyboard.Controller(),pynput.keyboard.Key.backspace)
                    func_dict = word_to_function[func_word]
                    func_dict["func"](*func_dict["args"])
        if key == pynput.keyboard.Key.backspace and len(word_cached) > 0:
            word_cached = word_cached[0:-1]
        elif key == pynput.keyboard.Key.space:
            word_cached += " "
        else: 
            word_cached += key.char
    except Exception as e: # If key is special
        pass
    if len(word_cached) > MAX_WORD_CACHED_LENGTH:
        word_cached = word_cached[1:]

def _pynput_on_release(key):
    pass

def start_keyboard_listener():
    with pynput.keyboard.Listener(
            on_press=_pynput_on_press,
            on_release=_pynput_on_release) as listener:
        listener.join()

DELAY_TIME = 0.3
def main():
    open_tos_notepad()
    time.sleep(DELAY_TIME)
    current_windows_infos = get_current_windows_infos()
    modify_notepad_window(current_windows_infos)
    decide_tos_vote_positions(current_windows_infos)
    try:
        start_keyboard_listener()
    except Exception:
        pass

if __name__ == "__main__":
    main()