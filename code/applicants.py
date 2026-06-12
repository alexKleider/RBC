#!/usr/bin/env python3

# File: code/applicants.py

"""
code/applicants.py and
code/people.py support logic.py
"""

try: import cli as ui
except ImportError: from code import cli as ui
try: import helpers
except ImportError: from code import helpers
try: import data
except ImportError: from code import data
try: import people
except ImportError: from code import people

app_letters = "app_letters.txt"  ## *
  ## * not yet used 

ap_fee = 25
key_status_mapping = { # entry to update:
        "app_rcvd":     1,
        "fee_rcvd":    #2,  # complete/not acknowledged
#       "no_meetings": 
                        3,  # no meetngs yet
        "meeting1":     4,  # attended 1 meeting
        "meeting2":     5,  # attended 2 meeting
        "meeting3":     6,  # attended 3 meeting
        "AP_approved":  7,  # approved
        "AP_dues_paid": 8,  # dues_paid
        "AP_notified":  9,  
        }
for_reference = '''
1|a-|Application received without fee
2|a|Application complete but not yet acknowledged
3|a0|No meetings yet
4|a1|Attended one meeting
5|a2|Attended two meetings
6|a3|Attended three (or more) meetings
7|ai|Inducted, needs to be notified
8|ad|Inducted & notified, membership pending payment of dues
9|av|Vacancy ready to be filled pending payment of dues
10|aw|Inducted & notified, awaiting vacancy
11|am|New Member
12|be|Email on record being rejected
13|ba|Postal address => mail returned
14|h|Honorary Member
15|m|Current Member
16|i|Inactive (continuing to receive minutes)
17|r|Retiring/Giving up Club Membership
18|t|Membership terminated (probably non payment of fees)
19|w|Fees being waived
20|z1_pres|President
21|z2_vp|VicePresident
22|z3_sec|Secretary
23|z4_treasurer|Treasurer
24|z5_d_odd|Director-odd yr
25|z6_d_even|Director-even yr
26|zae|Application expired or withdrawn
27|zzz|No longer a member
28|zzd|Deceased
29|mc|Membership Chair
30|com|Committee member
'''

def get_lastID():
    """
    Returns the last entered personID.
    Don't need a user interface version of this.
    """
    return data.get_highest_ID()

def get_sponsors():
    """
    Prompts for two People table records and
    returns a mapping including both with
    keys prefaced by "s1_" and "s2_"
    """
    while True:
        sponsors = []
        while len(sponsors)<2:
            data.announce(header="Need 2 sponsors..",
              text=f"Enter sponsor #{len(sponsors)+1}:")
            sponsor = get_person()
            if sponsor:
                pass
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

def add_sponsors(applicant):
    """
    Adds sponsor data to applicant mapping.
    Also adds first 3 date keys all /w empty values
    Does _not_ change the data base!
    """

    yn = input("Enter sponsor data (yY) or collect from file?: ")
    if not (yn and yn[0] in ("yY")): 
        return helpers.load_json_file("B_sponsors_incl.json")
    sponsors = get_sponsors()
    ap_mapping = {
          "s1_ID": sponsors["s1_personID"],
          "s1_first": sponsors["s1_first"],
          "s1_last": sponsors["s1_last"],
          "s1_suffix": sponsors["s1_suffix"],
          "s1_email": sponsors["s1_email"],
          "s2_ID": sponsors["s2_personID"],
          "s2_first": sponsors["s2_first"],
          "s2_last": sponsors["s2_last"],
          "s2_suffix": sponsors["s2_suffix"],
          "s2_email": sponsors["s2_email"],
          "app_rcvd": "",
          "fee_rcvd": "",
          "meeting1": "",
                  }
    ret = applicant | ap_mapping 
    helpers.dump2json(ret, "B_sponsors_incl.json")
    return ret

def add_dates(applicant):
    """
    Add 0-3 of the Applicant table date entries.
    and on basis of them adds "statusID" to mapping.
    Does _not_ change the data base!

    """
    ap_mapping = ui.add_info(applicant,
                "app_rcvd", "fee_rcvd", "meeting1",
                header="Applicant Dates",
                text="Add dates as appropriate:")
    if not (isinstance(applicant, dict) 
            and isinstance(ap_mapping, dict)):
        print("major problem in code/logic.add_dates")
        return
    for key in ("meeting1", "fee_rcvd", "app_rcvd"):
        if ap_mapping[key]:
            ap_mapping["statusID"] = key_status_mapping[key]
            ap_mapping["begin"] = ap_mapping[key]
#           if key == "fee_rcvd":
#               ap_mapping[] = 
            break
    if ap_mapping["fee_rcvd"]:
        ap_mapping["fee"] = ap_fee
    return applicant | ap_mapping

def add_letter(mapping):
    f"""
    Generate or add to text file <app_letters>.
    Mapping must contain data needed.
    Acknowledgements that application +/- fee
    have been received.
    """
    print(add_letter.__doc__)
    letters.append_letter(mapping)

def create_applicant_mapping():
    """
    Creates a Person table entry and returns a mapping
    which includes sponsors, applicable dates and
    receipts data as applicable but DOES NOT make any
    other table entries.
    """
    mapping = create_person()
    if not mapping: return
    mapping = add_sponsors(mapping)
    if not mapping: return
    mapping = add_dates(mapping)
    if not mapping: return
    return mapping

def load_applicant(mapping):
    """
    <mapping> contains all required applicant data.
    Applicant, Person_Status, +/- Receipts table entries.
    People table entry has already been done and key/value
    pairs assigned to <mapping>.
    """
#   for key, val in mapping.items():
#       print(f"{key}: {val}")
#   _ = input("mapping passed to code/logic.load_applicant")
    data.create_applicant_entry(mapping)
    data.create_person_status_entry(mapping)
    data.create_app_receipts_entry(mapping)
    add_letter(mapping)


def enter_applicant():
    mapping = people.create_person()
    mapping = add_sponsors(mapping)
    mapping = add_dates(mapping)
    load_applicant(mapping)
    add_letter(mapping)

def update_applicant(id_=None):
    """
    ### INCOMPLETE ###
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
    mapping = data.get_applicant(id_)
    ret = {}
    keys = ["A_personID", "A_first", "A_last", "A_suffix",
        "AP_meeting1", "AP_meeting2", "AP_meeting3",
        "AP_approved", "AP_dues_paid", "AP_notified", ]
    date_keys = keys[4:]
#   _ = input(f" date keys: {date_keys}")
#   _ = input(f" mapping: {mapping}")
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


if __name__ == "__main__":
    print("Running code/applicants.py")
