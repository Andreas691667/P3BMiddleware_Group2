import turtle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
LEFT_X = -400
RIGHT_X = 400

class View():
    """ PlayerModel class """

    def __init__(self) -> None:
        self.left_pad, self.right_pad = self.create_paddles()
        self.hit_ball = self.create_ball()
        self.sc = self.create_screen()
        self.sc_board = self.create_scoreboard()
        self.my_pos = 0 # My position
        self.op_pos = 0 # Opponents position

    def create_paddles(self):
        """Create the paddle"""
        l_pad = turtle.Turtle()
        l_pad.speed(0)
        l_pad.shape("square")
        l_pad.color("black")
        l_pad.shapesize(stretch_wid=6, stretch_len=0.7)
        l_pad.penup()
        l_pad.goto(LEFT_X, 0)

        r_pad = turtle.Turtle()
        r_pad.speed(0)
        r_pad.shape("square")
        r_pad.color("black")
        r_pad.shapesize(stretch_wid=6, stretch_len=0.7)
        r_pad.penup()
        r_pad.goto(RIGHT_X, 0)

        return l_pad, r_pad

    
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
        sc.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        return sc
    
    def create_scoreboard(self):
        """Create the scoreboard"""
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color("blue")
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(0, 260)
        sketch.write("Left_player : 0 Right_player: 0",
                     align="center", font=("Courier", 24, "normal"))
        return sketch
    
    def update_view(self, l_pos: int, r_pos: int, ball_pos: (int, int)):
        """Update the view"""
        self.left_pad.goto(LEFT_X, l_pos)
        self.right_pad.goto(RIGHT_X, r_pos)
        self.hit_ball.goto(*ball_pos)
        self.sc.update()