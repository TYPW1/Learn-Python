import random
from turtle import Turtle, Screen

screen = Screen()
screen.setup(500, 400)
user_bet = screen.textinput("Make your bet", "Which turtle will win the race")
turtles ={
    "tam":"red",
    "tem": "orange",
    "tim": "yellow",
    "tom": "green",
    "tum": "blue",
    "tym": "indigo",
    "tbm": "violet"
}

start_y = [-150, -100, -50, 0, 50, 100, 150]  # Y positions for 7 turtles
start_x = -230  # All turtles start at left edge
is_race_on = False

race_turtles = []
for (name, color), y_pos in zip(turtles.items(), start_y):
    turtle = Turtle(shape="turtle")
    turtle.color(color)
    turtle.penup()
    turtle.goto(start_x, y_pos)
    race_turtles.append(turtle)

if user_bet:
    is_race_on = True

# Show result on screen
result = Turtle()
result.hideturtle()
result.penup()
result.goto(0, 0)

while is_race_on:
    for turtle in race_turtles:
        turtle.forward(random.randint(1,10))

        if turtle.xcor() >= 230:
            is_race_on = False
            winning_color = turtle.pencolor()

            if winning_color.lower() == user_bet.lower():
                result.write(f"You won {winning_color} turtle won")
            else:
                result.write(f"You lose {winning_color} turtle won")


screen.exitonclick()