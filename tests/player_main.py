import sys
sys.path.insert(0, './')
from src.Player.game import Game

if __name__ == "__main__":

    up = sys.argv[1]
    down = sys.argv[2]

    game = Game(up, down)
   