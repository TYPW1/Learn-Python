import colorgram
from turtle import Turtle
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
        colours.append(c)
    return colours



tim = Turtle()
tim.shape("turtle")
tim.speed(10)
turtle.colormode(255)

# tim.penup()
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.setheading(90)

# numi = 1
# for o in range(10):
#     numi= numi + numi
#
#     print(numi)

num = 1
for j in range (10):

    for i in range(10):
        tim.penup()
        tim.forward(50)
        tim.dot(25, random.choice(get_colours()))
    tim.setheading(90)
    tim.forward(50)
    tim.dot(25, random.choice(get_colours()))
    tim.setheading(90**num + num)

#
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.setheading(90)
# tim.forward(50)
# tim.dot(25, random.choice(get_colours()))
# tim.setheading(90**4)
