import turtle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class PlayerModel():
    """ PlayerModel class """

    def __init__(self) -> None:
        self.left_pad, self.right_pad = self.create_paddles()
        self.hit_ball = self.create_ball()
        self.sc = self.create_screen()

    def create_paddles(self):
        """Create the paddle"""
        l_pad = turtle.Turtle()
        l_pad.speed(0)
        l_pad.shape("square")
        l_pad.color("black")
        l_pad.shapesize(stretch_wid=6, stretch_len=2)
        l_pad.penup()
        l_pad.goto(-400, 0)

        r_pad = turtle.Turtle()
        r_pad.speed(0)
        r_pad.shape("square")
        r_pad.color("black")
        r_pad.shapesize(stretch_wid=6, stretch_len=2)
        r_pad.penup()
        r_pad.goto(400, 0)

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
    