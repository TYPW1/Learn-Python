# flashcard program (Flashy)
# This program will help users learn through flashcards.
from tkinter import *
from tkinter import messagebox
import random
import time
import pandas as pd

# display card front and back
def display_card_front():
    canvas.itemconfig(card_background, image=card_front_img)
def display_card_back():
    canvas.itemconfig(card_background, image=card_back_img)
try:
    df = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = df.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)  # Cancel previous timer
    current_card = random.choice(to_learn)
    print(current_card['French'])
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    display_card_front()
    flip_timer = window.after(3000, flip_card)


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_card()

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
    display_card_back()
    

# Main window setup
window = Tk()
window.title("Flashy - Flashcard Learning App")
window.config(padx=50, pady=50, bg="#B1DDC6")

flip_timer = window.after(3000, flip_card)  # Schedule flip_card to run after 3 seconds
# Canvas for flashcards
canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)  
canvas.grid(row=0, column=0, columnspan=2)  

# Load images
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

right_button = Button(image=right_img, highlightthickness=0, command=next_card)
right_button.grid(row=1, column=1)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=is_known)
wrong_button.grid(row=1, column=0)

# write text on the card
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

next_card()


window.mainloop()