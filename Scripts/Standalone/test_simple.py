import turtle

# Can you guess what each line does?
window = turtle.Screen()
window.title("Pong Game by Me!")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Let's make the left paddle!
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B (Right)
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0) # The X is positive!

def paddle_a_up():
    y = paddle_a.ycor()
    y += 10
    paddle_a.sety(y)

# Tell the window to listen
window.listen()

# When "w" is pressed, call our function
window.onkeypress(paddle_a_up, "w")

# Functions for paddle A
def paddle_a_down():
    y = paddle_a.ycor()
    y -= 10
    paddle_a.sety(y)

# Functions for paddle B
def paddle_b_up():
    y = paddle_b.ycor()
    y += 10
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 10
    paddle_b.sety(y)

# Keyboard bindings
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

# Create the ball (like a paddle)
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.dx = 0.06
ball.dy = 0.06

# Initialize scores
score_a = 0
score_b = 0

# Setup the score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

while True:
    window.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Inside the while True loop...

    # Top wall bounce
    if ball.ycor() > 290:
        ball.sety(290) # Prevents getting stuck
        ball.dy *= -1  # Reverse the y-direction

    # Bottom wall bounce
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
    
    # Right paddle bounce
    if (ball.xcor() > 340 and ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.dx *= -1

    # Left paddle bounce
    if (ball.xcor() < -340 and ball.xcor() > -350) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.dx *= -1
    
    # When ball goes off-screen (right side - Player A scores)
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

    # When ball goes off-screen (left side - Player B scores)
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", \
                  align="center", font=("Courier", 24, "normal"))