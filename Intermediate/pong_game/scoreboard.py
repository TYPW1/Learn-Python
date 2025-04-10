from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score1 = 0
        self.score2 = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"Player 1: {self.score1} Player 2: {self.score2}", align="center", font=("Courier", 24, "normal"))

    def player1_score(self):
        self.score1 += 1
        self.update_scoreboard()

    def player2_score(self):
        self.score2 += 1
        self.update_scoreboard()