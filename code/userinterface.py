#!/usr/bin/env python3

# File: code/userinterface.py

"""
Provides the user interface (cli or gui.)
"View" in MCV
Presents (not implements) the application logic.
#####################################################
###       I believe this is redundant!!!          ###
### Functionality provided is found in ../main.py ###
#####################################################
"""

print("code/userinterface.py: being imported (or run.)")

try:
    import logic
except ModuleNotFoundError:
    from code import logic

cmds_available = [
    logic.get_person,
    logic.get_sponsors,
    logic.enter_applicant,
                  ]

choices = [(count, item.__name__) for count, item
           in enumerate(cmds_available, start=1)]


def get_P_from_clues(first='', last='', suffix=''):
    pass

if __name__ == "__main__":
    while True:
        print("**")
        print("Pick a number:")
        for choice in choices: print(f" {choice}")
        try:
            n = int(input(
      "Choose a function to execute (0 to quit): "))
        except ValueError:
            print("!!! Must be a number !!!")
            continue
        if n == 0: break
        if n<0 or n>len(cmds_available):
          print("Number must be >=0 and " +
            f"<= {len(choices)}")
          continue
        cmds_available[n-1]()
