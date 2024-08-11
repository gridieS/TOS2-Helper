
# TOS2 Vim Helper

A Town of Salem 2 helper, including a Vim notepad and some custom commands (such as guilty, or inno) that you can type and press your desired action key, then your mouse will automatically do that action in TOS2, without you having to move your mouse!


# Requirements

Vim, Can be installed with your distro's package manger, for example:

For debian users:
```bash
  sudo apt install vim
```

Or for fedora/red hat users:
```bash
  sudo dnf install vim
```

[Python3](https://www.python.org/downloads/) 

[Pip](https://pypi.org/project/pip/)  Can be installed with:
```bash
  python3 -m ensurepip
```
[Pipenv](https://pypi.org/project/pipenv/)  Can be installed with:
```bash
  python3 -m pip install pipenv
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
  ./quickstart.sh
```
# All Commands

#### guilty 
Presses the guilty when theres a trial.
#### inno 
Presses the innocent when theres a trial.
#### vote1 <player_num> 
Votes/Targets the player_num you entered.
#### vote2 <player_num> 
Targets the player_num you entered. (For example, usable when you're a witch and want to send your target to player_num)

