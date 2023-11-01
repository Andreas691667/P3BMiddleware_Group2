import sys
sys.path.insert(0, './')

from src.Player.game import Game
from src.Server.server import Server

if __name__ == "__main__":
    # start server
    server = Server()

    # start game
    game1 = Game()
    game2 = Game()
