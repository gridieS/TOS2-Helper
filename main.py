import subprocess
import time
from shlex import split
from sys import exit
import pynput

TOS_TOWN_MEMBERS = 15
TOS_NOTEPAD_WINDOW_NAME = "TOS-Notepad"
vote1_locations_dict = {}
vote2_locations_dict = {}
button_dict = {}
best_terminal_position = [850 , 710, 278, 411]
MouseController = pynput.mouse.Controller
class WindowInfo:
    index_to_attr_name = {
        "hex_value":0,
        "gravity":1,
        "position_x":2,
        "position_y": 3,
        "width":4,
        "height":5, 
        "device_name":6,
        "window_name":7
    } 
    def __init__(self,unreadableInfo: str):
        split_info = [attr for attr in unreadableInfo.split(" ") if attr != " " and attr != ""]
        for attr_name,attr_index in WindowInfo.index_to_attr_name.items():
            self.__setattr__(attr_name,split_info[attr_index])

        self.width = int(self.width)
        self.height = int(self.height)
        self.position_x = int(self.position_x)
        self.position_y = int(self.position_y)

    def change_window_name(self,new_name: str):
        subprocess.run(split(f"wmctrl -ir {self.hex_value} -N {new_name}"))

    def change_window_dimensions(self,position_x = None,position_y = None,width = None,height = None) -> None:
        if width == None:
            width = self.width
        if height == None:
            height = self.height
        if position_x == None:
            position_x = self.position_x
        if position_y == None:
            position_y = self.position_y

        subprocess.run(split(f"wmctrl -ir {self.hex_value} -e 0,{position_x},{position_y},{width},{height}"))
    def soft_close_window(self) -> None:
        subprocess.run(split(f"wmctrl -ic {self.hex_value}"))
        
    def toggle_always_on_top(self, toggle:bool) -> None:
        keyword = "add"
        if toggle == False:
            keyword = "remove"
            
        subprocess.run(split(f"wmctrl -ir {self.hex_value} -b {keyword},above"))

    def __str__(self) -> str:
        final_string = ""
        for attr_name,attr_value in self.__dict__.items():
            final_string += f"{attr_name}: {attr_value}, "
        return final_string

def get_current_windows_infos() -> list[WindowInfo]:
    command_stdout = subprocess.run(["wmctrl", "-lG"],capture_output=True)
    return [WindowInfo(unreadableWindowInfo) for unreadableWindowInfo in str(command_stdout.stdout).split(r"\n") if len(unreadableWindowInfo) >= 8]


def decide_tos_vote_positions(current_windows_infos):
    # 58 38.4,32 40
    global vote1_locations_dict
    global vote2_locations_dict
    global button_dict
    result = False
    for windowInfo in current_windows_infos:
        if "Town" in windowInfo.window_name:
            result = True
            ending_y_position = windowInfo.height - (windowInfo.height/27)+windowInfo.position_y
            vote1_x_position = windowInfo.width - (windowInfo.width/33.1)+windowInfo.position_x
            vote2_x_position = vote1_x_position-(windowInfo.width/38.4)
            y_margin_between_votes = windowInfo.height/33.75
            for i in range(TOS_TOWN_MEMBERS,0,-1):
                vote1_locations_dict[i] = (vote1_x_position,ending_y_position-((TOS_TOWN_MEMBERS-i)*y_margin_between_votes))
                vote2_locations_dict[i] = (vote2_x_position,ending_y_position-((TOS_TOWN_MEMBERS-i)*y_margin_between_votes))
            members_buttons_x_position = windowInfo.width -(windowInfo.width/4)+windowInfo.position_x
            show_alive_y_position = windowInfo.height -(windowInfo.height/2.4)+windowInfo.position_y
            show_all_y_position = windowInfo.height -(windowInfo.height/6.75)+windowInfo.position_y
            button_dict["show_all"] = (members_buttons_x_position,show_all_y_position)
            button_dict["show_alive"] = (members_buttons_x_position,show_alive_y_position)
            decision_buttons_y_position = windowInfo.height - (windowInfo.height/2.9) + windowInfo.position_y
            inno_x_position = windowInfo.width -(windowInfo.width/2.5)+windowInfo.position_x
            guilty_x_position = windowInfo.width -(windowInfo.width/1.65)+windowInfo.position_x
            button_dict["inno"] = (inno_x_position,decision_buttons_y_position)
            button_dict["guilty"] = (guilty_x_position,decision_buttons_y_position)

    if result == False:
        print("Could not find TOS2 window.")

def move_mouse_to(posx:float | int,posy:float | int):
    MouseController.move(MouseController(),-3000,-3000)
    MouseController.move(MouseController(),posx,posy)

def show_all_members():
    move_mouse_to(int(button_dict["show_all"][0]),int(button_dict["show_all"][1]))
    MouseController.click(MouseController(),pynput.mouse.Button.left)

def show_alive_members():
    move_mouse_to(int(button_dict["show_alive"][0]),int(button_dict["show_alive"][1]))
    MouseController.click(MouseController(),pynput.mouse.Button.left)

def vote1_tos(num):
    show_all_members()
    time.sleep(DELAY_TIME/3)
    move_mouse_to(int(vote1_locations_dict[num][0]),int(vote1_locations_dict[num][1]))
    MouseController.click(MouseController(),pynput.mouse.Button.left)
    time.sleep(DELAY_TIME/3)
    show_alive_members()

def vote2_tos(num):
    show_all_members()
    time.sleep(DELAY_TIME/3)
    move_mouse_to(int(vote2_locations_dict[num][0]),int(vote2_locations_dict[num][1]))
    MouseController.click(MouseController(),pynput.mouse.Button.left)
    time.sleep(DELAY_TIME/3)
    show_alive_members()

def decide_verdict_tos(verdict: bool):
    if verdict == True:
        move_mouse_to(button_dict["guilty"][0],button_dict["guilty"][1])
    elif verdict == False:
        move_mouse_to(button_dict["inno"][0],button_dict["inno"][1])
    MouseController.click(MouseController(),pynput.mouse.Button.left)

def stop_program():
    print("Stopping program..")
    close_notepad(get_current_windows_infos())
    exit()

def open_tos_notepad():
    subprocess.run(split("cp assets/tos_template.txt assets/temp_tos.txt"))
    subprocess.run(split("gnome-terminal -e 'vim assets/temp_tos.txt'"))

def modify_notepad_window(current_windows_infos: list[WindowInfo]):
    for WindowInstance in current_windows_infos:
        if WindowInstance.window_name == "Terminal":
            WindowInstance.change_window_name(TOS_NOTEPAD_WINDOW_NAME)
            WindowInstance.change_window_dimensions(*best_terminal_position)
            WindowInstance.toggle_always_on_top(True)

def close_notepad(current_windows_infos: list[WindowInfo]):
    for WindowInstance in current_windows_infos:
        if WindowInstance.window_name == TOS_NOTEPAD_WINDOW_NAME:
            WindowInstance.soft_close_window() 


def restart_notepad():
    current_windows_infos = get_current_windows_infos()
    close_notepad(current_windows_infos)
    open_tos_notepad()
    time.sleep(DELAY_TIME)
    current_windows_infos = get_current_windows_infos()
    modify_notepad_window(current_windows_infos)

word_to_function = {
    "stop program": {"func": stop_program,"args": []},
    "restart": {"func": restart_notepad,"args": []},
    "guilty": {"func": decide_verdict_tos,"args": [True]},
    "inno": {"func": decide_verdict_tos,"args": [False]},
    "innocent": {"func": decide_verdict_tos,"args": [False]},
}

for i in range(1,TOS_TOWN_MEMBERS+1): #keep this
    word_to_function[f"vote1 {i}"] = {"func": vote1_tos,"args": [i]} 
    word_to_function[f"vote2 {i}"] = {"func": vote2_tos,"args": [i]}  

word_cached = ""
MAX_WORD_CACHED_LENGTH = 15
def _pynput_on_press(key):
    global word_cached
    try: 
        if key == pynput.keyboard.KeyCode.from_char("`"):
            for func_word in list(word_to_function.keys()):
                if func_word in word_cached[-1*len(func_word):]:
                    print(f"Triggered event: {func_word}")
                    for _ in range(len(func_word)+1):
                        pynput.keyboard.Controller.press(pynput.keyboard.Controller(),pynput.keyboard.Key.backspace)
                        pynput.keyboard.Controller.release(pynput.keyboard.Controller(),pynput.keyboard.Key.backspace)
                    func_dict = word_to_function[func_word]
                    func_dict["func"](*func_dict["args"])
        elif key == pynput.keyboard.Key.backspace and len(word_cached) > 0:
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