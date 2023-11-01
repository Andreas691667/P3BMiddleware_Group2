from config import MSG_TYPES, POS_TYPES
import message_parsing
import keyboard
from model import Model
from view import View
from client import Client
from queue import Queue
import random
import time
import sys
sys.path.insert(0, './src/Player')
sys.path.insert(0, './src/Utility')


class Game():
    """Class for the game
    The game is responsible for running the game loop and updating the player's position"""

    def __init__(self) -> None:
        self.set_player_id()
        self.client = Client(self.on_message, self.player_id)
        self.game_view = View()
        self.game_model = Model()
        self.incoming_message_queue = Queue()
        self.game_is_on: bool = False
        self.my_pos: str = ""
        self.op_pos: str = ""

        self.start_game()

    def set_player_id(self):
        """Generate a unique player id randomly"""
        time_ns = time.time_ns()
        random.seed(time_ns)
        self.player_id = random.randint(0, 1000000)

    def start_game(self):
        """Start the game loop when accepted by server"""
        # send new player msg to the server
        new_player_msg = message_parsing.encode_message(
            MSG_TYPES.NEW_PLAYER_USR, self.player_id, "")
        self.client.send_message(new_player_msg)

        # wait for game to start
        while not self.game_is_on:
            while self.incoming_message_queue.empty():
                print("Waiting for game to start...")
            # when message comes, pass it to handle_message
            # if yes, set opponent position and own position
            msg = self.incoming_message_queue.get()
            self.handle_message(msg)

        self.main_game_loop()

    def on_message(self, ch, method, properties, body):
        """Callback function for when a message is received
        ch: The channel object
        method: The method object
        properties: The properties object
        body: The message body
        This function is called when a message is received from the server
        It is responsible for updating the queue of incoming messages"""
        self.incoming_message_queue.put(body)

    def handle_message(self, msg):
        """Handle the message"""
        # TODO: update model!
        msg_type, sender_id, msg_payload = message_parsing.decode_message(msg)
        print("Player received message: ", msg)
        if msg_type == MSG_TYPES.PLAYER_POSITION_INIT_SRV:
            # set opponent position and own position
            self.my_pos = msg_payload
            self.op_pos = POS_TYPES.LEFT if self.my_pos == POS_TYPES.RIGHT else POS_TYPES.RIGHT

        elif msg_type == MSG_TYPES.GAME_CAN_START_SRV:
            # start game
            self.game_is_on = True

        elif msg_type == MSG_TYPES.GAME_UPDATE_SRV:
            self.game_model.increment_op_pos(msg_payload)

    def main_game_loop(self):
        """The main game loop"""
        while self.game_is_on:

            # ---- UPDATE OPPONENTS PADDLE & BALL POSITION ----
            # Check queue for incoming messages
            if not self.incoming_message_queue.empty():
                msg = self.incoming_message_queue.get()
                self.handle_message(msg)

            # ---- UPDATE MY PADDLE ----
            # Get user input
            dt = self.get_user_input()

            # Update model
            self.game_model.increment_my_pos(dt)

            # ---- UPDATE VIEW ----
            self.game_view.update_view(self.game_model.get_my_pos(
            ), self.game_model.get_op_pos(), self.game_model.get_ball_pos(), self.my_pos)

            if dt != 0:
                # ---- PUBLISH USER UPDATE ----
                self.client.send_message(
                    (message_parsing.encode_message(MSG_TYPES.PLAYER_UPDATE_USR, self.player_id, self.game_model.get_my_pos())))

    def get_user_input(self) -> str:
        """Returns KEY_DOWN, KEY_UP or NO_KEY"""

        if (keyboard.is_pressed("up")):
            return 0.1
        elif (keyboard.is_pressed("down")):
            return -0.1
        else:
            return 0
