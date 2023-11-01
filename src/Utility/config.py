from enum import Enum


class RMQ_CONFIG():
    """RabbitMQ configuration"""
    SERVER_IP = "localhost"
    SERVER_PORT = 5672
    SERVER_EXCHANGE = "server_updates"
    USER_EXCHANGE = "user_updates"

class MSG_TYPES():
    """Message types"""
    NEW_PLAYER_USR = "NEW_PLAYER" # Type used to indicate a new player wants to join the game
    PLAYER_POSITION_INIT_SRV = "PLAYER_POSITION_INIT" # Type used to indicate which side the player is on, i.e. left or right
    PLAYER_UPDATE_USR = "PLAYER_UPDATE" # Type used to indicate when a player have moved
    # Type used to indicate a change of game state, that is positions of players and ball
    GAME_UPDATE_SRV = "GAME_UPDATE"
    GAME_CAN_START_SRV = "GAME_CAN_START" # Type used to indicate that the game can start (i.e. there are now two players)

class POS_TYPES():
    """Position types"""
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class SCREEN_CONFIG():
    """Screen configuration"""
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    LEFT_X = -400
    RIGHT_X = 400

# types
KEY_UP = "KEY_UP"
KEY_DOWN = "KEY_DOWN"
NO_KEY = "NO_KEY"
