"""import turtle
from turtle import Turtle, Screen

timmy = Turtle()

print(timmy)

timmy.shape("turtle")
timmy.color("PuRpLe")
timmy.speed(0.6)
timmy.forward(100)
timmy.left(90)
timmy.speed(1)
timmy.forward(100)
my_screen = Screen()
my_screen.exitonclick()"""

from prettytable import PrettyTable

table = PrettyTable()

table.add_column("Pokemon Name", ["Pikachu", "Squirtle", "Charmander"], "l")

table.add_column("Type", ["Electric", "Water", "Fire"],"l")
print(table)
