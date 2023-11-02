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
    COUNTDOWN_SRV = "COUNTDOWN" # Type used to indicate that the game is starting


class POS_TYPES():
    """Position types"""
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class SCREEN_CONFIG():
    """Screen configuration"""
    SCREEN_WIDTH = 1300
    SCREEN_HEIGHT = 600
    LEFT_X = -SCREEN_WIDTH/2+110
    RIGHT_X = SCREEN_WIDTH/2-110

class PADDLE_CONFIG():
    """Paddle configuration"""
    PADDLE_WIDTH = 1
    PADDLE_HEIGHT = 6

class BALL_STATE():
    """Ball state"""
    BORDER_COLLISION = "BORDER_COLLISION"
    PADDLE_COLLISION = "PADDLE_COLLISION"
    RIGHT_GOAL = "RIGHT_GOAL"
    LEFT_GOAL = "LEFT_GOAL"
    NO_COLLISION = "NO_COLLISION"

class BALL_CONFIG():
    """Ball configuration"""
    BALL_RADIUS = 0.5
    MAX_BALL_SPEED = 15

# types
KEY_UP = "KEY_UP"
KEY_DOWN = "KEY_DOWN"
NO_KEY = "NO_KEY"
