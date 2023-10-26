import pika
from dataclass import dataclass

# TODO: Define publish subscribe topics here

# Publish topics


# Subscribe topics

class Leader():
    """Class for the leader of the game"""
    
    @dataclass
    class State():
        """Dataclass for the state vector"""
        position: list[int] = [-1, -1]    # positions of the players
        score: list[int] = [-1, -1]       # scores of the players
        ball_position: tuple[int, int] = (-1, -1)  # position of ball
        game_active: bool = False
        winner: int = -1                  # winner of the game

    def __init__(self) -> None:
        self.state_vector = self.State()
        
        # TODO: Setup connection attributes
        # self.connection = 

    def main_loop(self):
        """"Listens for events on subscriber topics and passes control to """
        # Case 1: Player 1 have moved
        
        # Case 2: Player 2 have moved

        # Update ball position
        
        # Evaluate state: have a player scored, won ect?
        
        pass

    def connect(self):
        """Connect to the rabbitmq server"""
        pass
    
    def disconnect(self):
        """Disconnect from the rabbitmq server"""
        pass
    
    def send_message(self):
        """Send message to the rabbitmq server"""
        # TODO: Publish the state vector to the rabbitmq server on the publish topic
        pass
    
    def update_state_vector(self):
        """"Update local state vector"""
        pass