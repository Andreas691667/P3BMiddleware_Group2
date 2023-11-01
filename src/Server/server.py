import sys
sys.path.insert(0, './src/Utility')
from threading import Thread
import pika
import message_parsing
from config import RMQ_CONFIG, MSG_TYPES, POS_TYPES


class Server():
    """Class for the leader of the game"""

    def __init__(self) -> None:
        self.configure_server()
        self.game_is_on: bool = False
        self.x_positions: dict[int, str] = {}  # player_id : int => x_pos : str (LEFT or RIGHT)
        self.y_positions: dict[int, int] = {}  # player_id : int => y_pos : int

        self.consumer_thread = Thread(target=self.start_consuming)
        self.consumer_thread.start()

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
            return True
            # for player_id in self.x_positions:
            #     game_can_start_msg = message_parsing.encode_message(
            #         MSG_TYPES.GAME_CAN_START_SRV, player_id, "")
            #     self.send_message(game_can_start_msg, player_id)
        else:
            return False

    def update_player_y_position(self, player_id, new_y_pos):
        """Update the player's position
        player_id: The id of the player to update
        new_pos: The new position of the player
        returns opposite id than sender
        """
        # Update position
        self.y_positions[player_id] = new_y_pos

        # Get opposite id
        ids = list(self.x_positions.keys())
        
        rec_id = ids[1] if ids[0] == player_id else ids[0]
        return rec_id

    def handle_message(self, msg):
        """Handle the message
        msg: The message to handle in json format"""
        msg_type, sender_id, msg_payload = message_parsing.decode_message(msg)

        if msg_type == MSG_TYPES.NEW_PLAYER_USR:
            game_can_start = self.assign_player_x_position(sender_id)
            # send player position to back to player
            player_pos_msg = message_parsing.encode_message(
                MSG_TYPES.PLAYER_POSITION_INIT_SRV, sender_id, self.x_positions[sender_id])
            self.send_message(player_pos_msg, sender_id)

            if game_can_start:
                # send game can start message to both players
                for player_id in self.x_positions:
                    game_can_start_msg = message_parsing.encode_message(
                        MSG_TYPES.GAME_CAN_START_SRV, player_id, "")
                    self.send_message(game_can_start_msg, player_id)

        elif msg_type == MSG_TYPES.PLAYER_UPDATE_USR:
            op_player_id = self.update_player_y_position(sender_id, msg_payload)
            # send game update to other player
            player_update_msg = message_parsing.encode_message(
                MSG_TYPES.GAME_UPDATE_SRV, op_player_id, msg_payload)
            self.send_message(player_update_msg, op_player_id)

        else:
            print("Unknown message type: ", msg_type)

    def on_message(self, ch, method, properties, body):
        """Callback function for when a message is received
        ch: The channel object
        method: The method object
        properties: The properties object
        body: The message body"""
        print("Server received message: ", body)
        self.handle_message(body)

    def start_consuming(self):
        """Start consuming messages
        This function runs in a thread"""
        self.channel.start_consuming()
