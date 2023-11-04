import sys
sys.path.insert(0, './src/Utility')

import pika
import threading
from config import RMQ_CONFIG, MSG_TYPES


# based on https://www.rabbitmq.com/tutorials/tutorial-three-python.html
class Client():
    """Class for the client of the game
    The client is responsible for sending the player's input to the leader using RMQ (pika)"""

    def __init__(self, on_message_clb, player_id) -> None:

        self.outgoing_channel = self.create_channel()
        self.incoming_channel = self.create_channel()

        self.configure_incoming_channel(on_message_clb, player_id)
        self.configure_outgoing_channel()

        # self.configure_client(on_message_clb, player_id)
        self.consumer_thread = threading.Thread(target=self.start_consuming)
        self.consumer_thread.start()

    def create_channel(self):
        """Create and return a channel object"""
        # The connection object
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RMQ_CONFIG.SERVER_IP, port=RMQ_CONFIG.SERVER_PORT))
        # The channel object
        channel = connection.channel()

        return channel
    
    def configure_incoming_channel(self, on_message_clb, player_id):
        """Configure the consumer channel"""
        self.incoming_channel.exchange_declare(
            exchange=RMQ_CONFIG.SERVER_EXCHANGE, exchange_type='direct')  # for incoming messages
        
        # Declare the queue (Name is generated uniquely by RMQ)
        # Incoming message queue
        args = {"x-max-length": 1}
        result = self.incoming_channel.queue_declare(queue='', exclusive=True, arguments=args)
        self.incoming_message_queue = result.method.queue

        # Bind the queue to the exchange
        self.incoming_channel.queue_bind(
            exchange=RMQ_CONFIG.SERVER_EXCHANGE, queue=self.incoming_message_queue, routing_key=str(player_id))

        # Create a consumer for the incoming message queue
        self.incoming_channel.basic_consume(
            queue=self.incoming_message_queue, on_message_callback=on_message_clb, auto_ack=True)

    def configure_outgoing_channel(self):
        """Configure the publisher channel"""
        self.outgoing_channel.exchange_declare(
            exchange=RMQ_CONFIG.USER_EXCHANGE, exchange_type='fanout')

    def start_consuming(self):
        """Start consuming messages
        This function runs in a thread"""
        self.incoming_channel.start_consuming()

    def send_message(self, message):
        """Send message to the rabbitmq server
        message: The message to send
        This is done by publishing the message to the outgoing message queue"""
        self.outgoing_channel.basic_publish(
            exchange=RMQ_CONFIG.USER_EXCHANGE, routing_key='', body=message)
