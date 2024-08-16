import subprocess
from shlex import split

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

    def toggle_hidden(self, toggle:bool) -> None:
        keyword = "add"
        if toggle == False:
            keyword = "remove"
        subprocess.run(split(f"wmctrl -ir {self.hex_value} -b {keyword},below"))

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

class ScreenCoordinates():
    def __init__(self,WindowInstance: WindowInfo | list, alpha_position_x: float | int,alpha_position_y: float | int, add_x: int = 0, add_y: int = 0,) -> None:
        self.x: int = int(WindowInstance.width/alpha_position_x) + WindowInstance.position_x + add_x
        self.y: int = int(WindowInstance.height/alpha_position_y) + WindowInstance.position_y + add_y
        self.position: tuple = (self.x,self.y)
    
