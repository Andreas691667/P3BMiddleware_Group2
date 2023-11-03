import turtle
import sys
sys.path.insert(0, './src/Utility')
from config import POS_TYPES, SCREEN_CONFIG, PADDLE_CONFIG, PLAYER_COLORS
class View():
    """ View class """

    def __init__(self) -> None:
        self.left_pad, self.right_pad = self.create_paddles()
        self.left_sc_board, self.right_sc_board = self.create_scoreboards()
        self.hit_ball = self.create_ball()
        self.sc = self.create_screen()
        self.countdown = self.create_countdown()
        self.player_position = self.create_player_position() # change color later?

    def create_paddles(self):
        """Create the paddle"""
        left = self.create_paddle(PLAYER_COLORS.IDLE_COLOR, SCREEN_CONFIG.LEFT_X)
        right = self.create_paddle(PLAYER_COLORS.IDLE_COLOR, SCREEN_CONFIG.RIGHT_X)

        return left, right
    
    def create_paddle(self, color: str, x_pos: int):
        """Create the paddle"""
        pad = turtle.Turtle()
        pad.speed(0)
        pad.shape("square")
        pad.color(color)
        pad.shapesize(stretch_wid=PADDLE_CONFIG.PADDLE_HEIGHT, stretch_len=PADDLE_CONFIG.PADDLE_WIDTH)
        pad.penup()
        pad.goto(x_pos, 0)
        return pad
    
    
    def create_ball(self):
        """Create the ball"""
        hit_ball = turtle.Turtle()
        hit_ball.speed(0)
        hit_ball.shape("square")
        hit_ball.color("lime")
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
    
    def create_scoreboard(self, color, x):
        """Create the scoreboard"""
        sketch = turtle.Turtle()
        sketch.speed(0)
        sketch.color(color)
        sketch.penup()
        sketch.hideturtle()
        sketch.goto(x, 200)
        sketch.write("0", font=("Courier", 50, "normal"))
        return sketch
    
    def create_scoreboards(self):
        left = self.create_scoreboard(PLAYER_COLORS.IDLE_COLOR, -100)
        right = self.create_scoreboard(PLAYER_COLORS.IDLE_COLOR, 60)
        return left, right
        
    
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
    
    def show_player_position(self, x_pos: str):
        color = ""
        if (x_pos == POS_TYPES.LEFT):
            color = "red"
        else: color = "blue"

        self.player_position.color(color)
        self.player_position.write(f"You are {color}", align="center", font=("Courier", 50, "bold"))
    
    def clear_player_position(self):
        """clears the player position notification"""
        self.player_position.clear()

    def create_player_position(self):
        """Create player position"""
        player_position = turtle.Turtle()
        player_position.speed(0)
        player_position.penup()
        player_position.hideturtle()
        player_position.goto(0, -200)
        return player_position
        
    def show_winner(self, winner: str):
        """Show winner"""
        winning_color = PLAYER_COLORS.LEFT_PLAYER_COLOR if winner == POS_TYPES.LEFT else PLAYER_COLORS.RIGHT_PLAYER_COLOR
        self.countdown.clear()
        self.countdown.color(winning_color)
        self.countdown.write(f"{winning_color} won!",
                     align="center", font=("Courier", 50, "bold"))
        
    def clear_countdown(self):
        """Clear countdown"""
        self.countdown.clear()
    
    def update_score_boards(self, my_x_pos, my_score, op_score):
        """update score boards"""
        self.left_sc_board.clear()
        self.right_sc_board.clear()
        if (my_x_pos == POS_TYPES.RIGHT):
            self.right_sc_board.write(f"{my_score}", font=("Courier", 50, "normal"))
            self.left_sc_board.write(f"{op_score}", font=("Courier", 50, "normal"))
        else:
            self.left_sc_board.write(f"{my_score}", font=("Courier", 50, "normal"))
            self.right_sc_board.write(f"{op_score}", font=("Courier", 50, "normal"))
        self.sc.update()
    
    def update_positions (self, my_x_pos, my_y, op_y, ball_pos):
        """update positions"""
        if (my_x_pos == POS_TYPES.RIGHT):
            self.left_pad.goto(SCREEN_CONFIG.LEFT_X, op_y)
            self.right_pad.goto(SCREEN_CONFIG.RIGHT_X, my_y)
        else:
            self.left_pad.goto(SCREEN_CONFIG.LEFT_X, my_y)
            self.right_pad.goto(SCREEN_CONFIG.RIGHT_X, op_y)

        self.hit_ball.goto(*ball_pos)

   
    def set_player_colors(self):
        """set colors when side is chosen"""
        # Set score board colors 
        self.left_sc_board.color(PLAYER_COLORS.LEFT_PLAYER_COLOR)
        self.right_sc_board.color(PLAYER_COLORS.RIGHT_PLAYER_COLOR)
        self.update_score_boards(POS_TYPES.LEFT, 0, 0)

        # Set paddle colors
        self.left_pad.color(PLAYER_COLORS.LEFT_PLAYER_COLOR)
        self.right_pad.color(PLAYER_COLORS.RIGHT_PLAYER_COLOR)
            


    def update_view(self, my_y: int, op_y: int, ball_pos: (int, int), my_x_pos : str, my_score: int, op_score: int, update_score : bool):
        """Update the view"""
        self.update_positions(my_x_pos, my_y, op_y, ball_pos)
    
        if update_score:
            self.update_score_boards(my_x_pos, my_score, op_score)

        self.sc.update()

    def reset_view(self):
        """Reset the view"""
        self.left_sc_board.clear()
        self.right_sc_board.clear()
        self.left_sc_board.write("0", font=("Courier", 50, "normal"))
        self.right_sc_board.write("0", font=("Courier", 50, "normal"))
        self.left_pad.goto(SCREEN_CONFIG.LEFT_X, 0)
        self.right_pad.goto(SCREEN_CONFIG.RIGHT_X, 0)
        self.hit_ball.goto(0, 0)
        self.show_winner("")
        self.sc.update()