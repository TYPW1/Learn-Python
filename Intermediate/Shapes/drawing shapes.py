import turtle
from turtle import Screen, Turtle
import random
import colorgram
tim = Turtle()

tim.shape("turtle")

#draw a circle with circles
# turtle.colormode(255)
# def randomcolor():
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     color = (r,g,b)
#     return color
#
# for i in range(25):
#     if tim.home() is not True:
#         tim.color(randomcolor())
#         tim.speed("fastest")
#         tim.setheading(25*i)
#         tim.circle(100, 360)

#timmy creates a square
# for i in range(5):
#     tim.speed(1)
#     tim.forward(100)
#     tim.right(90)

#get turtle to move and create blanks
# for i in range(15):
#     for j in range (10):
#         tim.forward(10)
#         tim.penup()
#         tim.forward(10)
#         tim.pendown()
#     for k in range(20):
#         tim.forward(10)
#         tim.penup()

#get turtle to build a triangle, square and pentagon
#startedwith this
# def trinagle():
#     for i in range (3):
#         tim.forward(100)
#         tim.right(120)
#
# def square():
#     for i in range (4):
#         tim.forward(100)
#         tim.right(90)
#
# def pentagon():

#     for i in range (5):
#         tim.forward(100)
#         tim.right(72)
#easier and simpler solution
# def shape(size, angle):
#     colors = ["red", "green", "blue", "orange", "purple", "pink", "yellow"]
#     tim.color(random.choice(colors))
#     for i in range (size):
#         tim.forward(100)
#         tim.right(angle)
#
# for j in range (3,20):
#     k = 360
#     shape(j,k/j)

#get turtle to move randomly around the map(big lines, random line length, random colours, random speed)
# colours = ["red", "green", "blue", "orange", "purple", "pink", "yellow"]
# directions = [0, 90, 180, 270]
# for _ in range (300): # set it 300 times to draw
#     tim.pensize(10)
#     tim.color(random.choice(colours))
#     tim.forward(30)
#     tim.speed(random.randrange(0,10))
#     tim.setheading(random.choice(directions))#randomly to choose a random directions.

# #give turtle random colors
# turtle.colormode(255)
# def randomcolor():
#     r = random.randint(0,255)
#     g = random.randint(0,255)
#     b = random.randint(0,255)
#     color = (r,g,b)
#     return color
# tim.color(randomcolor())

tim.setheading(0)

screen = Screen()
screen.exitonclick()

