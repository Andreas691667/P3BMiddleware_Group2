# import turtle

from PlayerModel import PlayerModel

class PlayerView():
    """View for the player based on model"""

    def __init__(self) -> None:
        self.model = PlayerModel()

