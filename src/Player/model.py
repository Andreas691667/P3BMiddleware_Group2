class Model():
    """Model class, include positions"""

    def __init__(self) -> None:
        self.my_pos: int = 0
        self.op_pos: int = 0
        self.ball_pos: (int, int) = (0, 0)

    # TODO: Don't know if they should be incremented or set?
    def increment_my_pos(self, dt: int) -> None:
        """d"""
        self.my_pos = self.my_pos + dt
    
    def increment_op_pos(self, dt: int) -> None:
        """d"""
        self.my_pos = self.my_pos + dt

    def set_ball_pos(self, pos) -> None:
        """d"""
        self.ball_pos = pos
    
    def get_my_pos (self):
        """d"""
        return self.my_pos
    
    def get_op_pos (self):
        """d"""
        return self.op_pos
    
    def get_ball_pos (self):
        """d"""
        return self.op_pos
    
