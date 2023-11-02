import sys
sys.path.insert(0, './src/Utility')
from config import SCREEN_CONFIG

class Model():
    """Model class, include positions"""

    def __init__(self) -> None:
        self.my_y_pos: int = 0
        self.op_y_pos: int = 0
        self.my_x_pos: str = ""
        self.op_x_pos: str = ""
        self.ball_pos: (int, int) = (0, 0)


    def paddle_collision(self, paddle_y_pos: int) -> bool:
        """Returns True if there is a collision with the paddle, False otherwise"""
        return paddle_y_pos > SCREEN_CONFIG.SCREEN_HEIGHT/2-6 or paddle_y_pos < -SCREEN_CONFIG.SCREEN_HEIGHT/2+6

    def increment_my_pos(self, dt: int) -> None:
        """d"""
        if not self.paddle_collision(self.my_y_pos + dt):
            self.my_y_pos = self.my_y_pos + dt

    def set_op_y_pos(self, new_y_pos: int) -> None:
        """d"""
        if not self.paddle_collision(new_y_pos):
            self.op_y_pos = new_y_pos

    def set_ball_pos(self, pos) -> None:
        """d"""
        self.ball_pos = pos

    def get_my_y_pos(self):
        """d"""
        return self.my_y_pos
    
    def set_my_y_pos(self, y_pos: int) -> None:
        """d"""
        self.my_y_pos = y_pos

    def get_op_y_pos(self):
        """d"""
        return self.op_y_pos

    def get_ball_pos(self):
        """d"""
        return self.ball_pos

    # region X positions
    def set_my_x_pos(self, x_pos: str):
        """doc"""
        self.my_x_pos = x_pos

    def set_op_x_pos(self, x_pos: str):
        """doc"""
        self.op_x_pos = x_pos

    def get_my_x_pos(self) -> str:
        """doc"""
        return self.my_x_pos
    
    def get_op_x_pos(self) -> str:
        """doc"""
        return self.op_x_pos
    # endregion
