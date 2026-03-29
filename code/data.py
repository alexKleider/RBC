#!/usr/bin/env python3

# File: code/data.py

"""
Provides interface to data base.
"Model" in MCV.
(Lowest level, so no imports from local code.)
"""

try:
    import sql
except ModuleNotFoundError:
    from code import sql
try:
    import misc
except ModuleNotFoundError:
    from code import misc

def getP_from_clues(mapping):
    """
    Based on <mapping> with incomplete entries
    for keys: first, last, suffix, describing a person
    Returns a (possibly empty) list of matching records
    or None (if no counditions speci.
    """
    first = mapping['first']
    last = mapping['last']
    suffix = mapping['suffix']
    conditions = []
    if first: conditions.append(f'first like "%{first}%"')
    if last: conditions.append(f'last like "%{last}%"')
    if suffix: conditions.append(f'suffix like "%{suffix}%"')
    if not conditions: return
    query = f"""
    SELECT personID, first, last, suffix FROM People
    WHERE {' AND '.join(conditions)}
    ;"""
    ret = sql.dicts_from_query(query, from_file=False)
#   print(query)
#   for mapping in ret: print(mapping)
    return ret

def get_person(personID, keys=None):
    """
    Get person info based on known <personID>.
    Returns values for <keys> specified
    (using format: "key1, key2, key3")
    or all values if not <keys>
    Fails if given a non valid <personID>.
    """
    if not keys: listing = "*"
    else: 
        ks = keys.split(", ")
        listing = []
        listing = [f"{k}" for k in ks]
        listing = ", ".join(listing)
    query = f"""SELECT {listing}
        FROM People WHERE
        personID = {personID}
        ;"""
#   print(query)
    ret = [res for res in sql.query2dict_listing(query)]
    if not ret:
#       ui.announce(header="Fatal problem!",
#           text="Must have entered an invalid personID!!")
        print("Must have entered an invalid personID!!")
        return
    if len(ret) > 1:
#       ui.announce(header="Fatal problem!",
#           text="get_person(id) should not return >1!!")
        print("get_person(id) should not return >1!!")
        return
    return ret[0]

def person_keys():
    """
    Returns the keys of the People table.
    """
    return sql.keys_from_schema("People", (1,0))

def put_person(mapping):
    keys = mapping.keys()
    k_listing = [ f'"{key}"' for key in keys]
    values = mapping.values()
    v_listing = [ f'"{value}"' for value in values]
#       for key, value in mapping.items():
#           print(f"{key}= {value}")
#   else:
#       print(f"{mapping=}")
    query = f"""
    INSERT INTO People
        ({", ".join(k_listing)}) 
    VALUES
        ({", ".join(v_listing)})
    ;
    """
#   print(
#       "data module ready to send the following query...")
#   print(query)
    sql.fetch(query, from_file=False, commit=True)

def put_applicant(mapping):
    """
    Adds record to Applicant table.
    <mapping> must contain the relevant key/value pairs.
    """
    query = f"""INSERT INTO Applicants (
        personID, sponsor1ID, sponsor2ID,
        app_rcvd, fee_rcvd, meeting1)
        VALUES (
        {mapping["personID"]},
        {mapping["sponsor1ID"]},
        {mapping["sponsor2ID"]},
        "{mapping["app_rcvd"]}",
        "{mapping["fee_rcvd"]}",
        "{mapping["meeting1"]}"
        ) ;"""
#   _ = input(query)
    sql.fetch(query, from_file=False, commit=True)

def get_highest_ID():
    """
    Gets the highest ID- that of the last entry.
    """
    query = """ SELECT personID FROM People
            ORDER BY personID DESC LIMIT 1;"""
    res = sql.fetch(query, from_file=False)
#   print(f"Highest personID is {res[0][0]}")
    return res[0][0]


def people_keys():
    pass

if __name__ == "__main__":
    print("running code/data.py")
    pass
