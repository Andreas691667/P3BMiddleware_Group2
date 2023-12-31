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
from threading import Event
import random
import time

class Controller():
    """Class for the game
    The game is responsible for running the game loop and updating the player's position"""
    def __init__(self, key_up : str, key_down : str) -> None:
        self.set_player_id()
        self.client = Client(self.on_message, self.player_id)
        self.game_view = View(key_up, key_down)
        self.game_model = Model()
        self.incoming_message_queue = Queue()
        self.game_is_on: bool = False
        self.key_up : str = key_up
        self.key_down : str = key_down
        self.key_restart : str = key_down
        self.refresh_rate: int = 10
        self.change_score = False
        self.game_finished : bool = False
        self.winner : str = ""
        self.stop_main_loop = Event()
        self.msg_send_times : dict[int, int] = {} # msg_id => tid
        self.latest_send_msg_id: int = -1

        # measurement
        self.message_count = 0
        self.msg_data: list[tuple[int, int]] = [] # (msg_id, time_interval_in_ms) 
        self.key_stroke_log: list[(str, int)] = [] # (key, time_in_ms)

        self.start_game()

    def add_msg_data (self, msg_id, time_stamp, transmission_time, queue_size):
        """d"""
        self.msg_data.append((msg_id, time_stamp, transmission_time, queue_size))
    
    def get_msg_data (self) -> list:
        """d"""
        return self.msg_data
    
    def add_keystroke (self, key, _time):
        """d"""
        self.key_stroke_log.append((key, _time))
    
    def get_key_strokes_data (self) -> list:
        """d"""
        return self.key_stroke_log
    
    def set_player_id(self):
        """Generate a unique player id randomly"""
        time_ns = time.time_ns()
        random.seed(time_ns)
        self.player_id = random.randint(0, 1000000)

    def start_game(self):
        """Start the game loop when accepted by server"""
        # initialize game by asking game server
        self.initialize_game()

        # when game is initialized (ack by server),
        # start game by running main game loop
        self.main_game_loop()
    
    def initialize_game(self):
        """Initialize the game"""
        # send new player msg to the server
        new_player_msg = message_parsing.encode_message(
            MSG_TYPES.NEW_PLAYER_USR, self.player_id, self.calculate_msg_id(), "")
        
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
        msg_type, sender_id, msg_id, msg_payload = message_parsing.decode_message(msg)
        # print("Player received message: ", msg)
        if msg_type == MSG_TYPES.PLAYER_POSITION_INIT_SRV:
            # set opponent position and own position
            self.game_model.set_my_x_pos(msg_payload)
            self.game_model.set_op_x_pos(POS_TYPES.LEFT if self.game_model.my_x_pos == POS_TYPES.RIGHT else POS_TYPES.RIGHT)
            

        elif msg_type == MSG_TYPES.GAME_CAN_START_SRV:
            # start game
            print("Recieved start game")
            print(f"You are: {self.game_model.get_my_x_pos()}")
            self.game_is_on = True
            self.game_view.clear_countdown()
            self.game_view.clear_player_position()
            self.game_view.set_player_colors()

        elif msg_type == MSG_TYPES.COUNTDOWN_SRV:
            print("Countdown: ", msg_payload)
            self.game_view.show_player_position(self.game_model.get_my_x_pos())
            self.game_view.show_countdown(msg_payload)

        elif msg_type == MSG_TYPES.GAME_UPDATE_SRV:
            ball_pos = msg_payload["ball_pos"]
            op_y_pos = msg_payload["op_y_pos"]
            my_y_pos = msg_payload["my_y_pos"]
            op_y_pos_msg_id = msg_payload["op_y_pos_msg_id"]
            my_y_pos_msg_id = msg_payload["my_y_pos_msg_id"]
            left_score = msg_payload["left_score"]
            right_score = msg_payload["right_score"]
            game_finished = msg_payload["game_finished"]

            
            # Find message send time and figure out if it have been logged
            if (not self.msg_was_logged(my_y_pos_msg_id) and my_y_pos_msg_id != -1):
                self.log_msg(my_y_pos_msg_id)

            # Set message ID in model if it have changed
            # If the latest send msg id is not equal to the incomming my_y_pos_msg_id? 
            # Then ta
            # if (self.game_model.get_my_latest_msg_id() != my_y_pos_msg_id and my_y_pos_msg_id != -1):

            #     self.game_model.set_my_latest_msg_id(my_y_pos_msg_id)
            #     # Calculate traversel time
            #     cur_time = time.time_ns()
            #     time_traversed = (cur_time - self.msg_send_times[my_y_pos_msg_id])/10**6
            #     queue_size = self.incoming_message_queue.qsize()
            #     self.add_msg_data(my_y_pos_msg_id, cur_time, time_traversed, queue_size)

            # if (self.game_model.get_op_latest_msg_id() != op_y_pos_msg_id and op_y_pos_msg_id != -1):
            #     self.game_model.set_op_latest_msg_id(op_y_pos_msg_id)


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
                self.write_log_to_file()
                # print(self.get_msg_data())
                # print([t for id, t in self.get_msg_data()])

    def msg_was_logged(self, msg_id: int) -> bool:
        # Find msg_id in msg_data: list[tuple[int, int]] -> (msg_id, time_interval_in_ms) 
        logged_msg_ids = [t[0] for t in self.msg_data]

        # Check if msg_id is in list
        try:
            logged_msg_ids.index(msg_id) # Try to find index. Raise exception if not found, go to else if found
        except:
            return False # Exception -> not found
        else:
            return True # Found

    def log_msg(self, msg_id: int) -> None:
        """Log message to message log"""
        self.game_model.set_my_latest_msg_id(msg_id)
        # Calculate traversel time
        cur_time = time.time_ns()
        time_traversed = (cur_time - self.msg_send_times[msg_id])/10**6
        queue_size = self.incoming_message_queue.qsize()
        self.add_msg_data(msg_id, cur_time, time_traversed, queue_size)

    def write_log_to_file(self):
        # TODO: vi skal have en log til player updates og en til keystrokes
        # TODO: men virkede det at skrive i mappen? Prøver lige selv at kører det, 2 sek \thumbsup \nice lol
        file = open(f"./log_files/transmission_times/{self.player_id}_pl_log.txt", "w")
        # write content of msg_data
        for msg_id, timestamp, transmission_time, queue_size in self.get_msg_data():
            file.write(f"{msg_id};{timestamp};{transmission_time};{queue_size} \n")
        file.close() 
        
    def calculate_msg_id (self):
        """calculates message id"""
        self.message_count += 1
        self.latest_send_msg_id = int(str(self.player_id) + str(self.message_count))
        return self.latest_send_msg_id
    

    def main_game_loop(self):
        """The main game loop"""
        while not self.stop_main_loop.is_set():
            while self.game_is_on:

                # ---- UPDATE OPPONENTS PADDLE & BALL POSITION ----
                # Check queue for incoming messages
                if not self.incoming_message_queue.empty():
                    msg = self.incoming_message_queue.get()
                    self.handle_message(msg)

                # ---- UPDATE VIEW ----
                self.game_view.update_view( self.game_model.get_my_y_pos(),
                                            self.game_model.get_op_y_pos(),
                                            self.game_model.get_ball_pos(),
                                            self.game_model.get_my_x_pos(),
                                            self.game_model.get_my_score(),
                                            self.game_model.get_op_score(),
                                            self.change_score
                                        )
                # Reset change score flag
                self.change_score = False

                # check if game has finished
                if self.game_finished:
                    self.game_view.show_winner(self.winner)
                    self.game_is_on = False
                    break

                # ---- UPDATE MY PADDLE ----
                # Get user input
                dt = self.get_user_input()

                if dt != 0:
                    # ---- PUBLISH USER UPDATE ----
                    self.client.send_message(
                        (message_parsing.encode_message(MSG_TYPES.PLAYER_UPDATE_USR,
                                                        self.player_id,
                                                        self.calculate_msg_id(),
                                                        dt)))
                    self.msg_send_times.update({self.latest_send_msg_id: time.time_ns()})
                
            self.stop_game()

    def stop_game(self):
        """Stop the game and wait for restart"""

        # ---- RESET GAME ----
        self.game_finished = False
        self.game_view.show_restart_msg()

        # ---- WAIT FOR NEW GAME ----
        # wait until key is pressed
        restart_game : bool = False
        while True:
            # Restart game by pressing down
            if keyboard.is_pressed(self.key_down):
                restart_game = True
                break
            
            # Exit game by pressing up
            elif keyboard.is_pressed(self.key_up):
                print("Exiting game...")
                self.stop_main_loop.set()
                # self.client # TODO: close connection
                self.game_view.close_screen()
                sys.exit(0)

        if restart_game:
            print("Restarting game...")
            self.winner = ""
            self.game_view.reset_view()
            # when space is pressed, init game
            self.initialize_game()

    def get_user_input(self) -> str:
        """Returns KEY_DOWN, KEY_UP or NO_KEY""" 
        if (keyboard.is_pressed(self.key_up)):
            self.add_keystroke(self.key_up, time.time_ns()/10**6)
            return 30
        elif (keyboard.is_pressed(self.key_down)):
            self.add_keystroke(self.key_down, time.time_ns()/10**6)
            return -30
        else:
            return 0