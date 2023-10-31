import pika
from config import SERVER_IP, SERVER_PORT


class Client():
    """Class for the client of the game
    The client is responsible for sending the player's input to the leader using RMQ (pika)"""

    def __init__(self) -> None:
        # The connection object
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=SERVER_IP, port=SERVER_PORT))

        # The channel object
        self.channel = self.connection.channel()

        # Declare the exchange
        self.channel.exchange_declare(exchange='', exchange_type='fanout')
