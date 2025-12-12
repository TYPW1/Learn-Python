# flashcard program (Flashy)
# This program will help users learn through flashcards.
from tkinter import *
from tkinter import messagebox
import random
import time

# display card front and back
def display_card_front():
    canvas.itemconfig(card_background, image=card_front_img)
def display_card_back():
    canvas.itemconfig(card_background, image=card_back_img)


def flip_card():
    time.sleep(3)
    display_card_back()
    # After displaying the back, wait another 3 seconds and show the front again
    time.sleep(3)
    display_card_front()
    
    

# Main window setup
window = Tk()
window.title("Flashy - Flashcard Learning App")
window.config(padx=50, pady=50, bg="#B1DDC6")

# Canvas for flashcards
canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)  
canvas.grid(row=0, column=0, columnspan=2)  

# Load images
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
right_button = Button(image=right_img, highlightthickness=0, command=flip_card)
right_button.grid(row=1, column=1)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=flip_card)
wrong_button.grid(row=1, column=0)

# write text on the card
canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))



window.mainloop()