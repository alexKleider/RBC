#!/usr/bin/env python3

# File: main.py

"""
Driver program for Bolinas Rod & Boat Club data management.
"""

try: from code import cli as ui
except ImportError: import cli as ui
try: from code import helpers
except ImportError: import helpers
try: import logic
except ImportError: from code import logic
try: from code import send_emails
except ImportError: import send_emails
try: from code import ck_data
except ImportError: import ck_data
try: from code import people
except ImportError: import people
try: from code import applicants
except ImportError: import applicants


cmds_available = [
    people.get_person,
    applicants.get_sponsors,
    applicants.enter_applicant,
    applicants.update_applicant,
    send_emails.test_send,
    ck_data.check_consistency_report,
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
                if helpers.is_iterable(res):
                    for item in res:
                        print(item)
                else: print(res)
        else:
            print("User terminated driver program!")
            break

if __name__ == "__main__":
#   forJune.member_email_listing()
#   logic.create_person()
    main()
#   print(f"{logic.getID()=}")
#   logic.enter_applicant()
