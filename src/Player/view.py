import turtle
import sys
sys.path.insert(0, './src/Utility')
from config import POS_TYPES, SCREEN_CONFIG, PADDLE_CONFIG
class View():
    """ View class """

    def __init__(self) -> None:
        self.my_pad, self.op_pad = self.create_paddles()
        self.hit_ball = self.create_ball()
        self.sc = self.create_screen()
        self.sc_board = self.create_scoreboard()


    def create_paddles(self):
        """Create the paddle"""
        my_pad = turtle.Turtle()
        my_pad.speed(0)
        my_pad.shape("square")
        my_pad.color("black")
        my_pad.shapesize(stretch_wid=PADDLE_CONFIG.PADDLE_HEIGHT, stretch_len=PADDLE_CONFIG.PADDLE_WIDTH)
        my_pad.penup()
        my_pad.goto(SCREEN_CONFIG.LEFT_X, 0)

        op_pad = turtle.Turtle()
        op_pad.speed(0)
        op_pad.shape("square")
        op_pad.color("black")
        op_pad.shapesize(stretch_wid=PADDLE_CONFIG.PADDLE_HEIGHT, stretch_len=PADDLE_CONFIG.PADDLE_WIDTH)
        op_pad.penup()
        op_pad.goto(SCREEN_CONFIG.RIGHT_X, 0)

        return my_pad, op_pad
    
    def create_ball(self):
        """Create the ball"""
        hit_ball = turtle.Turtle()
        hit_ball.speed(40)
        hit_ball.shape("circle")
        hit_ball.color("blue")
        hit_ball.penup()
        hit_ball.goto(0, 0)
        hit_ball.dx = 5
        hit_ball.dy = -5
        return hit_ball

    def create_screen(self):
        """Create the screen"""
        sc = turtle.Screen()
        sc.title("Pong game")
        sc.bgcolor("white")
        sc.setup(width=SCREEN_CONFIG.SCREEN_WIDTH, height=SCREEN_CONFIG.SCREEN_HEIGHT)
        return sc
    
    def create_scoreboard(self):
        """Create the scoreboard"""
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("blue")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 260)
        sketch.write("My score : 0 Opponent's score: 0",
                     align="center", font=("Courier", 24, "normal"))
        return sketch
    
    def update_view(self, my_y: int, op_y: int, ball_pos: (int, int), my_x_pos : str, my_score: int, op_score: int, update_score : bool):
        """Update the view"""
        if (my_x_pos == POS_TYPES.RIGHT):
            self.my_pad.goto(SCREEN_CONFIG.RIGHT_X, my_y)
            self.op_pad.goto(SCREEN_CONFIG.LEFT_X, op_y)
        else:
            self.my_pad.goto(SCREEN_CONFIG.LEFT_X, my_y)
            self.op_pad.goto(SCREEN_CONFIG.RIGHT_X, op_y)
        self.hit_ball.goto(*ball_pos)
    
        if update_score:
            self.sc_board.clear()
            self.sc_board.write(f"My score : {my_score} Opponent's score: {op_score}",
                         align="center", font=("Courier", 24, "normal"))

        self.sc.update()