from turtle import Screen
from food import Food
from snake import Snake
from scoreboard import Scoreboard
import time

screen = Screen()
screen.tracer(0)
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")

snake = Snake()
food = Food()
score = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # detect collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        score.count()

    # Detect collision with wall
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        score.reset()
        snake.reset()

    # Detect collision with tail
    for segment in snake.segments[1:]:
        # if segment == snake.head:
        #     pass
        if snake.head.distance(segment) < 10:
            score.reset()
            snake.reset()



screen.exitonclick()