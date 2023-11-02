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
        self.my_sc_board = self.create_scoreboard(POS_TYPES.LEFT)
        self.op_sc_board = self.create_scoreboard(POS_TYPES.RIGHT)
        self.countdown = self.create_countdown()


    def create_paddles(self):
        """Create the paddle"""
        my_pad = turtle.Turtle()
        my_pad.speed(0)
        my_pad.shape("square")
        my_pad.color("red")
        my_pad.shapesize(stretch_wid=PADDLE_CONFIG.PADDLE_HEIGHT, stretch_len=PADDLE_CONFIG.PADDLE_WIDTH)
        my_pad.penup()
        my_pad.goto(SCREEN_CONFIG.LEFT_X, 0)

        op_pad = turtle.Turtle()
        op_pad.speed(0)
        op_pad.shape("square")
        op_pad.color("blue")
        op_pad.shapesize(stretch_wid=PADDLE_CONFIG.PADDLE_HEIGHT, stretch_len=PADDLE_CONFIG.PADDLE_WIDTH)
        op_pad.penup()
        op_pad.goto(SCREEN_CONFIG.RIGHT_X, 0)

        return my_pad, op_pad
    
    def create_ball(self):
        """Create the ball"""
        hit_ball = turtle.Turtle()
        hit_ball.speed(0)
        hit_ball.shape("circle")
        hit_ball.color("medium spring green")
        hit_ball.penup()
        hit_ball.goto(0, 0)
        hit_ball.dx = 5
        hit_ball.dy = -5
        return hit_ball

    def create_screen(self):
        """Create the screen"""
        sc = turtle.Screen()
        sc.title("Pong game")
        sc.bgcolor("black")
        sc.setup(width=SCREEN_CONFIG.SCREEN_WIDTH, height=SCREEN_CONFIG.SCREEN_HEIGHT)

        t = turtle.Turtle()
        t.penup()
        t.goto(0, -SCREEN_CONFIG.SCREEN_HEIGHT // 2)
        t.pendown()

        # Draw a dashed vertical line
        t.setheading(90)
        t.setundobuffer(0)
        for i in range(SCREEN_CONFIG.SCREEN_HEIGHT // 20):
            if i % 2 == 0:
                t.pencolor("white")
            else:
                t.pencolor("black")
            t.forward(20)
        
        return sc
    
    def create_scoreboard(self, player):
        """Create the scoreboard"""
        color = ""
        x = 0
        font_size = 50
        
        if (player == POS_TYPES.LEFT):
            color = "red"
            x = -font_size*2
        else:
            color = "blue"
            x = font_size

        
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color(color)
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(x, 200)
        sketch.write("0", font=("Courier", font_size, "normal"))
        return sketch
    
    def create_countdown(self):
        """Create the countdown"""
        countdown = turtle.Turtle()
        countdown.speed(0)
        countdown.color("red")
        countdown.penup()
        countdown.hideturtle()
        countdown.goto(0, 0)
        countdown.write("Waiting for game to start...",
                        align="center", font=("Courier", 30, "normal"))
        return countdown
    
    def show_countdown(self, countdown: int):
        """Show countdown value"""
        self.countdown.clear()
        if countdown == 1:
            self.countdown.color("green")
        if countdown == 2:
            self.countdown.color("yellow")
        if countdown == 3:
            self.countdown.color("red")
        self.countdown.write(f"{countdown}",
                     align="center", font=("Courier", 200, "bold"))
        
    def show_winner(self, winner: str):
        """Show winner"""
        self.countdown.clear()
        self.countdown.color("green")
        self.countdown.write(f"{winner} player won!",
                     align="center", font=("Courier", 50, "bold"))
        
    def clear_countdown(self):
        """Clear countdown"""
        self.countdown.clear()

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
            self.my_sc_board.clear()
            self.op_sc_board.clear()
            if (my_x_pos == POS_TYPES.RIGHT):
                self.my_sc_board.write(f"{my_score}", font=("Courier", 50, "normal"))
                self.op_sc_board.write(f"{op_score}", font=("Courier", 50, "normal"))
            else:
                self.my_sc_board.write(f"{op_score}", font=("Courier", 50, "normal"))
                self.op_sc_board.write(f"{my_score}", font=("Courier", 50, "normal"))

        self.sc.update()

    def reset_view(self):
        """Reset the view"""
        self.my_sc_board.clear()
        self.op_sc_board.clear()
        self.my_sc_board.write("0", font=("Courier", 50, "normal"))
        self.op_sc_board.write("0", font=("Courier", 50, "normal"))
        self.my_pad.goto(SCREEN_CONFIG.LEFT_X, 0)
        self.op_pad.goto(SCREEN_CONFIG.RIGHT_X, 0)
        self.hit_ball.goto(0, 0)
        self.show_winner("")
        self.sc.update()