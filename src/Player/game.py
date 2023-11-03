import sys
sys.path.insert(0, './src/Player')
sys.path.insert(0, './src/Utility')
from config import MSG_TYPES, POS_TYPES
import message_parsing
import keyboard
from model import Model
from view import View
from client import Client
from queue import Queue
import random
import time

class Game():
    """Class for the game
    The game is responsible for running the game loop and updating the player's position"""
    def __init__(self, key_up : str, key_down : str) -> None:
        self.set_player_id()
        self.client = Client(self.on_message, self.player_id)
        self.game_view = View()
        self.game_model = Model()
        self.incoming_message_queue = Queue()
        self.game_is_on: bool = False
        self.key_up : str = key_up
        self.key_down : str = key_down
        self.refresh_rate: int = 10
        self.change_score = False
        self.game_finished : bool = False
        self.winner : str = ""

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

        print("Waiting for game to start...")

        # wait for game to start
        while not self.game_is_on:
            # Waiting for position/game start 
            while self.incoming_message_queue.empty():
                pass
                # print("Waiting for game to start...")
            # when message comes, pass it to handle_message
            # if yes, set opponent position and own position
            msg = self.incoming_message_queue.get()
            self.handle_message(msg)

        # start game
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
            self.game_model.set_my_x_pos(msg_payload)
            self.game_model.set_op_x_pos(POS_TYPES.LEFT if self.game_model.my_x_pos == POS_TYPES.RIGHT else POS_TYPES.RIGHT)
            

        elif msg_type == MSG_TYPES.GAME_CAN_START_SRV:
            # start game
            self.game_is_on = True
            self.game_view.clear_countdown()
            self.game_view.clear_player_position()
            self.game_view.set_player_colors()

        elif msg_type == MSG_TYPES.COUNTDOWN_SRV:
            print("Countdown: ", msg_payload)
            print(f"You are: {self.game_model.get_my_x_pos()}")
            self.game_view.show_player_position(self.game_model.get_my_x_pos())
            self.game_view.show_countdown(msg_payload)

        elif msg_type == MSG_TYPES.GAME_UPDATE_SRV:
            ball_pos = msg_payload["ball_pos"]
            op_y_pos = msg_payload["op_y_pos"]
            my_y_pos = msg_payload["my_y_pos"]
            left_score = msg_payload["left_score"]
            right_score = msg_payload["right_score"]
            game_finished = msg_payload["game_finished"]

            my_score = left_score if self.game_model.my_x_pos == POS_TYPES.LEFT else right_score
            op_score = left_score if self.game_model.my_x_pos == POS_TYPES.RIGHT else right_score

            # Evaluate if score have changed
            if (my_score != self.game_model.get_my_score() or op_score != self.game_model.get_op_score()):
                self.change_score = True

            self.game_model.set_my_y_pos(my_y_pos)
            self.game_model.set_op_y_pos(op_y_pos)
            self.game_model.set_ball_pos(ball_pos)
            self.game_model.set_my_score(my_score)
            self.game_model.set_op_score(op_score)

            if game_finished[0]:
                self.game_finished = True
                self.winner = game_finished[1]
                print("Game finished!", game_finished)
                

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

            # ---- UPDATE VIEW ----
            self.game_view.update_view(self.game_model.get_my_y_pos(),
                                       self.game_model.get_op_y_pos(),
                                       self.game_model.get_ball_pos(),
                                       self.game_model.get_my_x_pos(),
                                        self.game_model.get_my_score(),
                                        self.game_model.get_op_score(),
                                        self.change_score
                                       )
            # Reset
            self.change_score = False

            # check if game has finished
            if self.game_finished:
                self.game_view.show_winner(self.winner)
                self.game_is_on = False
                break

            if dt != 0:
                # ---- PUBLISH USER UPDATE ----
                self.client.send_message(
                    (message_parsing.encode_message(MSG_TYPES.PLAYER_UPDATE_USR,
                                                    self.player_id,
                                                    dt)))
            
            # time.sleep(1/self.refresh_rate)

    def get_user_input(self) -> str:
        """Returns KEY_DOWN, KEY_UP or NO_KEY""" 
        if (keyboard.is_pressed(self.key_up)):
            return 10
        elif (keyboard.is_pressed(self.key_down)):
            return -10
        else:
            return 0