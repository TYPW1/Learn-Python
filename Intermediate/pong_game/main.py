import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

# Create the screen
screen = Screen()

# Create the paddles
paddle1 = Paddle((350, 0))
paddle2 = Paddle((-350, 0))

#create the ball
ball = Ball()

# Create the scoreboard
scoreboard = Scoreboard()

# Set the speed of the paddles
paddle1.speed(0)
paddle2.speed(0)

# Set up the screen
screen.title("Pong")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)  # Turns off the screen updates for better performance

# Listen for key presses
screen.listen()

# Bind the paddle movement to the key presses
screen.onkeypress(paddle1.go_up, "Up")
screen.onkeypress(paddle1.go_down, "Down")
screen.onkeypress(paddle2.go_up, "w")
screen.onkeypress(paddle2.go_down, "s")

game_is_on = True
# Main game loop
while game_is_on:
    time.sleep(ball.move_speed)  # Add a small delay to control the speed of the game
    screen.update()

    # Move the ball
    ball.move()

    # Check for collisions with the wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Check for collisions with the paddles
    if ball.distance(paddle1) < 50 and ball.xcor() > 320 or ball.distance(paddle2) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    # Check for ball out of bounds
    if ball.xcor() > 380:
        ball.goto(0, 0)
        ball.bounce_x()
        scoreboard.player1_score()


    if ball.xcor() < -380:
        ball.goto(0, 0)
        ball.bounce_x()
        scoreboard.player2_score()
screen.exitonclick()