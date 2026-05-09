#!/usr/bin/env python3

# File: ~/Git/RBC/code/show.py

"""
Part of business logic ("C" of MCV).
Sister to logic.py file.
"""

try: import data
except ImportError: from code import data
try: import sql
except ImportError: from code import sql
try: import helpers
except ImportError: from code import helpers

mem_n_query = f"""
/*  File: Sql/count_ff.sql */
-- "1st yr" & "in good standing"
SELECT count(*) FROM Person_Status
WHERE statusID in (11, 15)
AND (begin = "" OR begin <= "{eightdigitdate}")
AND (end = "" OR end > "{eightdigitdate}")
; """

all_mem_query = f"""
-- "1st yr", "in good standing", "honorary",
-- "inactive" & "retiring"
SELECT P.personID, P.first, P.last, P.suffix, P.phone,
P.address, P.town, P.state, P.postal_code, P.email, 
S.statusID, S.text
FROM People as P,
     Stati as S,
     Person_Status as PS
WHERE S.statusID in (11, 15, 14,16,17)
AND PS.personID = P.personID
AND S.statusID = PS.statusID
/* 1st yr, in good standing, honorary, inactive, retiring */
AND (PS.begin = "" OR PS.begin <= "{eightdigitdate}")
AND (PS.end = "" OR PS.end > "{eightdigitdate}")
ORDER by P.last, P.first, P.suffix
;"""

def current_n():
    """
    returns the number of currently active members
    """
    res = sql.fetch(mem_n_query, from_file=False)
    return res[0][0]

def member_mappings():
    """
    Provides a listing of mappings of  all current members
    (including honorary, inactive and retiring.)
    """
    ret = sql.dicts_from_query(all_mem_query,
                from_file=False, replace_periods=True)
    return [mapping for mapping in ret]

def main():
#   n_members = current_n()
#   print(f"Membership stands at {n_members}")
    ret = member_mappings()
    keys = [key for key in ret[0].keys()]
    # ^ solves generator problem
    out_file = "all_membs.csv"
    with open(out_file, "w") as f:
        for mapping in ret:
            print([value for value in mapping.values()],
                  file=f)
    print(f"Data written to {out_file}")
    print("Keys are as follows:")
    print(keys)


if __name__ == "__main__":
    print("Running ~/Git/RBC/code show.py")
    main()
else:
    print("Importing ~/Git/RBC/code show.py")
