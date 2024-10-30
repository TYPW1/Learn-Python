import colorgram
from turtle import Turtle, Screen
import random
import turtle
colors = colorgram.extract("image.jpg",100)


def get_colours():
    colours = []
    for i in range(len(colors)):
        r = colors[i].rgb.r
        g = colors[i].rgb.g
        b = colors[i].rgb.b
        c = (r,g,b)
        if r < 200 or g < 200 or b < 200:  # Adjust threshold as needed
            c = (r, g, b)
            colours.append(c)

    return colours




tim = Turtle()
tim.hideturtle()
tim.speed("fastest")
turtle.colormode(255)


for j in range (10):
    for k in range(10):
        tim.penup()
        tim.forward(50)
        tim.dot(25, random.choice(get_colours()))
    tim.setheading(180)
    tim.forward(500)
    tim.setheading(90)
    tim.forward(50)
    tim.setheading(0)

screen = Screen()
screen.exitonclick()