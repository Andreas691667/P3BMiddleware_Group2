import sys
sys.path.insert(0, './src/Utility')
from config import SCREEN_CONFIG, BALL_STATE, PADDLE_CONFIG


def determine_game_state(ball_pos: (int, int), left_pos: int, right_pos: int, d_ball: (int, int)) -> str:
    """Determine state of the game using all available information"""

    # Paddle collisions
    if (paddle_collision(ball_pos, left_pos, right_pos) == BALL_STATE.PADDLE_COLLISION):
        dx = d_ball[0]
        dy = d_ball[1]
        return (BALL_STATE.PADDLE_COLLISION, (dx*-1, dy))
    
    # Border collisions
    elif (border_collision(ball_pos) == BALL_STATE.BORDER_COLLISION):
        dx = d_ball[0]
        dy = d_ball[1]
        return (BALL_STATE.BORDER_COLLISION, (dx, dy*-1))
    
     # Goals
    elif (goal(ball_pos) == BALL_STATE.LEFT_GOAL):
        return (BALL_STATE.LEFT_GOAL, (0,0))

    elif (goal(ball_pos) == BALL_STATE.RIGHT_GOAL):
        return (BALL_STATE.RIGHT_GOAL, (0, 0))
    
    # No collision
    else:
        return (BALL_STATE.NO_COLLISION, (0, 0))



def paddle_collision(ball_pos: (int, int), left_pos: int, right_pos: int) -> BALL_STATE:
    """Determine if the ball has collided with a paddle"""
    ball_x = ball_pos[0]
    ball_y = ball_pos[1]
    a = 40
    if (ball_x <= SCREEN_CONFIG.LEFT_X + PADDLE_CONFIG.PADDLE_WIDTH/2 + 3
        and ball_x >= SCREEN_CONFIG.LEFT_X - PADDLE_CONFIG.PADDLE_WIDTH/2 - 3):
        if (ball_y >= left_pos - PADDLE_CONFIG.PADDLE_HEIGHT/2 - a
            and ball_y <= left_pos + PADDLE_CONFIG.PADDLE_HEIGHT/2 + a):
            return BALL_STATE.PADDLE_COLLISION
    elif (ball_x >= SCREEN_CONFIG.RIGHT_X - PADDLE_CONFIG.PADDLE_WIDTH/2 - 3
          and ball_x <= SCREEN_CONFIG.RIGHT_X + PADDLE_CONFIG.PADDLE_WIDTH/2 + 3):
        if (ball_y >= right_pos - PADDLE_CONFIG.PADDLE_HEIGHT/2 - a 
            and ball_y <= right_pos + PADDLE_CONFIG.PADDLE_HEIGHT/2 + a):
            return BALL_STATE.PADDLE_COLLISION
    else:
        return None


def goal(ball_pos: (int, int)) -> BALL_STATE:
    """Determine if a goal has been scored"""
    ball_x = ball_pos[0]
    if ball_x < -SCREEN_CONFIG.SCREEN_WIDTH/2:
        return BALL_STATE.RIGHT_GOAL
    elif ball_x > SCREEN_CONFIG.SCREEN_WIDTH/2:
        return BALL_STATE.LEFT_GOAL
    else:
        return None


def border_collision(ball_pos: (int, int)) -> BALL_STATE:
    """Determines if the ball has collided with the top or bottom border"""
    ball_y = ball_pos[1]
    if ball_y > SCREEN_CONFIG.SCREEN_HEIGHT/2 or ball_y < -SCREEN_CONFIG.SCREEN_HEIGHT/2:
        return BALL_STATE.BORDER_COLLISION
    else:
        return None
