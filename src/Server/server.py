import sys
sys.path.insert(0, './src/Utility')
from threading import Thread, Event, Lock
import pika
import message_parsing
from config import RMQ_CONFIG, MSG_TYPES, POS_TYPES, BALL_STATE, BALL_CONFIG
import collision
import time
import random

class Server():
    """Class for the leader of the game"""

    def __init__(self) -> None:
        self.game_is_on: bool = False

        self.incoming_channel = self.create_channel()
        self.outgoing_channel = self.create_channel()
        self.configure_incoming_channel()
        self.configure_outgoing_channel()

        # Model variables
        self.x_positions: dict[int, str] = {}    # player_id : int => x_pos : str (LEFT or RIGHT)
        self.y_positions: dict[int, int] = {}    # player_id : int => y_pos : int
        self.latest_msg_ids: dict[int, int] = {} # player_id : int => msg_id : int
        self.ball_pos: (int, int) = (0, 0)
        self.d_ball: (int, int) = (BALL_CONFIG.MAX_BALL_SPEED, BALL_CONFIG.MAX_BALL_SPEED)
        self.refresh_rate: int = 10
        self.left_score: int = 0
        self.right_score: int = 0
        self.winner: str = ""
        self.winning_score = 5
        self.svr_msg_id = 0

        self.consumer_thread = Thread(target=self.start_consuming)
        self.state_thread = Thread(target=self.state_thread_fun)
        
        self.state_thread_stop_event = Event()
        self.mutex = Lock()
        
        self.queue_sizes : list([int, int]) = [] # queue len and timestamp [ns]

        self.consumer_thread.start()
        self.state_thread.start()


    def create_channel(self):
        """Configure the server"""
        # The connection object
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RMQ_CONFIG.SERVER_IP, port=RMQ_CONFIG.SERVER_PORT))
        # The channel object
        channel = connection.channel()

        return channel

    def configure_incoming_channel(self):
        """Configure the consumer channel"""
        self.incoming_channel.exchange_declare(
            exchange=RMQ_CONFIG.USER_EXCHANGE, exchange_type='fanout')  # for incomming messages
        
        # Declare the queue (Name is generated uniquely by RMQ)
        # Incoming message queue
        self.result = self.incoming_channel.queue_declare(queue='', exclusive=True)
        self.incoming_message_queue = self.result.method.queue

        # Bind the queue to the exchange
        self.incoming_channel.queue_bind(
            exchange=RMQ_CONFIG.USER_EXCHANGE, queue=self.incoming_message_queue)

        # Create a consumer for the incoming message queue
        self.incoming_channel.basic_consume(
            queue=self.incoming_message_queue, on_message_callback=self.on_message, auto_ack=True)

    def configure_outgoing_channel(self):
        """Configure the outgoing channel"""
        self.outgoing_channel.exchange_declare(
            exchange=RMQ_CONFIG.SERVER_EXCHANGE, exchange_type='direct')  # for incoming messages

    def send_message(self, message, player_id):
        """Send message to the rabbitmq server
        message: The message to send
        This is done by publishing the message to the server updates queue
        The routing key is the player id =(left or right)"""
        self.outgoing_channel.basic_publish(
            exchange=RMQ_CONFIG.SERVER_EXCHANGE, routing_key=str(player_id), body=message)

    def assign_player_x_position(self, player_id):
        """Assign a player position to the player
        player_id: The id of the player to assign a position to"""
        # first player to join game is always left
        if len(self.x_positions) == 0:
            self.x_positions[player_id] = POS_TYPES.LEFT
        else:
            self.x_positions[player_id] = POS_TYPES.RIGHT

        # if two players have joined, initialize y-pos and msg_ids and the game can start (return true)
        if len(self.x_positions) == 2:
            self.y_positions = {player_id: 0 for player_id in self.x_positions}
            self.latest_msg_ids = {player_id: -1 for player_id in self.x_positions}
            return True
        else:
            return False

    def update_player_model(self, player_id, msg_id, new_y_pos):
        """Update the player's position
        player_id: The id of the player to update
        new_pos: The new position of the player
        returns opposite id than sender
        """
        # Update position of player that sent message
        self.mutex.acquire()
        if not collision.paddle_wall_collision(new_y_pos):
            self.y_positions[player_id] += new_y_pos

        self.latest_msg_ids[player_id] = msg_id
        self.mutex.release()

    def calculate_msg_id (self):
        """calculate msg id for server"""
        self.svr_msg_id += 1
        return self.svr_msg_id

    def handle_message(self, msg):
        """Handle the message
        msg: The message to handle in json format"""
        msg_type, sender_id, msg_id, msg_payload = message_parsing.decode_message(msg)

        if msg_type == MSG_TYPES.NEW_PLAYER_USR:
            game_can_start : bool = self.assign_player_x_position(sender_id)
            # send player position to back to player
            player_pos_msg = message_parsing.encode_message(
                MSG_TYPES.PLAYER_POSITION_INIT_SRV, sender_id, self.calculate_msg_id(), self.x_positions[sender_id])
            self.send_message(player_pos_msg, sender_id)

            if game_can_start:
                # send three countdown messages every 1 second before starting game
                for i in range(3, 0, -1):
                    for player_id in self.x_positions:
                        countdown_msg = message_parsing.encode_message(
                            MSG_TYPES.COUNTDOWN_SRV, player_id, self.calculate_msg_id(), i)
                        self.send_message(countdown_msg, player_id)
                    time.sleep(1)

                # start game
                for player_id in self.x_positions:
                    game_can_start_msg = message_parsing.encode_message(
                        MSG_TYPES.GAME_CAN_START_SRV, player_id, self.calculate_msg_id(), "")
                    self.send_message(game_can_start_msg, player_id)

                self.game_is_on = True
                    
        elif msg_type == MSG_TYPES.PLAYER_UPDATE_USR:
            # print(f"Recieved: {msg_id} from: {sender_id}")
            self.update_player_model(sender_id, msg_id, msg_payload)

        else:
            print("Unknown message type: ", msg_type)

    def on_message(self, ch, method, properties, body):
        """Callback function for when a message is received
        ch: The channel object
        method: The method object
        properties: The properties object
        body: The message body"""
        # print("Server received message: ", body)
        self.handle_message(body)

    def start_consuming(self):
        """Start consuming messages
        This function runs in a thread"""
        print("Server is waiting for messages...")
        self.incoming_channel.start_consuming()

    def get_y_from_x(self, x_pos):
        """Get the y position from the x position"""
        x_val_list = list(self.x_positions.values())
        return list(self.y_positions.values())[x_val_list.index(x_pos)]
    
    def calculate_ball_pos(self):
        """ Calculate new ball position """
        self.ball_pos = (self.ball_pos[0] + self.d_ball[0],
                         self.ball_pos[1] + self.d_ball[1])
        
    def set_random_ball_speed(self):
        """ Randomize the speed of the ball """
        self.d_ball = (BALL_CONFIG.MAX_BALL_SPEED, random.randint(-BALL_CONFIG.MAX_BALL_SPEED, BALL_CONFIG.MAX_BALL_SPEED))
    
    def state_thread_fun(self):
        """State thread"""
        # Get message
        while not self.state_thread_stop_event.is_set():
            while self.game_is_on:
                # Check for collision
                self.calculate_ball_pos()
                ball_state, payload = collision.determine_game_state(self.ball_pos,
                                                            self.get_y_from_x(POS_TYPES.LEFT),
                                                            self.get_y_from_x(POS_TYPES.RIGHT),
                                                            self.d_ball)
                # Check for paddle collision or border collision
                if(ball_state == BALL_STATE.PADDLE_COLLISION or
                   ball_state == BALL_STATE.BORDER_COLLISION):
                    self.d_ball = payload
                    # self.calculate_ball_pos() #not here, since players should see event

                # Increment goals
                if (ball_state == BALL_STATE.LEFT_GOAL):
                    self.left_score += 1
                    if (self.left_score >= self.winning_score):
                        self.winner = POS_TYPES.LEFT
                        self.game_is_on = False
                    self.ball_pos = (0, 0)
                    self.set_random_ball_speed()

                if (ball_state == BALL_STATE.RIGHT_GOAL):
                    self.right_score += 1
                    if (self.right_score >= self.winning_score):
                        self.winner = POS_TYPES.RIGHT
                        self.game_is_on = False
                    self.ball_pos = (0, 0)
                    self.set_random_ball_speed()

                # send game update to both players
                for player_id in self.x_positions:
                    # Construct new message
                    # TODO: Include points(goal)
                    # Get opposite id of the one we send message to
                    ids = list(self.x_positions.keys())
                    op_id = ids[1] if ids[0] == player_id else ids[0]

                    self.mutex.acquire(blocking=False)
                    new_msg_payload = {
                        "ball_pos": self.ball_pos,
                        "my_y_pos": self.y_positions[player_id],
                        "op_y_pos": self.y_positions[op_id],
                        "my_y_pos_msg_id": self.latest_msg_ids[player_id],
                        "op_y_pos_msg_id": self.latest_msg_ids[op_id],
                        "left_score": self.left_score,
                        "right_score": self.right_score,
                        "game_finished": (not self.game_is_on, self.winner)
                    }
                    self.mutex.release()
                    # send message
                    update_msg = message_parsing.encode_message(
                        MSG_TYPES.GAME_UPDATE_SRV, player_id, self.calculate_msg_id(), new_msg_payload)

                    # print(f"Sending: {self.svr_msg_id} to: {player_id}")
                    self.send_message(update_msg, player_id)
           
                # # TODO: Calculate queue length
                # queue_len = self.result.method.message_count
                # self.queue_sizes.append((queue_len, time.time_ns()))
                time.sleep(1/self.refresh_rate)
            
            if (self.winner != ""):
                print("Game finished!")
                # file = open(f"./log_files/queue_size/queue_log.txt", "w")
                # # write content of msg_data
                # for queue_size, timestamp in self.queue_sizes:
                #     file.write(f"{queue_size};{timestamp} \n")
                # file.close() 
                self.y_positions.clear()
                self.x_positions.clear()
                self.left_score = 0
                self.right_score = 0
                self.ball_pos = (0, 0)
                self.winner = ""
