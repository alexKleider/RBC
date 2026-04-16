#!/usr/bin/env python3

# File: app_page.py

"""
"""
import helpers
import sql
import tkinter as tk
from tkinter import ttk

# Necessary Globals...
global_res = {}

def get_app_info():
    """
    Returns a mapping of all data needed to 
    enter a new Applicant.
    """
    def submit_data():
        global global_res
        for key in mapping.keys():
            global_res[key] = str_vars[key].get()
        root.destroy()

    keys = ['first', 'last', 'suffix', 'phone',
            'address', 'town', 'state',
            'postal_code', 'country', 'email']

    root = tk.Tk()
    root.title("New Applicant Entry")
    root.geometry("640x480+300+300")
    root.resizable(False, False)

    mapping = {key: "" for key in keys}
    labels = {}
    str_vars = {}
    values = {}
    row = 0;

    title = tk.Label(root, text='Enter available data',
         font=('Ariel 16 bold'), bg='brown', fg='#FF0')

    for key, value in mapping.items():
        labels[key] = tk.Label(root, text=key)
        labels[key].grid(row=row, column=0)
        str_vars[key] = tk.StringVar(value=value)
        values[key] = tk.Entry(root,
                       textvariable=str_vars[key])
        values[key].grid(row=row, column=1)
        row += 1;

    # Submit Button
    submit_button = tk.Button(root,
                text="Submit", command=submit_data)
    submit_button.grid(row=row, column=1)

    root.mainloop()
    return global_res


if __name__ == "__main__":
    print("Running app_page.py")
    applicant = get_app_info()
    for key, val in applicant.items():
        print(F"{key}: {val}")

