import turtle
from turtle import Screen, Turtle
import pandas as pd

screen = Screen()
screen.title("U.S. State Quiz")
screen.setup(width=725, height=491)
screen.bgpic("blank_states_img.gif")

#get state only series
state_data = pd.read_csv("50_states.csv")
all_states = state_data["state"].to_list()

#correct state list
guessed_states = []


#find user state from the list of all states
def find_state_in_list(state, state_list):
    for s in state_list:
        if state.lower() == s.lower():
            return True
    return False


#add correct state to a list

#get state coordinates
def get_state_coordinates(state_name):
    state_row = state_data[state_data.state == state_name]
    return int(state_row.x), int(state_row.y)

# Create a turtle to write the state name
def write_state_name(state_name, x, y):
    state_turtle = Turtle()
    state_turtle.hideturtle()
    state_turtle.penup()
    state_turtle.goto(x, y)
    state_turtle.write(state_name, align="center", font=("Arial", 8, "normal"))

#loop to keep asking for states until all are guessed
while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct", prompt="What's another state's name?").title()
    if answer_state == "Exit":
        break
    # Check if the answer is already guessed
    if answer_state in guessed_states:
      if not hasattr(screen, "alert_turtle"):
          screen.alert_turtle = Turtle()
          screen.alert_turtle.hideturtle()
          screen.alert_turtle.penup()
      screen.alert_turtle.clear()
      screen.alert_turtle.goto(0, 50)
      screen.alert_turtle.write("Already guessed", align="center", font=("Arial", 8, "normal"))

    elif find_state_in_list(answer_state, all_states):
        guessed_states.append(answer_state)
        x, y = get_state_coordinates(answer_state)
        write_state_name(answer_state, x, y)
    else:
        # If the state is not found, tutle print an alert box
        if not hasattr(screen, "alert_turtle"):
            screen.alert_turtle = Turtle()
            screen.alert_turtle.hideturtle()
            screen.alert_turtle.penup()
        screen.alert_turtle.clear()
        screen.alert_turtle.goto(0, 50)
        screen.alert_turtle.write("State not Found", align="center", font=("Arial", 8, "normal"))

#screen stays on
screen.mainloop()