import pika
import threading
from src.config import SERVER_IP, SERVER_PORT, SERVER_EXCHANGE, USER_EXCHANGE


# based on https://www.rabbitmq.com/tutorials/tutorial-three-python.html
class Client():
    """Class for the client of the game
    The client is responsible for sending the player's input to the leader using RMQ (pika)"""

    def __init__(self, on_message_clb, player_id) -> None:
        self.configure_client(on_message_clb, player_id)
        self.consumer_thread = threading.Thread(target=self.start_consuming)
        self.consumer_thread.start()

    def configure_client(self, on_message_clb, player_id):
        """Configure the client"""
        # The connection object
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=SERVER_IP, port=SERVER_PORT))

        # The channel object
        self.channel = self.connection.channel()

        # Declare the exchanges
        self.channel.exchange_declare(
            exchange=SERVER_EXCHANGE, exchange_type='direct')  # for incoming messages

        self.channel.exchange_declare(
            exchange=USER_EXCHANGE, exchange_type='fanout')  # for outgoing messages

        # Declare the queue (Name is generated uniquely by RMQ)
        # Incoming message queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.incoming_message_queue = result.method.queue

        # Bind the queue to the exchange
        self.channel.queue_bind(
            exchange=SERVER_EXCHANGE, queue=self.incoming_message_queue, routing_key=player_id)

        # Create a consumer for the incoming message queue
        self.channel.basic_consume(
            queue=self.incoming_message_queue, on_message_callback=on_message_clb, auto_ack=True)

    def start_consuming(self):
        """Start consuming messages
        This function runs in a thread"""
        self.channel.start_consuming()

    def send_message(self, message):
        """Send message to the rabbitmq server
        message: The message to send
        This is done by publishing the message to the outgoing message queue"""
        self.channel.basic_publish(
            exchange=USER_EXCHANGE, routing_key='', body=message)
