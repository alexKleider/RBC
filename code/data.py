#!/usr/bin/env python3

# File: code/data.py

"""
Provides interface to data base.
"Model" in MCV.
(Lowest level, so no imports from local code.)
Uses sqlite2 via sql.code module.
"""

try:
    import sql
except ImportError:
    from code import sql

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
    """
    Creates an entry in the data base (People table.)
    <mapping> must contain the relevant key/value pairs.
    """
    keys = mapping.keys()
    k_listing = [ f'"{key}"' for key in keys]
    values = mapping.values()
    v_listing = [ f'"{value}"' for value in values]
    query = f"""
    INSERT INTO People
        ({", ".join(k_listing)}) 
    VALUES
        ({", ".join(v_listing)})
    ;
    """
    sql.fetch(query, from_file=False, commit=True)

def put_applicant(mapping):
    """
    Creates an entry in the data base (Applicant table.)
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

def add_date(personID, date_key, date):
    """
    Adds specified <date> to specified <date_key>
    for <personID> in the Applicant table
    """
    query = f"""
        UPDATE Applicants SET
        {date_key} = "{date}"
        WHERE personID = {personID}
        ;"""
    print("In cli.add_date running:")
    _ = input(query)
    sql.fetch(query, from_file=False, commit=True)


def get_app_info(id_):
    query = f"""
    SELECT A.personID, A.first, A.last, A.suffix,
        A.email, AP.app_rcvd, AP.fee_rcvd,
        AP.meeting1, AP.meeting2, AP.meeting3,
        AP.approved, AP.dues_paid, AP.notified,
        sp1.personID, sp1.first, sp1.last,
            sp1.suffix, sp1.email,
        sp2.personID, sp2.first, sp2.last,
            sp2.suffix, sp2.email
    FROM Applicants AS AP,
             People AS A,
             People AS sp1,
             People AS sp2
        WHERE A.personID = {id_}
        AND A.personID = AP.personID
        AND   AP.sponsor1ID = sp1.personID
        AND   AP.sponsor2ID = sp2.personID
        ;"""
    maps = sql.dicts_from_query(query,
                     replace_periods=True)
    mappings = [map_ for map_ in maps]
    if mappings:  # if not, returns None
        return mappings[0]

def update_applicant(mapping):
    pass

def get_highest_ID():
    """
    Gets the highest ID- that of the last People table entry.
    """
    query = """ SELECT personID FROM People
            ORDER BY personID DESC LIMIT 1;"""
    res = sql.fetch(query, from_file=False)
    return res[0][0]

def ck_get_app_info():
    mapping = get_app_info(249)
    if mapping:
        for key, value in mapping.items():
            print(f"{key}: {value}")
    else:
        print("?Aborted?")

if __name__ == "__main__":
    print("running code/data.py")
    ck_get_app_info()
    pass
