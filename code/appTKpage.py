#!/usr/bin/env python3

# File: appTKpage.py

"""
Supplies gui method of entering an Applicant's data.
Unfortunately, tried to do too much.
Expect this to be redacted but keeping it for reference.
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

    def check_sponsors():
        pass


    root = tk.Tk()
    root.title("New Applicant Entry")
    root.geometry("640x480+300+300")
    root.resizable(False, False)

    # Enter applicant's data...
    keys = ['first', 'last', 'suffix', 'phone',
            'address', 'town', 'state',
            'postal_code', 'country', 'email']
    mapping = {key: "" for key in keys}
    labels = {}
    str_vars = {}
    values = {}

    title = tk.Label(root, text='Enter applicant data')
#        font=('Ariel 16 bold'), bg='brown', fg='#FF0')
    title.grid(row=0, column=1)
    row = 1
    for key, value in mapping.items():
        labels[key] = tk.Label(root, text=key)
        labels[key].grid(row=row, column=0)
        str_vars[key] = tk.StringVar(value=value)
        values[key] = tk.Entry(root,
                       textvariable=str_vars[key])
        values[key].grid(row=row, column=1)
        row += 1;
    # Collect sponsor data...
    col3 = 2; col4 = 3;
    # 1st sponsor...
    s1_title = tk.Label(root,
                text="Find 1st sponsor (use % wildcards)")
    s1_title.grid(row=0, column=col3)

    s1keys = ['S1_first', 'S1_last', 'S1_suffix']
    s1mapping = {key: "" for key in s1keys}
    s1labels = {}
    s1str_vars = {}
    s1values = {}
    row = 1
    for key, value in s1mapping.items():
        s1labels[key] = tk.Label(root, text=key)
        s1labels[key].grid(row=row, column=col3)
        s1str_vars[key] = tk.StringVar(value=value)
        s1values[key] = tk.Entry(root,
                        textvariable=s1str_vars[key])
        s1values[key].grid(row=row, column=col4)
        row += 1
    row +=1
    s1id_label = tk.Label(root,text="Sponsor 1 ID")
    s1id_label.grid(row=row, column = 3)
    # 2nd sponsor...
    row += 2
    s2_title = tk.Label(root,
                text="Find 2nd sponsor (use % wildcards)")
    s2_title.grid(row=row, column=col3)
    row += 1
    s2keys = ['S2_first', 'S2_last', 'S2_suffix']
    s2mapping = {key: "" for key in s2keys}
    s2labels = {}
    s2str_vars = {}
    s2values = {}
    for key, value in s2mapping.items():
        s2labels[key] = tk.Label(root, text=key)
        s2labels[key].grid(row=row, column=col3)
        s2str_vars[key] = tk.StringVar(value=value)
        s2values[key] = tk.Entry(root,
                        textvariable=s2str_vars[key])
        s2values[key].grid(row=row, column=col4)
        row += 1
    row +=1
    s2id_label = tk.Label(root,text="Sponsor 2 ID")
    s2id_label.grid(row=row, column = 3)


    # Submit Button
    submit_button = tk.Button(root,
                text="Submit", command=submit_data)
    submit_button.grid(row=30, column=2)

    root.mainloop()
    return global_res


if __name__ == "__main__":
    print("Running app_page.py")
    applicant = get_app_info()
    for key, val in applicant.items():
        print(F"{key}: {val}")

