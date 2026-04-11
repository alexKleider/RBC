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

partial_app_query = """
SELECT A.personID, A.first, A.last, A.suffix,
    A.email, A.phone, AP.app_rcvd, AP.fee_rcvd,
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
    WHERE A.personID = AP.personID
    AND   AP.sponsor1ID = sp1.personID
    AND   AP.sponsor2ID = sp2.personID
    AND   AP.notified = ""
    """
app_query_byID = (partial_app_query 
                + "    AND A.personID = {};")
all_app_query = partial_app_query + ';'

def get_app_info(id_):
    """ Retrieves a single applicant mapping
    specified by personID <id_> 
    Returns None if no such applicant found"""
    query = app_query_byID.format(id_)
    maps = sql.dicts_from_query(query,
                     replace_periods=True)
    mappings = [map_ for map_ in maps]
    if len(ret) == 1:
        mapping = ret[0]

def get_all_app_info():
    """ gets a list of mappings for all current applicants """
#   _ = input(all_app_query)
    ret = sql.dicts_from_query(all_app_query,
                     replace_periods=True)
    return ret

def ck_get_all_app_info():
    mappings = [map_ for map_ in get_all_app_info()]
    res = ["Applicants",]
    res.append("="*len(res[:-1]))
    for mg in mappings:
        listing = []
        line1 = "    [{A_personID:>3}] {A_first} {A_last}"
        if mg["A_suffix"]: line1 = line1 + "{A_suffix}"
        line1 = line1 + "  {A_email}"
        line1p = " {A_phone}"
        line = line1+line1p
        if len(line) > 70:
            line = line1 + line1e
            n = len(line)
            listing.append(line)
            listing.append(" "*(70-len(line)) + linep)
        else:
            listing.append(line)
        entry = '\n'.join(listing)
        _ = input(entry)
        text2add = entry.format(**mg)
        _ = input(text2add)
        listing.append("")


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

def ck_app_queries():
    query_w_ID = app_query_byID.format(250)  # single mapping
    _ = input(query_w_ID)
    all_app_query = partial_app_query + ";"  # mappings of...
                                            # ...all applicants
    _ = input(all_app_query)
    _ = input(len(all_app_query))

def show_all_app_info():
    """
    returns a listing of text: all current applicant data
    """
    all_info = get_all_app_info()
    mappings = [map_ for map_ in get_all_app_info()]
    # prepare a listing (ret) of lines:
    ret = []
    for mg in mappings:  # create a listing for each applicant:
        listing = []
        # arrange 1st line: possibly two lines...
        line1 = (
            "    [{A_personID:>3}] {A_first} {A_last}".format(**mg))
        if mg["A_suffix"]: line1 = line1 + "{A_suffix}".format(**mg)
        line = line1 + "  {A_email}".format(**mg)
        line_p = " {A_phone}".format(**mg)
        if (len(line)+len(line_p)) > 70:
            listing.append(line)
            listing.append(" "*(len(line)-len(line_p)) + line_p)
        else:
            listing.append(line + line_p)
        # sponsor line...
        line = "      sponsor line"
        listing.append(line)
        # meeting line...
        line = "      meeting line"
        listing.append(line)
        # possible approved line
        if True:
            line = "      possible approved line..."
            listing.append(line)
        listing.append("")
        ret.extend(listing)
    return ret

def ck_show_all_app_info():
    app_file = "applicants.txt"
    with open(app_file, "w") as f:
        header = "Applicants"
        print(header, file=f)
        print("="*len(header), file=f)
        f.write("\n".join(show_all_app_info()))
    print(f"Applicant data written to {app_file}")


if __name__ == "__main__":
    print("running code/data.py")
#   ck_get_app_info()
#   ck_app_queries()
    ck_show_all_app_info()
    pass
