# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_vel = [0, 0]
paddle1_pos = [0, (HEIGHT / 2) - HALF_PAD_HEIGHT]
paddle2_pos = [WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT]
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == LEFT:
        ball_vel = [-3, -3]
    else:
        ball_vel = [3, -3]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = [0, (HEIGHT / 2) - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH, (HEIGHT / 2) - HALF_PAD_HEIGHT]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(random.choice([RIGHT, LEFT]))

def ball_direction():
    return random.randrange(0,2)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[0] <= BALL_RADIUS:
        ball_vel[0] = - ball_vel[0]
    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS:
        ball_vel[0] = - ball_vel[0]
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
                         
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel    
    paddle2_pos[1] += paddle2_vel
   
    if paddle1_pos[1] <= 0:
        paddle1_pos[1] = 0
    elif paddle1_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    elif paddle2_pos[1] <= 0:
        paddle2_pos[1] = 0
    elif paddle2_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
        
    # draw paddles
    canvas.draw_polygon([(paddle1_pos),
                         (PAD_WIDTH, paddle1_pos[1]),
                         (PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT),
                         (paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT)],
                         1, "Yellow", "Yellow")
    
    canvas.draw_polygon([(paddle2_pos),
                         (WIDTH - PAD_WIDTH, paddle2_pos[1]),
                         (WIDTH - PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT),
                         (paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT)],
                         1, "Yellow", "Yellow")

    # determines whether ball intersects gutter and whether paddle and ball collide
    acc = 1.1
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * acc
            ball_vel[1] = + ball_vel[1] * acc
        else:
            score2 += 1
            spawn_ball(random.choice([RIGHT, LEFT]))
    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * acc
            ball_vel[1] = + ball_vel[1] * acc
        else:
            score1 += 1
            spawn_ball(random.choice([RIGHT, LEFT]))

    if score1 == 5 or score2 == 5:
        game_over(canvas, score1 > score2)
    # draw scores
    canvas.draw_text("P|1" , [100, 100], 72, "White")
    canvas.draw_text(str(score1), [125, 300], 72, "White")
    canvas.draw_text("P|2", [400, 100], 72, "White")
    canvas.draw_text(str(score2), [425, 300], 72, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 2
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle2_vel + vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle2_vel + vel
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += vel
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
def restart_game():
    new_game()
    
def game_over(canvas,score):
    if score == True:
        canvas.draw_text("P|1 Wins!", [100, 300], 100, "White")
    else:
        canvas.draw_text("P|2 Wins!", [100, 300], 100, "White")
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart_button = frame.add_button("Restart", restart_game, 75)


# start frame
new_game()
frame.start()
