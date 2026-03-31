#!/usr/bin/env python3

# File: main.py

"""
Driver program for Bolinas Rod & Boat Club data management.
"""

try:
    from code import cli as ui
except ImportError:
    import cli as ui
try:
    from code import logic
except ImportError:
    import logic
try:
    from code import send_emails
except ImportError:
    import send_emails

cmds_available = [
    logic.get_person,
    logic.get_sponsors,
    logic.enter_applicant,
    logic.update_applicant,
    send_emails.test_send,
    ]

def main():
    print("beginning main.py")
    while True:
        command = ui.choose(cmds_available)
        if command:
            res = None
            print(f"Running {command.__name__} ...")
            res = command()
            if res:
                print(f"{command.__name__} yielded...")
                if helpers.isiterable(res):
                    for item in res:
                        print(item)
                else: print(res)
        else:
            print("Program ('main.py') aborted!")
            break

if __name__ == "__main__":
#   logic.create_person()
    main()
#   print(f"{logic.getID()=}")
#   logic.enter_applicant()
