import time
import math
from tkinter import *

from sympy.abc import lamda

#from Projects.pdf_editor_streamlit.app import columns

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    count_down(3)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec == 0:
        count_sec = "00"


    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        window.after(1000, count_down, count - 1)



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(width=200, height=224, highlightthickness=0, bg=YELLOW)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


timer_label = Label()
timer_label.config(text="Timer", fg= GREEN, bg=YELLOW, font=(FONT_NAME, 24, "bold") )
timer_label.grid(column=1, row=0)

start_button = Button()
start_button.config(text="Start", command= start_timer)
start_button.grid(column=0, row=2)

reset_button = Button()
reset_button.config(text="Reset", command= lambda: print("reset"))
reset_button.grid(column=2, row=2)

done_label = Label(text="✓", fg= GREEN, bg=YELLOW)
done_label.grid(column=1, row=3)





















window.mainloop()