#!/usr/bin/env python3

# File: intake.py

import tkinter as tk
#from tkinter import *

#to run the command set on submit button
#entry1.get() stores the text we wrote on entry widget in user variable
def print_on_terminal():
    user = entry1.get()
    pw = entry2.get()
    print(f"Username: {user} \n Password: {pw}")


#Initaiting
window = tk.Tk()
window.title("Login Example")
window.geometry("300x150")

#placing the username and password label
label1 = tk.Label(window, text="Username:")
label2 = tk.Label(window, text="Password:")
label1.place(x=10, y=20)
label2.place(x=10, y=60)

#placing the entry widgets
entry1 = tk.Entry(window)  # For username
entry2 = tk.Entry(window, show='*') #shows * for anything we type
entry1.place(x=100, y=20)
entry2.place(x=100, y=60)

#creating a submit button
submit_button = tk.Button(window, text="Submit", command= print_on_terminal)
submit_button.place(x=100, y=100)

window.mainloop()
