#!/usr/bin/env python3

# File: code/data.py

"""
Provides interface to data base via the sql.py module.
"Model" in MCV. ...hence the name "data"
(Lowest level, so no imports from local code
except helpers (to get eightdigit date which
is only used for testing.)
Uses sqlite2 via sql.py module.
"""

try:
    import cli as ui
except ImportError:
    from code import cli as ui
try:
    import sql
except ImportError:
    from code import sql
try:
    import helpers
except ImportError:
    from code import helpers


def announce(header="Note the following...",
             text="Announcing..."):
    return ui.announce(header=header, text=text)

def entries(mapping,
    header="Data Entry",
    text="Rtn to leave value as is, '_' to clear..."):
    return ui.entries(mapping=mapping, text=text)

def add_info(mapping, *keys,
        header="Add/change values (_ reverses changes)",
        text="Can only change some..."):
    """ ### already in UI Why is it here???? ### """
    return ui.add_info(mapping, *keys,
                header=header, text=text)

def choose(choices,
           header="Choose",
           text="(Select by number...)"):
    return ui.choose(choices,
           header="Choose",
           text="(Select by number...)")

def confirm_mapping(mapping,
            header="Confirmation Required",
            text="Accept mapping as above? (y/n): "):
    return ui.confirm_mapping(mapping=mapping,
                               text=text)


def yn(header="Confirmation Required",
       text="OK to proceed? (y/n"):
    return ui.yn(header=header, text=text)


def get_hints(header="People Table Lookup",
      text="Enter hints (no wild cards necessary.)"):
    """
    Returns a mapping of first, last, +/- suffix.
    """
    return ui.get_hints(header=header,
      text=text)

def get_mappings(which_type):
    queries = dict(
        applicants= ("Sql/appl_dates_sponsors_f.sql",
                     helpers.eightdigitdate),
        all_members = ("Sql/all_members_ff.sql",
                     helpers.eightdigitdate),
        leadership = ("Sql/leadership_f.sql",
                     helpers.eightdigitdate),
        expired = ("Sql/expired_ff.sql",
                     helpers.six_months_ago),
            )
    query = sql.import_query(queries[which_type][0])
    frmt = queries[which_type][1]
    query = query.format(today=frmt)
    res = sql.dicts_from_query(query, from_file=False,
                               replace_periods=True)
    return [mapping for mapping in res]

redact = '''
def applicant_mappings():
    """
    Uses the "Sql/appl_dates_sponsors_f.sql" query to
    retrieve a listing of applicant data mappings.
    """
    query = sql.import_query(
            "Sql/appl_dates_sponsors_f.sql")
    query = query.format(today=helpers.eightdigitdate)
    apps = sql.dicts_from_query(query, from_file=False,
                                replace_periods=True)

    return [mapping for mapping in apps] 
'''

def numbers(m_type):
    """
    <m_type> options: "in_good_standing", "first_yr",
    "honorary", "inactive", "retiring", "applicants"
    Each in turn calls the appropriate Sql file
    n_[]_ff.sql and returns the count.
    """
    day = helpers.eightdigitdate
    query_file = f"Sql/n_{m_type}_ff.sql"
    with open(query_file, 'r') as stream:
        query = stream.read().format(today=day)
    res = sql.fetch(query, from_file=False)
    return int(res[0][0])

def in_good_standing(personID):
    """
    Is person with <personID> a member in good standing?
    Returns True or False 
    """
    query = f""" SELECT statusID 
        FROM Person_Status
        WHERE personID = {personID}
        AND statusID = 15
        AND begin < "{helpers.eightdigitdate}"
        AND end = ""
        ; """
#   print(query)
    return sql.fetch(query, from_file=False)
    if res:
        return True
        print(f"{personID} in good standing")
        for line in res:
            print(line)
    else:
        print(f"{personID} not in good standing")

def ck_in_good_standing():
    for id_ in (100, 250):
        if in_good_standing(id_):
            print(f"{id_} in good standing")
        else:
            print(f"{id_} not in good standing")

def getP_from_clues(mapping):
    """
    Based on <mapping> with incomplete entries
    for keys: first, last, suffix, describing a person
    Returns a (possibly empty) list of matching records
    including email
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
    SELECT personID, first, last, suffix, email
    FROM People
    WHERE {' AND '.join(conditions)}
    ;"""
#   _ = input(f"Clues query is\n{query}")
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
        announce(
            "Must have entered an invalid personID!!")
        return
    if len(ret) > 1:
        announce(
            "get_person(id) should not return >1!!")
        return
    return ret[0]

def person_keys():
    """
    Returns all keys of the People table except ID.
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
    if ui.acceptable(query, header="Proposed Query:",
                     text="Run the above query? (y/n)"):
        sql.fetch(query, from_file=False, commit=True)
    else:print(f"Failed to insert {mapping}")

# create_% functions create database entries...

def create_applicant_entry(mapping):
    """ makes entry >> Applicant table"""
    query = f"""INSERT INTO Applicants (
        personID, sponsor1ID, sponsor2ID,
        app_rcvd, fee_rcvd, meeting1)
        VALUES (
        {mapping["personID"]},
        {mapping["s1_ID"]},
        {mapping["s2_ID"]},
        "{mapping["app_rcvd"]}",
        "{mapping["fee_rcvd"]}",
        "{mapping["meeting1"]}"
        ) ;"""
    if ui.acceptable(query, header="Proposed Query:",
                     text="Run the above query? (y/n)"):
        sql.fetch(query, from_file=False, commit=True)

def create_person_status_entry(ap_mapping):
    """
    Makes entry >> Person_Status table.
    Assumes ap_mapping has values for necessary keys.
    """
    query = f"""INSERT INTO Person_Status (
        personID, statusID, begin)
        VALUES (
        {ap_mapping["personID"]},
        {ap_mapping["statusID"]},
        {ap_mapping["begin"]}
        ) ;"""
    if ui.confirm_text(query):
        sql.fetch(query, from_file=False,
                       commit=True)

def create_app_receipts_entry(ap_mapping):
    """ makes entry >> Receipts table"""
    if not ap_mapping["fee_rcvd"]:
        return
    query = f"""INSERT INTO Receipts (
        personID, date_received, ap_fee, acknowledged)
        VALUES (
        {ap_mapping["personID"]},
        {ap_mapping["app_rcvd"]},
        {ap_mapping["fee"]},
        {ap_mapping["app_rcvd"]}
        ) ;"""
    if ui.confirm_text(query):
        sql.fetch(query, from_file=False,
                       commit=True)

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
#   print("In cli.add_date running:")
#   _ = input(query)
    sql.fetch(query, from_file=False, commit=True)

def set_person_status(personID, statusID, begin_date):
    query = f"""INSERT INTO Person_Status 
        (personID, statusID, begin) VALUES
        ({personID}, {statusID}, "{begin_date}");"""
#   _ = input(query)
    sql.fetch(query, from_file=False, commit=True)


def update_person_status(personID, old_status,
                         new_status, date):
    query = f"""UPDATE Person_Status SET end = {date}
            WHERE personID = {personID}
            AND statusID = {old_status};"""
#   _ = input(query)
    sql.fetch(query, from_file=False, commit=True)
    set_person_status(personID, new_status, date)

def add_letter(mapping):
    """
    """
    _ = input("Prepare letter_type in data.py")


def receipts_and_status_entries(applicant):
    """
    Pakes entries into both the Receipts and the
    Status tables as appropriate.
    """
    if applicant["fee_rcvd"]:
        add_receipt(applicant["personID"],
                    applicant["fee_rcvd"],
                    25, category="ap_fee")
    if applicant["meeting1"]:
        applicant["statusID"] = 4
        applicant["begin_date"] = applicant["meeting1"]
    elif applicant["fee_rcvd"]:
        applicant["begin_date"] = applicant["fee_rcvd"]
        applicant["statusID"] = 3
    else:  # application without fee!
        applicant["begin_date"] = applicant["app_rcvd"]
        applicant["statusID"] = 1
    set_person_status(applicant["personID"],
                      applicant["statusID"],
                      applicant["begin_date"])

def add_receipt(personID, date, amnt, category="ap_fee"):
    """
    Makes entry into Receipts table.
    <date> => both date_received & acknowledged fields
    so should be used in conjunction with sending of
    an acknowledgement email.
    """
    query = f"""INSERT INTO Receipts
    (personID, date_received, {category}, acknowledged)
    VALUES
    ({personID}, "{date}", {amnt}, "{date}"); """
#   print(query)
    sql.fetch(query, from_file=False, commit=True)

partial_app_query = """SELECT
        A.personID, A.first, A.last, A.suffix,
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

def ck_update_person_status():
    update_person_status(100, 3, 4, "20260422")

def ck_add_receipt():
    date = helpers.eightdigitdate
    add_receipt(310, date, 25, category="ap_fee")

def ck_numbers():
    for m_type in ("active", "first_yr",
                   "honorary", "inactive"):
        print(f"There are {data.numbers(m_type)} {m_type} members.")


if __name__ == "__main__":
    print("running code/data.py")
    ck_in_good_standing()
#   ck_add_receipt()
#   ck_update_person_status()
#   ck_get_app_info()
#   ck_app_queries()
#   ck_show_all_app_info()
