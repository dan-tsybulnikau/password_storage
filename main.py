import pyperclip
import random
from tkinter import messagebox
from tkinter import *
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
           'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
           'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_input.delete(0, last=END)
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 3)
    nr_numbers = random.randint(3, 4)
    password_list = [random.choice(letters) for _ in range(0, nr_letters)] + \
                    [random.choice(numbers) for _ in range(0, nr_numbers)] + \
                    [random.choice(symbols) for _ in range(0, nr_symbols)]
    random.shuffle(password_list)
    password = ''.join(password_list)
    pyperclip.copy(password)
    password_input.insert(END, f"{password}")


# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_password():
    web_site = website_input.get().lower()
    try:
        with open('./my_passwords.json', mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title='Warning', message="No Data File Found")
    else:
        if web_site in data.keys():
            messagebox.showinfo(title=web_site.title(), message=f"Email/Username: {data[web_site]['email/username']}\n"
                                                               f"Password:{data[web_site]['password']}")
            password_input.delete(0, END)
            password_input.insert(END, f"{data[web_site]['password']}")
        else:
            messagebox.showinfo(title='Info', message="No details for the website exists")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_password():
    web_site = website_input.get()
    email_username = email_username_input.get()
    password = password_input.get()
    new_data = {
        web_site.lower(): {
            "email/username": email_username.lower(),
            'password': password,
        }
    }
    if not password or not email_username or not web_site:
        messagebox.showwarning(title='Warning', message="Please fill all fields!")
    else:
        try:
            with open('./my_passwords.json', mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open('./my_passwords.json', mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open('./my_passwords.json', mode="w") as file:
                json.dump(data, file, indent=4)
        finally:
            messagebox.showinfo(title='Info', message="Data was stored")
            website_input.delete(0, last=END)
            password_input.delete(0, last=END)


# ---------------------------- UI SETUP ------------------------------- #

my_screen = Tk()
my_screen.config(padx=50, pady=50)
my_screen.title("Password Storage")
my_canvas = Canvas(width=200, height=200, highlightthickness=0)
my_image = PhotoImage(file='./logo.png')
my_canvas.create_image(100, 100, image=my_image)

website_label = Label()
website_label.config(text="Website:")
email_username_label = Label()
email_username_label.config(text="Email/Username:")
password_label = Label()
password_label.config(text="Password:")

website_input = Entry(width=32)
email_username_input = Entry(width=54)
email_username_input.insert(END, "byhrodna@gmail.com")
password_input = Entry()
password_input.config(width=32)

generate_password_button = Button()
generate_password_button.config(text="Generate password", width=17, command=generate_password)
search_button = Button()
search_button.config(text="Search", width=17, command=search_password)
add_button = Button()
add_button.config(width=46, text="Add", command=add_password)

website_label.grid(row=1, column=0)
email_username_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)
my_canvas.grid(row=0, column=0, columnspan=3)
website_input.grid(row=1, column=1, sticky=W)
website_input.focus()
email_username_input.grid(row=2, column=1, columnspan=2, sticky=W)

password_input.grid(row=3, column=1, sticky=W)
add_button.grid(row=4, column=1, columnspan=2)
search_button.grid(row=1, column=2)
generate_password_button.grid(row=3, column=2, sticky=W)
my_screen.mainloop()
