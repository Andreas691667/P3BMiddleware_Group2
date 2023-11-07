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
        self.my_latest_msg_id: int = -1
        self.op_latest_msg_id: int = -1
        self.ball_pos: (int, int) = (0, 0)
        self.my_score: int = 0
        self.op_score: int = 0


    def set_my_latest_msg_id (self, msg_id: int) -> None:
        """Set my latest msg id"""
        self.my_latest_msg_id = msg_id
    
    
    def set_op_latest_msg_id (self, msg_id: int) -> None:
        """Set opponent latest msg id"""
        self.op_latest_msg_id = msg_id
    
    def get_my_latest_msg_id (self) -> int:
        """Get my latest msg id"""
        return self.my_latest_msg_id
    
    def get_op_latest_msg_id (self) -> int:
        """Get opponent latest msg id"""
        return self.op_latest_msg_id

    def paddle_collision(self, paddle_y_pos: int) -> bool:
        """Returns True if there is a collision with the paddle, False otherwise"""
        return paddle_y_pos > SCREEN_CONFIG.SCREEN_HEIGHT/2-6 or paddle_y_pos < -SCREEN_CONFIG.SCREEN_HEIGHT/2+6

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
        if not self.paddle_collision(y_pos):
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
    
    def set_my_score(self, score: int) -> None:
        """doc"""
        self.my_score = score
    
    def get_my_score(self) -> int:
        """d"""
        return self.my_score
    
    def set_op_score(self, score: int) -> None:
        """d"""
        self.op_score = score
    
    def get_op_score(self) -> int:
        """d"""
        return self.op_score

#endregion