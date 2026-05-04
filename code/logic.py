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
    import letters
except ImportError:
    from code import letters
try:
    import data
except ImportError:
    from code import data
try:
    import content
except ImportError:
    from code import content
try:
    from code import helpers
except ImportError:
    import helpers
try:
    import data
except ImportError:
    from code import data
#print("logic.py: being imported (or run.)")

from code import cli as ui

ap_fee = 25
dues = 200


def getID():
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

def get_sponsors():
    """
    Returns a mapping of both sponsors
    with keys prefaced with "s1_" and "s2_"
    """
    while True:
        sponsors = []
        while len(sponsors)<2:
            data.announce(header="Need 2 sponsors..",
              text=f"Enter sponsor #{len(sponsors)+1}:")
            sponsor = get_person()
            if sponsor:
                sponsors.append(sponsor)
        for key, val in sponsors[0].items():
            ret0 = {f"s1_{key}": val for
                    key, val in sponsors[0].items()}
        for key, val in sponsors[1].items():
            k = f"s2_{key}"
            ret1 = {f"s2_{key}": val for
                    key, val in sponsors[1].items()}
        ret = ret0 | ret1
        res = dict(sorted(ret.items()))
        # emails provided by keys "s1_email" & "s2_email"
        return res

empty_dict = {}

def create_person(empty_dict):
    """
    Create an entry into the People table
    Return mapping with personID value.
    """
    keys = data.person_keys()
    mapping = {key: "" for key in keys}
    person = data.entries(mapping,
        header="Adding New Person to People Table",
        text="Add values (empty strings accepted)... ")
    if person:
        data.put_person(person)
        person["personID"] = getID()
    helpers.dump2json(person, "new_person_mapping.json")
    return person

def add_ap_fee(ap_mapping, fee=ap_fee):
    data.add_receipt(ap_mapping["personID"],
                     ap_mapping['fee_rcvd'],
                     ap_fee,
                     category="ap_fee")

def add_person_status(ap_mapping, statusID):
    data.set_person_status(ap_mapping["personID"],
           statusID,
           ap_mapping["fee_rcvd"])  # begin date

def add_sponsors(applicant):
    """
    Adds sponsor data to applicant mapping.
    Also adds first 3 date keys all /w empty values
    """
    sponsors = get_sponsors()
    ap_mapping = {  #"personID": applicant["personID"],
                  "s1_ID": sponsors["s1_personID"],  # not all
                  "s2_ID": sponsors["s2_personID"],  # of them.
                  "app_rcvd": "",
                  "fee_rcvd": "",
                  "meeting1": "",
                  }
    return applicant | ap_mapping

def add_dates(applicant):
    """Add up to first 3 Applicant date entries."""
    ap_mapping = data.add_info(applicant,
                "app_rcvd", "fee_rcvd", "meeting1",
                header="Applicant Dates",
                text="Add dates as appropriate:")
    return applicant | ap_mapping

def collect(func, mapping, f_name, header):
    """
    Choose between returning <func>(<mapping>) which is 
    json loaded into <f_name> or returning a mapping
    retrieved from <f_name>.
    """
    choice = ui.choose(
            ["Pick from file", "Collect info"],
            header=header)
    if choice == "Pick from file":
        return helpers.load_json_file(
                f_name)
    else: 
        ret = func(mapping)
        helpers.dump2json_file(ret, f_name)
        return ret

def applicant_mapping():
    """
    Returns a mapping of all info needed
    to create an applicant and create
    the appropriate acknolwdgement letter/email.
    Also makes entries into the People, Applicant,
    Person_Status and Receipts tables via sql module.
    <applicant>: data for People table plus personID
    <ap_mapping>:
    """
    ## create People table entry & return mapping...
    applicant = collect(create_person, {},
            "new_person_mapping.json",
            "Collect or Retrieve from JSON")
    ## add sponsors & dates to <applicant> mapping...
    applicant = collect(add_sponsors, applicant,
            "appl_w_sponsors.json",
            "Add sponsors or get from file?")
    applicant = collect(add_dates, applicant,
            "app_w_3dates.json",
            "Add 3 dates or get from file?")

redacted = '''
#######################
    data.put_applicant(ap_mapping)  # Applicant table entry
    ap_mapping = ap_mapping | applicant | sponsors
    fname = "final_ap_mapping.json"
    helpers.dump2json_file(ap_mapping, fname)
    ap_mapping = helpers.get_json(fname)

    ### Need to make entry into Person_Status table ###
    # Letters assigned as category is determined...
    if ap_mapping["meeting1"]:
        ap_mapping["letter"] = letters.letter_bodies[
                "app_with_1st_meeting"]
        #!!!#("send fee and 1st meeting letter,")
        add_person_status(ap_mapping, 4)
        add_ap_fee(ap_mapping)  # Receipts table entry
    elif ap_mapping["fee_rcvd"]:
        # need to send acknowledgement letter
        # status is 2 until acknowledgement is sent
        # setting status '3|a0|No meetings yet'...
        ap_mapping["letter"] = letters.letter_bodies[
                "new_applicant_welcome"]
        add_person_status(ap_mapping, 3)
        # adding to receipts...
        add_ap_fee(ap_mapping)  # Receipts table entry
    elif ap_mapping["app_rcvd"]:
        # letter re app but no fee received
        ap_mapping["letter"] = letters.letter_bodies[
                "app_fee_pending"]
        add_person_status(ap_mapping, 1)
    return ap_mapping
    '''

def get_applicant_table_entry(personID):
    return data.get_app_info(personID)

def update_applicant(id_=None):
    """
    Provides for addition of dates to Applicant table
    and Status table updates
    If not <id_>, calls get_person to get an ID
    Returns None if fails to find an applicant.
    """
    # first must pick an applicant...
    if not id_: id_ = 0
    ap_map = {"personID": id_,
              "first": "",
              "last": "",
              "suffix": "",
              }
    appl = data.entries(ap_map,
        header="Pick Applicant:by ID or clues",
        text="If ID unknown, add name clues.")
    id_ = appl["personID"]
    if not id_:  # use pick person to get an ID
        rec = get_person()
        id_ = rec["personID"]
    if not id_: return
    mapping = get_applicant_table_entry(id_)
    ret = {}
    keys = ["A_personID", "A_first", "A_last", "A_suffix",
        "AP_meeting1", "AP_meeting2", "AP_meeting3",
        "AP_approved", "AP_dues_paid", "AP_notified", ]
    date_keys = keys[4:]
    date_slot = None
    for date_key in date_keys:
        if not mapping[date_key]:
            key2fill = date_key.split('_')[1]
            break
    header=f"{mapping['A_first']} {mapping['A_last']}"
    if mapping["A_suffix"]:
        header = header + mapping["A_suffix"]
    text="Enter date (yyyymmdd)"

    d = {f"{key2fill}": "",  }
    ret = data.entries(d, header=header, text=text)
    data.add_date(mapping["A_personID"],
                key2fill, ret[f"{key2fill}"])
    # now need to update Person_Status table
    # key2fill relationship to status mapping:
    key_status_mapping = { # entry to update:
            "meeting1":     3,  # no meetngs yet
            "meeting2":     4,  # attended 1 meeting
            "meeting3":     5,  # attended 2 meeting
            "AP_approved":  6,  # attended 3 meeting
            "AP_dues_paid": 7,  # approved
            "AP_notified":  8,  # dues_paid
            }


def main():
    cmds_available = [
        get_person,
        get_sponsors,
        enter_applicant,
        update_applicant,
        ] 
    cmd = data.choose(cmds_available)  # may want to
        #  add default key word params header & text
    print()
    print(f"About to run {cmd.__name__} ...")
    res = cmd()
    print(f"Finished running {cmd.__name__} ==> ", end='')
    print(res)

def ck_get_person():
    ret = get_person()
    if ret:
        for key, value in ret.items():
            print(f"{key}: {value}")
    else:
        print(f"get_person returned {ret}")
    return ret

def ck_get_sponsors():
    for key, val in get_sponsors().items():
        print(f"{key}: {val}")

def ck_applicant_mapping():
    print("Running get_applicant.py")
    dest = "ck_app_entry.json"
    mapping = applicant_mapping()

    if mapping:
        with open(dest, 'w') as outf:
            json.dump(mapping, outf, indent=2)
        print("(Applicant) data dumped to "
                + f"{outf.name}")
        yn = input(
            "Print to screen as well? (yn): ")
        if yn and yn[0] in "yY":
            for key, val in mapping.items():
                print(f"{key}: {val}")
    else:
        print(f"applicant_mapping returned {mapping}")

if __name__ == "__main__":
    ck_applicant_mapping()
#   ck_get_sponsors()
#   print("running code/logic.py")
#   ck_get_person()
#   main()

