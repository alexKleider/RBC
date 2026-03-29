#!/usr/bin/env python3

# File: code/logic.py

"""
Provides the core (business) logic.
"Controller" in MCV.
getters: person, sponsor, ...
putters: person, applicant, 
!!!!!!! Won't run !!!!!!!
Can be imported by main.py and tested that way.
"""

try:
    import data
except ImportError:
    from code import data

try:
    import content
except ImportError:
    from code import content

try:
    from code import cli as ui
except ImportError:
    import cli as ui

#print("logic.py: being imported (or run.)")

class Applicant(object):
    pass

def getID():
    """
    Returns the last entered personID.
    """
    return data.get_highest_ID()

def get_person():
    """
    Method of selecting an entry from 
    the People table.
    """
    while True:
#       print("entering func get_person")
        hints = ui.get_hints()
        choices = data.getP_from_clues(hints)
        choice = ui.choose(choices)
#       print("func get_person returning...")
#       print(choice)
        if choice:
            if ui.ok(header=repr(choice),
                 text="Confirm above is OK (y/n) "):
                return choice
        else:
            if not ui.announce(
                    header="Person not found...",
                    text="Try again? (yn): "):
                return

def get_sponsors():
    """
    Returns a tuple of sponsor records.
    """
    while True:
        sponsors = []
        while len(sponsors)<2:
            n = len(sponsors) + 1
            ui.announce(header="Need 2 sponsors..",
                        text=f"Enter sponsor #{n}:")
            sponsor = get_person()
            if sponsor:
                sponsors.append(sponsor)
        return sponsors

def create_person():
    """
    create an entry into the People table
    """
    keys = data.person_keys()
    mapping = {key: "" for key in keys}
    person = ui.entries(mapping,
        header="Adding New Person to People Table",
        text="Add values (or leave blank.. ")
    if person:
        data.put_person(person)
    return person

def enter_applicant():
    ui.announce(
        header="Enter Applicant (new Person)",
        text="Get sponsors 1st, then enter data...")
    sponsors = get_sponsors()
    sponsor1ID, sponsor2ID  = [sponsor["personID"]
                for sponsor in sponsors]
    applicant = create_person()  # creates db entry
    app_id = getID()
    ap_mapping = {"personID": app_id,
                  "sponsor1ID": sponsor1ID,
                  "sponsor2ID": sponsor2ID,
                  "app_rcvd": "",
                  "fee_rcvd": "",
                  "meeting1": "",
                  }
    ap_entry = ui.entries(ap_mapping,
        header="Applicant Dates",
        text="Add dates as appropriate, leave IDs")
    data.put_applicant(ap_entry)
    return applicant | ap_entry

def app_intro_letter(app_mapping):
    """
    Sets up an email to be sent to applicant
    and sponsors with bcc's to ...
    Use code/content.py as source for ap_rfc
    and ap_text
    """
    app_map = data.get_person(
                    app_mapping["personID"],
                    keys="first, last, email")
    print(f"app_intro_letter => {app_map}")
    query = f"""SELECT first, last, email
        FROM People WHERE
        personID = {app_mapping["personID"]}
    ;"""

def make_choice(listing):
    pass

def ck_get_person():
    person = get_person()
    for key, val in person.items():
        print(f"{key}: {val}")

def main():
    cmds_available = [
        get_person,
        get_sponsors,
        enter_applicant,
        ] 
    res = ui.choose(cmds_available)
    print(res())

if __name__ == "__main__":
    print("running code/logic.py")
#   ck_get_person()
    main()

