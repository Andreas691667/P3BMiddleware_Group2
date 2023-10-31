import time
import random
from queue import Queue
from client import Client
from view import View
from model import Model
import keyboard


class Game():
    """Class for the game
    The game is responsible for running the game loop and updating the player's position"""

    def __init__(self) -> None:
        # Create the client
        # TODO: IMPORTANT: We need a notion of which player is left and which is right
        # This is just a placeholder for now
        self.set_player_id()
        self.client = Client(self.on_message, self.player_id)
        self.game_view = View()
        self.game_model = Model()
        self.incoming_message_queue = Queue()
        self.game_is_on: bool = False

        self.start_game()

    def set_player_id(self):
        """Generate a unique player id randomly"""
        time_ns = time.time_ns()
        random.seed(time_ns)
        self.player_id = random.randint(0, 1000000)

    def start_game(self):
        """Start the game loop"""
        
        # send new player msg to the server
        
        # wait for game to start
        while not self.game_is_on:     
            print("Waiting for game to start...")

        # when game starts, start game loop
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
        pass
        # TODO: update model!

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
            self.game_view.update_view(self.game_model.get_my_pos(), self.game_model.get_op_pos(), self.game_model.get_ball_pos())
            
            # ---- PUBLISH USER UPDATE ----
            self.client.send_message((self.player_id, self.game_model.get_my_pos()))


    def get_user_input(self) -> str:
        """Returns KEY_DOWN, KEY_UP or NO_KEY"""
        if (keyboard.is_pressed("down")):
            return 1
        elif (keyboard.is_pressed("up")):
            return -1
        else:
            return 0
    