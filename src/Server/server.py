from threading import Thread
import pika
import Utility.message_parsing as message_parsing
from Utility.config import RMQ_CONFIG, MSG_TYPES


class Server():
    """Class for the leader of the game"""

    def __init__(self) -> None:
        self.configure_server()
        self.game_is_on: bool = False
        self.players: dict[int, str] = {}  # player_id -> player_position
        self.consumer_thread = Thread(target=self.start_consuming)
        self.consumer_thread.start()

    def configure_server(self):
        """Configure the server"""
        # The connection object
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RMQ_CONFIG["SERVER_IP"], port=RMQ_CONFIG["SERVER_PORT"]))

        # The channel object
        self.channel = self.connection.channel()

        # Declare the exchanges
        self.channel.exchange_declare(
            exchange=RMQ_CONFIG["SERVER_EXCHANGE"], exchange_type='direct')  # for incoming messages
        self.channel.exchange_declare(
            exchange=RMQ_CONFIG["USER_EXCHANGE"], exchange_type='fanout')  # for outgoing messages

        # Declare the queue (Name is generated uniquely by RMQ)
        # Incoming message queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.incoming_message_queue = result.method.queue

        # Bind the queue to the exchange
        self.channel.queue_bind(
            exchange=RMQ_CONFIG["USER_EXCHANGE"], queue=self.incoming_message_queue)

        # Create a consumer for the incoming message queue
        self.channel.basic_consume(
            queue=self.incoming_message_queue, on_message_callback=self.on_message, auto_ack=True)

    def send_message(self, message, player_id):
        """Send message to the rabbitmq server
        message: The message to send
        This is done by publishing the message to the server updates queue
        The routing key is the player id =(left or right)"""
        self.channel.basic_publish(
            exchange=RMQ_CONFIG["SERVER_EXCHANGE"], routing_key=player_id, body=message)

    def handle_message(self, msg):
        """Handle the message
        msg: The message to handle in json format"""
        msg_type, sender_id, msg_payload = message_parsing.decode_message(msg)

        if msg_type == MSG_TYPES["NEW_PLAYER"]:
            # TODO: If there are no players assign position right, else assign the other position left
            pass
        elif msg_type == MSG_TYPES["PLAYER_UPDATE"]:
            pass
        else:
            print("Unknown message type: ", msg_type)

    def on_message(self, ch, method, properties, body):
        """Callback function for when a message is received
        ch: The channel object
        method: The method object
        properties: The properties object
        body: The message body"""
        print("Received message: ", body)
        self.handle_message(body)

    def start_consuming(self):
        """Start consuming messages
        This function runs in a thread"""
        self.channel.start_consuming()
