#!/usr/bin/env python3

# File: people.py

"""
"""

from code import helpers
from code import data
from code import applicants

def create_person():
    """
    Attempts to Create an entry into the People table
    & Return mapping with personID value.
    Returns None if attempt fails.
    """
    yn = input("Enter person data (yY) or collect from file?: ")
    if (yn and yn[0] in ("yY")): 
        keys = data.person_keys()
        mapping = {key: "" for key in keys}
        person = data.entries(mapping,
            header="Adding New Person to People Table",
            text="Add values (empty strings accepted)... ")
    else:
        person = helpers.load_json_file("A_new_person.json") 
    if person:
        data.put_person(person)
        helpers.dump2json(person,
                          "A_new_person.json")
        person["personID"] = applicants.get_lastID()
        return person
    else:
        print("logic/create_person: person is False")

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

if __name__ == "__main__":
    print("Running people.py")
