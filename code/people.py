#!/usr/bin/env python3

# File: people.py

"""
Code dealing with the People table.
"""

from code import helpers
from code import data

# if True:
#   When entering data: option is provided to
#   collect it from a JSON file
#   and
#   once entered, option is provided to 
#   save it in a JSON file (for future use prn.)

def create_person():
    """
    Attempts to Create an entry into the People table
    & Return mapping with personID value.
    Returns None if attempt fails.
    First question only needed during debugging: it
    allows one to have data available without having
    to re-enter it. == A_new_person.json
    """
    def collect_data():
        keys = data.person_keys()
        mapping = {key: "" for key in keys}
        person = data.entries(mapping,
            header="Adding New Person to People Table",
            text="Add values (empty strings accepted)... ")
        return person
    
    if data.store_data:  # allow use of existing data
        yn = input("Load existing data (yY): ")
        if (yn and yn[0] in ("yY")): 
            person = helpers.load_json_file(
                    data.store_dict["create_person"])
        else:
            person = collect_data()
    else:
        person = collect_data()

    if person:
        data.put_person(person)
        if data.store_data:
            # for debugging purposes: saves the data so
            # it can be retrieved next time code is run
            helpers.dump2json(person,
                        data.store_dict["create_person"])
        person["personID"] = get_lastID()
        return person
    else:
        print("logic/create_person returning None!")

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

def get_lastID():
    """
    Returns the last entered personID.
    Don't need a user interface version of this.
    """
    return data.get_highest_ID()

def assign_status(personID, stati2assign):
    """
    Assumes <personID> already exists in the People table.
    Makes entries into the <Person_Status> table with
    -begin- date defaulting to -today-.
    """
    pass

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
