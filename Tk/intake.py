#!/usr/bin/env python3

# File: intake.py

import tkinter as tk
#from tkinter import *

#to run the command set on submit button
#entry1.get() stores the text we wrote on entry widget in user variable

def get_credentials():
    pass
    credentials = {}

    def print_on_terminal():
        nonlocal credentials
        credentials["user"] = entry1.get()
        credentials["pw"] = entry2.get()
        root.quit()
#       print(f"Username: {user} \n Password: {pw}")


    #Initaiting
    root = tk.Tk()
    root.title("Login Example")
    root.geometry("300x150")

    #placing the username and password label
    label1 = tk.Label(root, text="Username:")
    label2 = tk.Label(root, text="Password:")
    label1.place(x=10, y=20)
    label2.place(x=10, y=60)

    #placing the entry widgets
    entry1 = tk.Entry(root)  # For username
    entry2 = tk.Entry(root, show='*') #shows * for anything we type
    entry1.place(x=100, y=20)
    entry2.place(x=100, y=60)

    #creating a submit button
    submit_button = tk.Button(root, text="Submit", command= print_on_terminal)
    submit_button.place(x=100, y=100)

    root.mainloop()
    
    if not credentials: return
    else: return credentials

def ck_get_credentials():
    pw = get_credentials()
    if pw:
        for key, val in pw.items():
#       for key, val in [key, val for key, val in pw.items()]:
            print(f"{key}: {val}")
    else: print("Authentication aborted!")

if __name__ == "__main__":
    ck_get_credentials()

