import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

window = tk.Tk()
window.title("My first GUI")
window.minsize(500, 300)
window.config(padx=200, pady=200)



def button_clicked():
    label["text"] = input.get()

#label
label = tk.Label(text= "I am a Label", font=("Arial", 24, "bold"))
label["text"] = "New Text"
label["font"] = ("Arial", 24, "bold")
label.grid(column=0, row=0)


# button2
button1 = tk.Button(text="Click Me", command=button_clicked)
button1.grid(column=1, row=1)

# button2
button2 = tk.Button(text="Click Me")
button2.grid(column=2, row=0)

# entry
input = tk.Entry(width=10)
input.grid(column=3, row=2)

# text
text = tk.Text(height=5, width=30)

# spinbox
spinbox = tk.Spinbox(from_=0, to=10, width=5)


# scale
scale = tk.Scale(from_=0, to=100, orient="horizontal")


# checkbutton
checkbutton = tk.Checkbutton(text="Is On?", command=lambda: print("Checked"))


# radiobutton
radiobutton1 = tk.Radiobutton(text="Option 1", value=1)


# listbox
fruits = ["Apple", "Banana", "Cherry", "Date"]
listbox = tk.Listbox(height=4)
for fruit in fruits:
    listbox.insert(fruits.index(fruit), fruit)









window.mainloop()