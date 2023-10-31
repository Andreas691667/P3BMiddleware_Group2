""" RMQ configurations """
RMQ_CONFIG = {"SERVER_IP": "localhost",
              "SERVER_PORT": 5672,
              "SERVER_EXCHANGE": "server_updates",
              "USER_EXCHANGE": "user_updates"}

# SERVER_IP = "localhost" # localhost
# SERVER_PORT = 5672      # default port for RMQ
# SERVER_EXCHANGE = "server_updates"
# USER_EXCHANGE = "user_updates"

# msg types
MSG_TYPES = {"NEW_PLAYER": "NEW_PLAYER",
             "PLAYER_POSITION_INIT": "PLAYER_POSITION_INIT",
             "PLAYER_UPDATE": "PLAYER_UPDATE"}

# types
KEY_UP = "KEY_UP"
KEY_DOWN = "KEY_DOWN"
NO_KEY = "NO_KEY"
