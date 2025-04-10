from turtle import Screen
from paddle import Paddle

screen = Screen()

# Create the paddles
paddle1 = Paddle((350, 0))
paddle2 = Paddle((-350, 0))

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
screen.onkey(paddle1.go_up, "Up")
screen.onkey(paddle1.go_down, "Down")
screen.onkey(paddle2.go_up, "w")
screen.onkey(paddle2.go_down, "s")


# Main game loop
while True:
    screen.update()
    # Check for collisions with the wall
    if paddle1.ycor() > 290:
        paddle1.sety(290)
    elif paddle1.ycor() < -290:
        paddle1.sety(-290)

screen.exitonclick()