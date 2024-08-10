script_directory=$(dirname "$(realpath $0)")
cd $script_directory
pipenv shell &
pipenv run python3 main.py
