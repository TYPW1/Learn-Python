from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = self.read_high_score()
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(x=0, y=280)
        self.update_scoreboard()

    def read_high_score(self):
        with open("data.txt", mode="r") as file:
            self.high_score = int(file.read())
        return self.high_score

    def write_high_score(self):
        with open("data.txt", mode="w") as file:
            file.write(str(self.high_score))
        return self.high_score

    def update_scoreboard(self):
        self.clear()
        self.write(arg=f"Score: {self.score} High{self.write_high_score()}", move=False, align="center", font=("Courrier", 10, "bold"))

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.clear()
        self.update_scoreboard()

    # def game_over(self):
    #     self.goto(0, 0)
    #     self.write("Game Over", move=False, align="center", font=("Courrier", 20, "bold"))

    def count(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()