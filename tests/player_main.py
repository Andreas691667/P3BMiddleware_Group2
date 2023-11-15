import sys
sys.path.insert(0, './')
from src.Player.controller import Controller

if __name__ == "__main__":

    up = sys.argv[1]
    down = sys.argv[2]
    # up = 'q'
    # down = 'a'
    game = Controller(up, down)
   