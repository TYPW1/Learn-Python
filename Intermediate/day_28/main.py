import time
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

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 





# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
window.after(1000,)

canvas = Canvas(width=200, height=224, highlightthickness=0, bg=YELLOW)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

timer_text = Label()
timer_text.config(text="Timer", fg= GREEN, bg=YELLOW, font=(FONT_NAME, 24, "bold") )
timer_text.grid(column=1, row=0)

start_button = Button()
start_button.config(text="Start", command= lambda: print("start"))
start_button.grid(column=0, row=2)

reset_button = Button()
reset_button.config(text="Reset", command= lambda: print("reset"))
reset_button.grid(column=2, row=2)

done_label = Label(text="✓", fg= GREEN, bg=YELLOW)
done_label.grid(column=1, row=3)





















window.mainloop()