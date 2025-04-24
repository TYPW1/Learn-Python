from tkinter import *

window = Tk()
window.title("Miles to Kilometers Converter")
window.minsize(300, 200)
window.config(padx=15, pady=15)

def calculate():
    miles  = float(user_input_text.get())
    km = miles * 1.60934
    user_input_label.config(text=int(km))

equal_label = Label()
equal_label.config(text="is equal to", font=("Arial", 15, "bold"))
equal_label.grid(column=0, row=1)

km_label = Label()
km_label.config(text="km", font=("Arial", 15, "bold"))
km_label.grid(column=2, row=1)

miles_label = Label()
miles_label.config(text="miles", font=("Arial", 15, "bold"))
miles_label.grid(column=2, row=0)

user_input_label = Label()
user_input_label.config(text="0", font=("Arial", 15, "bold"))
user_input_label.grid(column=1, row=1)

user_input_text= Entry()
user_input_text.config(width=10)
user_input_text.grid(column=1, row=0)

button = Button()
button.config(text="Calculate", font=("Arial", 15, "bold"), command=calculate)
button.grid(column=1, row=2)

window.mainloop()