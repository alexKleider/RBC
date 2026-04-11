#!/usr/bin/env python3

# File: forJune.py

"""
Custom query for June who wants all member emails.

NOTE:
Must move this file down one directory to make import work
Plan might be to make this into a function and offer it as a main
menu option.
"""

from code import sql

outfile = "4june.txt"

def member_emails(outfile = outfile):
    query = """
    SELECT P.last, P.first, P.suffix, P.email
    FROM People as P
    JOIN Person_Status as S
    WHERE P.personID = S.personID
    AND NOT P.email = ""
    AND S.statusID in (11, 14,15, 16)
    AND S.begin < "20260407"
    AND (S.end = "" OR S.end > "20260407")
    ORDER BY P.last, P.first, P.suffix
    ;"""

    return sql.fetch(query, from_file=False)

if __name__ == "__main__":
    with open(outfile, "w") as f:
        for item in member_emails():
            print(item, file=f)
    print(f"Output send to {outfile}")
