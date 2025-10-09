from tkinter import *
from tkinter import messagebox
import random

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)

password_list = []

password_list = [random.choice(letters) for _ in range(nr_letters)] + \
                [random.choice(symbols) for _ in range(nr_symbols)] + \
                [random.choice(numbers) for _ in range(nr_numbers)]

random.shuffle(password_list)

password = ""
for char in password_list:
  password += char

print(f"Your password is: {password}")
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    # Check if wy<------§ebsite is valid
    if not website or not website_entry.get().isalnum():
        messagebox.showerror(title="Invalid Website", message="Please enter a valid website name.")
        return
    # Check if email is valid
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        messagebox.showerror(title="Invalid Email", message="Please enter a valid email address.")
        return
    # Check if password is valid
    if not password or len(password) < 8:
        messagebox.showerror(title="Invalid Password", message="Password must be at least 8 characters long.")
        return
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\nIs it okay to save?")
    if is_ok:
        with open("data.txt", "a") as data_file:
            data_file.write(f"{website} | {email} | {password}\n")
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        website_entry.focus()
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=20)

canvas = Canvas(width=200, height=200)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=2)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=3)
password_label = Label(text="Password:")
password_label.grid(column=0, row=4)

# Entries
website_entry = Entry(width=35)
website_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
website_entry.focus()
email_entry = Entry(width=35)
email_entry.insert(0, "example@example.com")
email_entry.bind('<FocusIn>', lambda e: email_entry.delete(0, END) if email_entry.get() == "example@example.com" else None)
email_entry.bind('<FocusOut>', lambda e: email_entry.insert(0, "example@example.com") if email_entry.get() == "" else None)
email_entry.grid(column=1, row=3, columnspan=2, sticky="EW")
password_entry = Entry(width=21)
password_entry.grid(column=1, row=4, sticky="EW")

generate_password_button = Button(text="Generate Password", width=14, pady=2)
generate_password_button.grid(column=2, row=4, sticky="EW")
add_button = Button(text="Add", width=35, pady=2, command=save_password)
add_button.grid(column=1, row=5, columnspan=2, sticky="EW")

window.mainloop()