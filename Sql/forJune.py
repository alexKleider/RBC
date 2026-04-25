#!/usr/bin/env python3

# File: ~/Git/RBC/Sql/forJune.py

"""
Custom query for June who wants all member emails.
NOTE:
For imports to work must be call as follows...
>>> python3 -m Sql.forJune
"""

from code import sql
from code import helpers

outfile = "4june.txt"

def member_emails():
    query = f"""
    SELECT P.last, P.first, P.suffix, P.email
    FROM People as P
    JOIN Person_Status as S
    WHERE P.personID = S.personID
    AND NOT P.email = ""  -- exclude those without email
    AND S.statusID in (11, 14,15, 16)  -- only current members
--  AND S.begin < "20260407"  -- why this line????
    AND (S.end = "" OR S.end > "{helpers.eightdigitdate}")
    ORDER BY P.last, P.first, P.suffix
    ;"""

    return sql.fetch(query, from_file=False)

def listing2file(listing, outfile=outfile):
    with open(outfile, "w") as f:
        for item in listing:
            print(item, file=f)
    print(f"Output send to {outfile}")

def member_email_listing():
    listing2file(member_emails())


if __name__ == "__main__":
    member_email_listing()

