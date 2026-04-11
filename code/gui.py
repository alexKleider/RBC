#!/usr/bin/env python3

# File: code/gui.py

"""
Provides the graphical user interface
(via the ui.py module.)
i.e. import gui as ui
"""

#print("code/gui.py: being imported (or run.)")
#print("!!!!!! run? !!!!!!!")

import tkinter as tk
from tkinter import ttk

try:
    import helpers
except ImportError:
    from code import helpers


def announce(header="Note the following...",
             text="Announcing..."):
    """
    Prints the header and the text
    and waits for 'go ahead' to proceed.
    """
    print("*"*len(header))
    print(header)
    print("*"*len(header))
    print(text)
#   _ = input("Any key to continue: ")


def ok(header="Confirmation Required",
       text="OK to proceed? (y/n"):
    """
    Returns True or False
    or possibly None if window is 'x'ed
    or if user response does not begin with
    one of the following letters: "yYnN".)
    """
    print("*"*len(header))
    print(header)
    print("*"*len(header))
    yn = input(text)
    if yn and yn[0] in "yY":
        return True
    if yn and yn[0] in "nN":
        return False
    return

def choose(choices):
    """
    <choices> must be a list of either functions or strings.
    Returns the chosen function or string.
    May return None (if choices is not an iterable,
                                is an empty list,
                             or if no choice is made.)
    """
    if not helpers.is_iterable(choices): return
    choices = [choice for choice in choices]
    if not choices: return
    _callable = callable(choices[0])
    if _callable:
        listing = [(count, item.__name__) for count,
            item in enumerate(choices, start=1)]
    else:
        listing = [(count, choice) for count, choice 
               in enumerate(choices, start=1)]
    while True:
        header = "Pick a number:" 
        print("*"*len(header))
        print(header)
        for option in listing: print(f" {option}")
        message = "Choose one (0 to quit): "
        if _callable: 
            message = ("Choose a function to " +
                "execute (0 to quit): ")
        else:
            message = (
                f"Chose 0 to {len(choices)} (0 to quit): ")
        try:
            n = int(input(message))
        except ValueError:
            print("***")
            print("!!! Must be a number !!!")
            continue
        if n == 0: break  # returns None
        if n<0 or n>len(choices):
          print("***")
          print("!!! Number must be >=0 and " +
            f"<= {len(choices)} !!!")
          continue
        return choices[n-1]

def entries(mapping,
            header="Data Entry",
            text="Rtn to leave value as is..."):
    while True:
            print("=" * len(header))
            print(header)
            print("=" * len(header))
            print(text)
            ret = {}
            for key, value in mapping.items():
                if value:
                    entry = input(f"{key}: {value}; New value: ")
                else:
                    entry = input(f"{key}: New value: ")
                if entry: ret[key] = entry
                else: ret[key] = value
            if ok(text="OK with above entries? (y/n) "):
                return ret
            if not ok(header="Try again?", text="y/n "):
                return
            else:
                mapping = {key: value for key, value
                           in ret.items()}

accept = None

def get_hints(header="People Table Lookup",
              text="Enter hints"):
    """
    Returns a mapping of first, last, +/- suffix
    """
    def on_accept():
        root.quit()
        global accept
        accept = True
    
    def on_abort():
        root.quit()
        global accept
        accept = False

    root = tk.Tk()
    root.title(header)
    root.columnconfigure(0, weight=1)

    ttk.Label(root, text=text, font=("TkDefaultFont", 16)).grid()
    # data record form...
    drf = ttk.Frame(root)
    drf.grid(padx=10, sticky=(tk.E + tk.W))
    drf.columnconfigure(0, weight=1)

    keys = ("first", "last", "suffix",)
    v = dict()
    col = 0
    row = 0
    for key in keys:
        # v for variables...
        v[key] = tk.StringVar()
        ttk.Label(drf, text=key).grid(row=row, column=col)
        ttk.Entry(drf, textvariable=v[key]
                  ).grid(row=row, column=col+1)
        row += 1
    #creating a submit button
    submit_btn = tk.Button(root, text="Submit", command=on_accept)
    submit_btn.grid(row=98)
    #create an abort button
    abort_btn = tk.Button(root, text="Abort", command=on_abort)
    abort_btn.grid(row=99)

    root.mainloop()
    if accept:
        ret = {}
        for key, val in v.items():
            ret[key] = val.get()
        return ret
    else:
        return

def main():
    res = get_hints(header="People Table Lookup",
                              text="Enter hints")
    if res:
        for key, val in res.items():
            print(f"{key}: {val}")
    else:
        print("Mission aborted")


if __name__ == "__main__":
    print("Running code/gui.py")
    main()
