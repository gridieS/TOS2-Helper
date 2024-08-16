
# TOS2 Vim Helper

A Town of Salem 2 helper, including a Vim notepad and custom commands (macros) accessed from your keyboard only, meaning you almost don't have to touch your mouse!



# Requirements

Vim and gnome-terminal, Can be installed with your distro's package manger, for example:

For debian users:
```bash
  sudo apt install vim gnome-terminal
```

Or for fedora/red hat users:
```bash
  sudo dnf install vim gnome-terminal
```

[Python3](https://www.python.org/downloads/) 

[Pip](https://pypi.org/project/pip/)  Can be installed with:
```bash
  python3 -m ensurepip
```

# Installing and running (bash)

Clone the project 

```bash
  git clone https://github.com/gridieS/TOS2-Helper
```

Go to the project directory

```bash
  cd TOS2-Helper
```

Install requirements
```bash
  pip install -r requirements.txt
```
Then, to run the program:
```bash
  ./quick_start.sh
```
# All Commands

<!-- ACTION_STRING="`"
STOP_PROGRAM_PREFIX="stop"
RESTART_PROGRAM_PREFIX="restart"
VOTE1_PREFIX="vote1 "
VOTE2_PREFIX="vote2 "
GUILTY_PREFIX="guilty"
INNOCENT_PREFIX="inno"
TERMINAL_WIDTH="278"
TERMINAL_HEIGHT="411"
TERMINAL_POSITION_X="850"
TERMINAL_POSITION_Y="710"
TOGGLE_MINIMIZED="toggle"
MINIMIZE="hide"
UNMINIMIZE="show"
ABILITY="ability"
FILTER_CHAT="filter "
CLEAR_FILTER="clear" -->
To perform all of the following commands, you have to set an action key ("`" by default) in the customizations.env file, then type your desired command and press the action key. (For example: guilty` will perform the guilty macro)

All of the following commands and their keywords are customizable in the customizations.env file.


#### stop
Stops the program, closing the notepad and stopping the keyboard listener.
#### restart
Closes and opens your notepad with the template in the assets/tos_template.txt file.
#### vote1 <player_num> 
Votes/Targets the player_num you entered.
#### vote2 <player_num> 
Targets the player_num you entered. (For example, usable when you're a witch and want to send your target to player_num)
#### guilty 
Presses the guilty when theres a trial.
#### inno 
Presses the innocent when theres a trial.
#### toggle
Unminimizes/Minimizes the notepad depending on it's status.
#### hide
Hides the notepad.
#### show
Shows the notepad.
#### ability
Presses the ability icon (For example, the veteran's "Alert" button is an ability button).
#### filter <player_num>
Performs a macro that shows you the chat logs of only the player_num you entered.
#### clear
Clears the chat filter.

