import sys
sys.path.insert(0, './')
from src.Player.game import Game

if __name__ == "__main__":

    up = sys.argv[1]
    down = sys.argv[2]
<<<<<<< HEAD

=======
    # up = 'q'
    # down = 'a'
>>>>>>> origin/restart_impl
    game = Game(up, down)
   