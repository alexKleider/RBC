#!/usr/bin/env python3

# File: ck_contacts.py

"""
Routine(s) to check the Google contacts.csv file.
For reasons that aren't clear, Scott Kallsen
does have a label but "doesn't"!!
"""

import csv

g_csv = "/home/alex/Git/RBC/Data/contacts.csv"

def g_contacts():
    """
    Reads the gmail contacts.csv file and returns
    the data we want: first, last, suffix, email
    and labels. Does _not_ include those with no
    label.
    """
    useful = []
    with open(g_csv,'r') as f:
        g_reader = csv.DictReader(f)
#       print('DictReading Google contacts file "{}"...'
#           .format(f.name))
        n = 0
        for g_rec in g_reader:
            n += 1
            labels = set(
                g_rec["Labels"].split( " ::: ")[:-1])
            if not labels: continue  #ignore
            if "Retired" in labels:  # still a member
                labels = (
                    labels - {"Retired"}) | {"LIST"}
            rec = dict(
                first = g_rec["First Name"],
                last = g_rec["Last Name"],
                suffix = g_rec["Name Suffix"],
                g_email= g_rec["E-mail 1 - Value"],
                groups=labels,
                )
            useful.append(rec)
    return useful

if __name__ == "__main__":
    print("Running ck_contacts.py")
    contacts = g_contacts()
    n = 0
    for m in contacts:
        print(
#       "{first} {last} {g_email} {groups}".format(**m))
        "{groups}".format(**m))
        n += 1
        if n % 27 == 0:
            _ = input(f"{n%27=}")

