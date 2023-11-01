import sys
sys.path.insert(0, './src/Utility')
from threading import Thread, Event
import pika
import message_parsing
from config import RMQ_CONFIG, MSG_TYPES, POS_TYPES
from queue import Queue, Empty
import time

class Server():
    """Class for the leader of the game"""

    def __init__(self) -> None:
        self.configure_server()
        self.game_is_on: bool = False

        # Model variables
        self.x_positions: dict[int, str] = {}  # player_id : int => x_pos : str (LEFT or RIGHT)
        self.y_positions: dict[int, int] = {}  # player_id : int => y_pos : int
        self.ball_pos: (int, int) = (0, 0)
        self.d_ball: (int, int) = (1, 1)
        self.refresh_rate: int = 10

        self.incoming_message_queue = Queue()

        self.consumer_thread = Thread(target=self.start_consuming)
        self.state_thread = Thread(target=self.state_thread_fun)
        
        self.state_thread_stop_event = Event()
        
        self.consumer_thread.start()
        self.state_thread.start()


    def configure_server(self):
        """Configure the server"""
        # The connection object
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RMQ_CONFIG.SERVER_IP, port=RMQ_CONFIG.SERVER_PORT))

        # The channel object
        self.channel = self.connection.channel()

        # Declare the exchanges
        self.channel.exchange_declare(
            exchange=RMQ_CONFIG.SERVER_EXCHANGE, exchange_type='direct')  # for incoming messages
        self.channel.exchange_declare(
            exchange=RMQ_CONFIG.USER_EXCHANGE, exchange_type='fanout')  # for outgoing messages

        # Declare the queue (Name is generated uniquely by RMQ)
        # Incoming message queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.incoming_message_queue = result.method.queue

        # Bind the queue to the exchange
        self.channel.queue_bind(
            exchange=RMQ_CONFIG.USER_EXCHANGE, queue=self.incoming_message_queue)

        # Create a consumer for the incoming message queue
        self.channel.basic_consume(
            queue=self.incoming_message_queue, on_message_callback=self.on_message, auto_ack=True)

    def send_message(self, message, player_id):
        """Send message to the rabbitmq server
        message: The message to send
        This is done by publishing the message to the server updates queue
        The routing key is the player id =(left or right)"""
        self.channel.basic_publish(
            exchange=RMQ_CONFIG.SERVER_EXCHANGE, routing_key=str(player_id), body=message)

    def assign_player_x_position(self, player_id):
        """Assign a player position to the player
        player_id: The id of the player to assign a position to"""
        # first player to join game is always left
        if len(self.x_positions) == 0:
            self.x_positions[player_id] = POS_TYPES.LEFT
        else:
            self.x_positions[player_id] = POS_TYPES.RIGHT

        # if two players have joined, send game can start message to both players
        if len(self.x_positions) == 2:
            self.game_is_on = True
            self.y_positions = {player_id: 0 for player_id in self.x_positions}
            # for player_id in self.x_positions:
            #     game_can_start_msg = message_parsing.encode_message(
            #         MSG_TYPES.GAME_CAN_START_SRV, player_id, "")
            #     self.send_message(game_can_start_msg, player_id)

    def update_player_y_position(self, player_id, new_y_pos):
        """Update the player's position
        player_id: The id of the player to update
        new_pos: The new position of the player
        returns opposite id than sender
        """
        # Update position of player that sent message
        self.y_positions[player_id] = new_y_pos

        # Get opposite id of sender
        ids = list(self.x_positions.keys())
        rec_id = ids[1] if ids[0] == player_id else ids[0]
        return rec_id

    def handle_message(self, msg):
        """Handle the message
        msg: The message to handle in json format"""
        msg_type, sender_id, msg_payload = message_parsing.decode_message(msg)

        if msg_type == MSG_TYPES.NEW_PLAYER_USR:
            self.assign_player_x_position(sender_id)
            # send player position to back to player
            player_pos_msg = message_parsing.encode_message(
                MSG_TYPES.PLAYER_POSITION_INIT_SRV, sender_id, self.x_positions[sender_id])
            self.send_message(player_pos_msg, sender_id)

            if self.game_is_on:
                # send game can start message to both players
                for player_id in self.x_positions:
                    game_can_start_msg = message_parsing.encode_message(
                        MSG_TYPES.GAME_CAN_START_SRV, player_id, "")
                    self.send_message(game_can_start_msg, player_id)
                    
        elif msg_type == MSG_TYPES.PLAYER_UPDATE_USR:
            op_player_id = self.update_player_y_position(sender_id, msg_payload)
            # send game update to other player
        #     player_update_msg = message_parsing.encode_message(
        #         MSG_TYPES.GAME_UPDATE_SRV, op_player_id, msg_payload)
        #     self.send_message(player_update_msg, op_player_id)

        else:
            print("Unknown message type: ", msg_type)

    def on_message(self, ch, method, properties, body):
        """Callback function for when a message is received
        ch: The channel object
        method: The method object
        properties: The properties object
        body: The message body"""
        print("Server received message: ", body)
        self.incoming_message_queue.put(body)
        
        # self.handle_message(body)

    def start_consuming(self):
        """Start consuming messages
        This function runs in a thread"""
        self.channel.start_consuming()
    
    def state_thread_fun(self):
        """State thread"""
        # Get message
        while not self.state_thread_stop_event.is_set():
            # Check queue for incoming messages
            try:
                msg = self.incoming_message_queue.get(timeout=1)
                              
            except Empty:
                pass
                
            else:
                self.handle_message(msg)

            if self.game_is_on:
                # Calculate new ball position
                new_x = self.ball_pos[0] + self.d_ball[0]
                new_y = self.ball_pos[1] + self.d_ball[1]
                self.ball_pos = (new_x, new_y)

                # send game update to both players
                for player_id in self.x_positions:
                    # Construct new message
                    new_msg_payload = {
                        "ball_pos": self.ball_pos,
                        "player_dt": self.y_positions[player_id] 
                    }

                    # Get opposite id of sender
                    ids = list(self.x_positions.keys())
                    op_id = ids[1] if ids[0] == player_id else ids[0]
                    # send message
                    update_msg = message_parsing.encode_message(
                        MSG_TYPES.GAME_UPDATE_SRV, op_id, new_msg_payload)
                    
                    self.send_message(update_msg, player_id)
                    time.sleep(1/self.refresh_rate)
