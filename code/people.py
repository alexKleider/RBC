#!/usr/bin/env python3

# File: people.py

"""
"""

from code import helpers
from code import data

def get_lastID():
    """
    Returns the last entered personID.
    Don't need a user interface version of this.
    """
    return data.get_highest_ID()

def get_person():
    """
    Method of selecting an entry (mapping)
    from the People table.
    """
    while True:
        hints = data.get_hints(
            header="People Table Lookup",
            text="Ener hints (no need for wild card)")
        choices = data.getP_from_clues(hints)
        choice = data.choose(choices,
            header="Choices",
            text="Select by number (0 to abort)..")
        if choice:
            if data.confirm_mapping(choice):
                return choice
        else:
            yn = data.yn(
                    header="Person not found...",
                    text="Try again? (yn): ")
            if not yn:
                return

def in_good_standing(personID):
    """ returns True (member for >= 1yr) or False """
    return data.is_member_in_good_standing(personID)

def ck_get_person():
    ret = get_person()
    if ret:
        for key, value in ret.items():
            print(f"{key}: {value}")
    else:
        print(f"get_person returned {ret}")
    return ret

def main():
    cmds_available = [
        people.get_person,
        ] 
    cmd = data.choose(cmds_available)  # may want to
        #  add default key word params header & text
    print()
    print(f"About to run {cmd.__name__} ...")
    res = cmd()
    print(f"Finished running {cmd.__name__} ==> ", end='')
    print(res)

if __name__ == "__main__":
    print("Running people.py")
