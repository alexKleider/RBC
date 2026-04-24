#!/usr/bin/env python3

# File: /home/alex/Git/RBC/code/proto_gui.py
# (graphical user interface using tKinter)
#   initially copied from /home/alex/Git/TK/gui.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

"""
Plan: have this module provide exactly the same
functionality as that provided by cli.py.

Provides: so far- 
    yn
    func_menu
    make_choice
    update_mapping
NOTE: we already have a code/gui.py module!!!!!
"""

returned_choice = None  # Globals required by...
global_res = {}         # make_choice and update_mapping

def yn(title, message):
    """
    Returns True or False.
    Note: [x] button also returns false
            (same as hitting the "No" box.)
    """
    def show_yes_no_dialog():
        result = messagebox.askyesno(title, message)
        root.destroy()
        return result
    root = tk.Tk()
    root.withdraw()    # Hide the main window
    ret = show_yes_no_dialog()
    root.mainloop()
    return ret


def func_menu(funcs,
              header="Choose a Function to Run"):
    """
    <funcs> is a listing of functions.
    Chosen funtion is executed.
    (unless user exits using [X].)
    """
    def destroyer(func):
        def wrapper(*args, **kwargs):
            res = func()
            root.destroy()
        return wrapper

    root = tk.Tk()
    root.title(header)
    root.geometry("400x300")

    # 1. Sidebar Frame
    sidebar = tk.Frame(root, bg="#2c3e50",
                       width=150, height=300)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    #  ^ Prevents frame from shrinking to button size

    # 2. Menu Buttons (Vertical Items)
    #menu_items = ["Dashboard", "Settings", "Profile", "Help"]
    #for item in menu_items:
    for func in funcs:
        # decorate each function to include root.destroy() 
        btn = tk.Button(
            sidebar, 
            text=func.__name__, 
            command= destroyer(func),
                    # ...decorate with a root.destroy() line
            bg="#2c3e50", 
            fg="white", 
            activebackground="#34495e", 
            activeforeground="white",
            bd=0, 
            padx=20, 
            pady=10, 
            anchor="w")
#       print(f"assigned {func.__name__}")
        btn.pack(fill="x")
        # ^ ensures buttons take full width of sidebar

    # 3. Main Content Area
#   main_area = tk.Frame(root, bg="white")
#   main_area.pack(side="right", expand=True, fill="both")

#   label = tk.Label(main_area,
#                    text="Select an option from the menu",
#                    bg="white")
#   label.pack(pady=50)

    root.mainloop()

def make_choice(choices, rootTitle):
    """
    <choices>: a listing of strings
    Returns selected string.
    Returns None if window is closed using the (top right) [X]
    Relies on presence of the nonlocal <returned_choice>.
    """
    returned_choice = None
    def bound_func(param=None):
        nonlocal returned_choice
        selection_index = listbox.curselection()
        if selection_index:
            # Get the value of the selected item
            returned_choice = listbox.get(selection_index[0])
        else:
            returned_choice = None
        root.destroy()

    # --- Main Application ---
    root = tk.Tk()
    root.title("Listbox Menu Example")

    # Create a Listbox widget
    listbox = tk.Listbox(root,
                         selectmode=tk.SINGLE,
                         width=0)
    listbox.pack(padx=10, pady=10)

    # Populate the Listbox with choices
    for item in choices:
        listbox.insert(tk.END, item)

    # Bind the selection event to a function
    listbox.bind('<<ListboxSelect>>', bound_func)

    root.mainloop()
    return returned_choice


def updated_mapping(mapping, header="Record Update"):
    """
    Provides a way of entering or modifying the values of a
    <mapping>, presented in a window labeled <header>.
    Returns None if closed without using the submit button.
    The <submit> button causes return of a new mapping with
    the visible values. The original mapping is left unchanged.
    Retrieval depends on <global_res> which must exist globally.
    """
    def submit_data():
        global global_res
        for key in mapping.keys():
            global_res[key] = str_vars[key].get()
        root.destroy()

    root = tk.Tk()
    root.title(header)

    keys = mapping.keys()
    labels = {}
    str_vars = {}
    values = {}

    row = 0;

    for key, value in mapping.items():
        labels[key] = tk.Label(root, text=key)
        labels[key].grid(row=row, column=0)
        str_vars[key] = tk.StringVar(value=value)
        values[key] = tk.Entry(root, textvariable=str_vars[key])
        values[key].grid(row=row, column=1)
        row += 1;

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit_data)
    submit_button.grid(row=row, column=1)

    root.mainloop()
    return global_res


def checkYN():
    title = "Exit Application"
    message = """This could be a very long message.
        Several lines long, infact!
        Do you really want to exit?"""
    if yn(title, message):
        print("Returning True")
    else:
        print("Returning False")

def ck_func_menu():
    def func1():
        print(f"Executing func1")
        return "f1"
    def func2():
        print(f"Executing func2")
    def func3():
        print(f"Executing func3")
    def func4():
        print(f"Executing func4")
        return "f4"
    def func5():
        print(f"Executing func5")
    def func6():
        print(f"Executing func6")
    funcs = (func1, func2, func3, func4, func5, func6 )
    
    print(f"Running func_menu...")
    func_menu(funcs)

def ck_make_choice():
    header = "Root Title"
    # List of choices
    choices = ["AppleAppleAppleAppleAppleAppleAppleAppleAppleAppleApple",
               "BananaBananaBananaBananaBananaBananaBananaBanana",
               "CherryCherryCherryCherryCherryCherryCherryCherryCherryCherry",
               "DateDateDateDateDateDateDateDateDateDateDateDateDateDate",
               "ElderberryElderberryElderberryElderberryElderberryElderberry"]
    ret = make_choice(choices, header)
    
    print("Your choice...")
    print(repr(ret))


def ck_updated_mapping():
    mapping = {
            "First": "Joe",
            "Last": "Blow", 
            "Phone": "333/333-3333",
             }
    header = "People Entry"
    res = updated_mapping(mapping, header)
    if res:
        for key, value in res.items():
            print(f"{key}: {value}")
    else:
        print(f"Entry aborted (returned {res=})")


if __name__ == "__main__":
    test_funcs = (checkYN,
                  ck_func_menu,
                  ck_make_choice,
                  ck_updated_mapping)
    while True:
        print("Choose which function to test:")
        for index, func in enumerate(test_funcs, start=1):
            print(f"  {index:>3}  {func.__name__}")
        choice = input(f"Which one? (1..{len(test_funcs)}) 0 to quit ")
        func_index = int(choice) -1
        if choice == "0":
            break
        func = test_funcs[func_index]
        print(f"Testing {func.__name__}...")
        func()
        print(f"...finished testing {func.__name__}...")




