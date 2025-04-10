from turtle import Turtle

class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.goto(position)
        self.shapesize(stretch_wid=5, stretch_len=1)

    # This method moves the paddle up by 20 units
    def go_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    # This method moves the paddle down by 20 units
    def go_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)

