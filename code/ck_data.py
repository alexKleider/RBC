#!/usr/bin/env python3

# File: code/ck_data.py

"""
Provides ck_data.consistency_report (for menu.py.)
Functions:
    def g_contacts():
    def g_filter(g_dict, set2include):
    def g_data_parts(data):
    def s_data_parts(stati2include=None,
                        restriction=False):
    def s_data_parts(stati2include=None,
                        restriction=False):
    def compare(g_data, label, which_stati, report):
    def ck_m_vs_g_data(report=None):
    def ck_appl_vs_status_tables():
    def ck_members_vs_dues(report=None):
    def mooring_dock():   # can redact??
    def consistency_report(report=None):
    def ck_stati_vs_labels():  work_in_progress
    def get_kayak_listing():
    def check_g_contacts():
    def check_m_data():
    def check_g_data_parts():
    def check_consistency_report():

Module to check for data consistency, specifically:
    1. everyone with an email is in the google data base
    2. google data "labels"/contacts match
    sql Person_Status table:
        applicant == statiID 1..10
        dropped   also GaveUpMembership  26, 27, 28
        DockUsers
        GaveUpMembership   also dropped  26, 27, 28
        inactive
        Kayak
        LIST == members (stati 11, 15 & 17)
        Moorings
        Officers == statiID 20..25:  z[123456]* 
        Outer Basin Moorers
        secretary
        Committee  = statusID 30 & 29 (Membership)
            26|zae|Application expired or withdrawn
            27|zzz|No longer a member
            28|zzd|Deceased
    3.
    4.
"""

import os
import sys
import csv
import json

try: from code import helpers
except ImportError: import helpers
try: from code import sql
except ImportError: import sql

g_csv = "/home/alex/Git/RBC/Data/contacts.csv"

##  ^^ the gmail contacts.csv file.

# The following queries are for comparison with Google
# contacts 'Labels' i.e. those without email are excluded
# since they wouldn't be amongst google contacts.
queries = dict( # indexed by google contacts LABELs.
    # We've no intention of accepting applicants without email!
    applicant="""SELECT P.first, P.last, P.suffix
        FROM people as P
        JOIN Applicants as A
        WHERE A.personID = P.personID
            AND A.notified = ''
            AND NOT P.email = ''
            -- excludes those that are no longer applicants
        ;""",
    GaveUpMembership="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (27, 28)
                AND (PS.end = '' OR PS.end > {})
                AND NOT P.email = ''
            -- Terminated, No longer a member
            ; """.format(helpers.eightdigitdate),
    # Unlikely we'll accept inactive status
    # for someone without email...
    inactive="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 16
                AND (PS.end = '' OR PS.end > {})
                AND NOT P.email = ''
            ;""".format(helpers.eightdigitdate),
    LIST="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (11, 15, 17)
                AND NOT P.email = ''
                AND (PS.end = '' OR PS.end > {})
                AND (PS.begin = '' OR PS.begin <= {})
            ;""".format(helpers.eightdigitdate,
                        helpers.eightdigitdate),
    Officers="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
              AND PS.statusID IN (20, 21, 22, 23, 24, 25, 29)
              AND (PS.end = '' OR PS.end > {})
            ;""".format(helpers.eightdigitdate),
    secretary="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 22
                AND (PS.end = '' OR PS.end > {})
            ;""".format(helpers.eightdigitdate),
    Committee="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID = 30
                AND (PS.end = '' OR PS.end > {})
            ;""".format(helpers.eightdigitdate),
    dropped="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND PS.statusID in (18, 26)
                AND (PS.end = '' OR PS.end > {})
                AND NOT P.email = ''
            ;""".format(helpers.eightdigitdate),
    DockUsers="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Dock_Privileges as DP
            WHERE P.personID = DP.personID
                AND NOT P.email = ''
            ;""",
    Kayak="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Kayak_Slots as KS
            WHERE P.personID = KS.personID
                AND NOT P.email = ''
            ;""",
    Moorings="""SELECT P.first, P.last, P.suffix
            FROM people as P
            JOIN Moorings as M
            WHERE P.personID = M.personID
                AND NOT P.email = ''
            ;""",
    )

for_later = '''
queries['Outer Basin_Moorers -2023'] = """
            SELECT P.first, P.last, P.suffix
            FROM people as P
            """
'''

dock_query = """SELECT P.personID, P.first, P.last, P.suffix
            FROM people as P
            JOIN Dock_Privileges as DP
            WHERE P.personID = DP.personID ;"""
kayak_query = """SELECT K.slot_code, K.slot_cost, P.personID,
                        P.first, P.last, P.suffix
            FROM people as P
            JOIN Kayak_Slots as K
            WHERE P.personID = K.personID
            ORDER by P.last, P.first;"""
mooring_query = """SELECT P.personID, P.first, P.last, P.suffix
            FROM people as P
            JOIN Moorings as M
            WHERE P.personID = M.personID ;"""
members4dues = """SELECT P.personID  -- must get rid
            FROM people as P         -- of retirees!
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND (PS.statusID in (11, 15)
                    AND (PS.end = '' OR PS.end > {})
                    AND (PS.begin = '' OR PS.begin <= {}))
            ORDER BY P.personID
            ;""".format(helpers.eightdigitdate,
                        helpers.eightdigitdate) 
retirees =  """SELECT P.personID
            FROM people as P
            JOIN Person_Status as PS
            WHERE PS.personID = P.personID
                AND (PS.statusID = 17   -- retiring
                    AND (PS.end = '' OR PS.end > {})
                    AND (PS.begin = '' OR PS.begin <= {}))
            ORDER BY P.personID
            ;""".format(helpers.eightdigitdate,
                        helpers.eightdigitdate) 
dues_listing = """SELECT personID from Dues
            ORDER by personID;"""

def g_contacts():
    """
    Reads the gmail contacts.csv file and returns the
    data as a list of dicts each with values for:
    first, last, suffix, email and labels.
    !! Does _not_ include those with no label. !!
    (Limits the data and uses more succinct keys.)
    """
    contacts = []
    with open(g_csv,'r') as f:
        g_reader = csv.DictReader(f)
#       print('DictReading Google contacts file "{}"...'
#           .format(f.name))
        n = 0
        for g_rec in g_reader:
            n += 1
            labels = set(
                g_rec["Labels"].split( " ::: ")[:-1])
            if not labels: continue  # ignore
            if "Retired" in labels:  # still a member
                labels = (
                    labels - {"Retired"}) | {"LIST"}
            rec = dict(
                first = g_rec["First Name"],
                last = g_rec["Last Name"],
                suffix = g_rec["Name Suffix"],
                g_email= g_rec["E-mail 1 - Value"],
                groups=set(labels),
                )
            contacts.append(rec)
    return contacts

def g_filter(g_dict, set2include):
    """
    Returns g_dict without entries that don't include
    any of the groups listed in set2include.
    """
    ret = []
    for mapping in g_dict:
        if set2include & mapping['groups']:
            ret.append(mapping)
    return ret


def g_data_parts(data):
    """
    <data> is a list of dicts generated by g_contacts()
    (possibly modified by g_filter().)
    Returns a dict keyed by 'parts' as follows:jj
        "name_w_gmail": a set
        "groups_by_name": dict keyed by name => groups
        "names_by_group": dict keyed by group => names
    ... see first 4 lines of code
    Serves to compare sql data and google contacts data.
    """
    # set up the three components to be returned...
    ret = {}
    ret['name_w_gmail'] = set() #strings (names and email)
    ret['groups_by_name'] = dict() # set of groups by name
    ret['names_by_group'] = dict() # set of names by group
#   for key in ret.keys():
#       print(type(ret[key]))
#   _ = input()
    data = g_contacts()
    # process the g_data => the components...
    for mapping in data:  # 
        # First set up the name key...
        name_key = "{last}, {first}".format(**mapping)
        if mapping['suffix']:
            name_key = name_key + " " + mapping['suffix']
            # sql db suffixes are prepended with " "
        # add a string consisting of name and email
        ret['name_w_gmail'].add( # a str to the set
                name_key + ": " + mapping['g_email'])
        # add group listing for each person...
        # add 
        ret['groups_by_name'][name_key
                    ] = mapping['groups']
        # set up dicts keyed by group names and
        # add name to appropriate group(s)...
        for group in mapping["groups"]:
            _ = ret['names_by_group'].setdefault(group,
                                                set())
            ret['names_by_group'][group].add(name_key)
#           _ = input(f"added {name_key} to {group}")
    return ret

# stati2include possibilities:
applicants_and_members = (3,4,5,6,7,8,9,10,11,14,15,16)

# restriction possibilities:
not_email_restriction = " NOT email = '' "

def s_data_parts(stati2include=None,
                        restriction=False):
    """
    An SQL JOIN on People & Person_Status tables
    is used to select stati (all if not <stati2include>)
    restricted by ON clauses if provided by <restriction>.

    Collects data from the sql data base returning
    three dicts (similar to <g_data_parts()>)
    Output can be restricted as follows:
    <stati2include> (an iterable of integers/statusIDs)
    if provided can limit what's returned.
    <restriction> can be an optional clause to restrict
    what is returned by the query. 
    """
    if not stati2include:
        stati_line = ""
    else:
        stati_line = f"AND PS.statusID in {stati2include}"
    if not restriction: restrict_line = ""
    else: restrict_line = f"AND {restriction}"
    # Mustn't use f"""...""" if use """...""".format()
    print(f"restrict line is '{restrict_line}'")
    query = """
    SELECT P.personID, P.last, P.first, P.suffix, P.email,
        PS.statusID, PS.end
    FROM People as P
    JOIN Person_Status as PS 
    ON  (PS.personID = P.personID
         {stati_line})
         -- +/- AND PS.statusID in ...
    WHERE PS.end > {date} or PS.end = ''
        {restriction}
    ; """.format(**{"stati_line": stati_line,
                  "date": helpers.eightdigitdate,
                  "restriction": restrict_line})
#   stati = ''
#   if stati2include:
#       listing = ','.join([repr(s) for s in stati2include])
#       stati = f"""PS.statusID in ({listing}) 
#               AND
#               """
    ret = {}  # member data
    ret['name_w_email'] = set()  # => strings (names and email)
    ret['stati_by_name'] = dict()  # => set of stati
    ret['names_by_status'] = dict()  # >set of names

    keys = "ID, last, first, suffix, email, status, end".split(', ')
    _ = input(f"query: {query}")
    res = sql.query2dict_listing(query,
                            keys, from_file=False)
    with open("2ck.txt", 'w') as f:
         print(res, file=f)
         _ = input(f"check file: {f.name}")
    for d in res:
        name_key = "{last}, {first}".format(**d)
        if d['suffix']:
            name_key = name_key + d['suffix']
        ret['name_w_email'].add(
                name_key + ": " + d['email'])
    return ret


def compare(g_data, label, which_stati, report):
    """
    <g_data> is customized version of contacts.csv data.
    <label> 
    """
    # First check that all 'labels' exist...
    label_names = set(g_data['names_by_group'].keys())
    if not label in label_names:
        report.append(
            f"!!'{label}' not in {repr(label_names)}!!")
        return
    if label == "Outer_Basin_Moorers_2023":
        report.append(
            f"!!not dealing with '{label}'!!")
        return
    # ... passed the check
    res = sql.fetch(queries[label],
                        from_file=False)
    set_members = set([f"{a[1]}, {a[0]}{a[2]}" for
                    a in res])
    if not (set_members ==
            g_data['names_by_group'][label]):
        report.append(
            f"...{label} group doesn't match {which_stati}")
        report.extend(helpers.check_sets(set_members, 
                            g_data['names_by_group'][label]))
    else:
        report.append(
            f"...{label} group matches {which_stati}")


def ck_m_vs_g_data(report=None):
    """
    Compares member (including applicant) data
    for consistency between sql db and gmail contacts
    (including stati/labels as appropriate.)
    (Excludes those without emails: not in gmail data)
    """
    if not report: report = []
    report.append(
        "Checking for gmail and sql db consistency...")
    g_data = g_filter(g_contacts(),
                {"LIST", "applicant", "inactive"})
    m_data = s_data_parts(
                stati2include=applicants_and_members,
                restriction=not_email_restriction)
    # check that names and emails match:
    g_parts = g_data_parts(g_data)
    if g_parts['name_w_gmail'] != m_data['name_w_email']:
        print(report[-1])
        report.extend(['',
        "Gmail and People table emails don't match!..."])
        report.extend(helpers.check_sets(
            g_parts['name_w_gmail'],
            m_data['name_w_email'],
            header_in1st_not2nd=
                "Entries in Gmail not in sql db:",
            header_in2nd_not1st=
                "Entries in sql db not in Gmail:"))
        report.append("-"*50)
    else:
        report.append("...emails consistent")
    # check that Labels/groups match stati..
    # need to lift restrictions to include all
    # (not just members and applicants!)
    g_data = g_data_parts(g_contacts())
    m_data = s_data_parts(
                restriction = not_email_restriction)
    # Applicants/applicant:
    compare(g_data, 'applicant', 'applicant_stati', report)
    # Members/LIST:
    compare(g_data, 'LIST', 'member_stati', report)
#   # Members/Retired:
#   compare(g_data, 'Retired', 'retired_stati', report)
    # Committee
    compare(g_data, 'Committee', 'comittee_stati', report)
    # DockUsers
#   compare(g_data, 'DockUsers', 'dock_user_stati', report)
    # dropped
    compare(g_data, 'dropped', 'dropped_stati', report)
    # GaveUpMembership
    compare(g_data, 'GaveUpMembership', 'quit_stati', report)
    # inactive
    compare(g_data, 'inactive', 'inactive_stati', report)
    # Kayak
#   compare(g_data, 'Kayak', 'kayak_stati', report)
    # Moorings
#   compare(g_data, 'Moorings', 'moorings_stati', report)
    # Officers
    compare(g_data, 'Officers', 'officers_stati', report)
    # Outer_Basin_Moorers_2023
#   compare(g_data, 'Outer_Basin_Moorers_2023',
#                           'outer_moorings_stati', report)
    # secretary
    compare(g_data, 'secretary', 'secretary_stati', report)
    report.append("...end of gmail vs SQL consistency check")
    return report


def ck_appl_vs_status_tables():
    """
    Compares Applicants and Stati tables for consistency.
    Sql/aS.sql queries get info from Applicant table
    Sql/sS.sql queries get info from Status table
    "S" can be one of the following: 0, 1, 2, 3, d
    """
    fs = "{:0} {:1}, {:2}{:3}"
    report = []
    report.append(
        "Checking Applicant and Stati table consistency...")
    res_app_table = sql.fetch(
            "Sql/still_applicants.sql")
    res_app = [fs.format(*entry) for entry in res_app_table]
    res_status_table = sql.fetch(
            "Sql/applicants_from_stati.sql")
    res_status =  [fs.format(*entry) for entry in
                                        res_status_table]
    if res_app != res_status:
        report.extend(helpers.check_sets(
                set(res_app), set(res_status)))
    query_pairs = (
                ('Sql/a0-.sql', 'Sql/s0-.sql', ),
                ('Sql/a0.sql', 'Sql/s0.sql', ),
                ('Sql/a1.sql', 'Sql/s1.sql', ),
                ('Sql/a2.sql', 'Sql/s2.sql', ),
                ('Sql/a3.sql', 'Sql/s3.sql', ),
                ('Sql/ad.sql', 'Sql/sd.sql', ),
            )
    ok = True
    for a_query, s_query in query_pairs:
#   for n in range(len(queries)):
        res_a = sql.fetch(a_query)
        res_s = sql.fetch(s_query)
        if res_a != res_s:
            ok = False
            report.append(
                "Applicant and Person_Status table missmatch!")
            print(f"res_a: {res_a}")
            res_a = [' '.join(str(item)) for item in res_a]
            print(f"res_s: {res_s}")
            res_s = [' '.join(str(item)) for item in res_s]
            report.extend(helpers.check_sets(
                set(res_a), set(res_s),
                header_in1st_not2nd=
                f"in {a_query}, not {s_query}"))
#   if not ok:
#       report.append("Problems")
    report.append("... App/Stati consistency check done.")
    return report

def ck_members_vs_dues(report=None):
    if not report: report = []
    resa = sql.fetch(members4dues, from_file=False)
    resb = sql.fetch(retirees, from_file=False)
    sa = set([item[0] for item in resa])
    sb = set([item[0] for item in resb])
    s1 = sa - sb
    res2 = sql.fetch(dues_listing, from_file=False)
    s2 = set([item[0] for item in res2])
    if s1 != s2:
        report.append(
            "Member listing and Dues table missmatch:")
        report.append(
            f"In members not dues: {repr(sorted(s1-s2))}")
        for pID in s1 - s2:
            report.append(
                f"{sql.get_rec_by_ID(pID).values()}")
        report.append(
            f"In dues not members: {repr(sorted(s2-s1))}")
        for pID in s2 - s1:
            report.append(
                f"{sql.get_rec_by_ID(pID).values()}")
    else:
        report.append(
            "Member listing and Dues table correspond.")
    return report

def mooring_dock():   # can redact??
    """
    Ensure that no one is charged for both mooring & dock usage.
    """
    report = []
    keys = "personID, first, last, suffix".split(', ')
    mooring = sql.fetch(mooring_query,from_file=False)
    dock = sql.fetch(dock_query,from_file=False)
    for res in [mooring, dock]:
        listing = []
        for item in res:
            d = helpers.make_dict(keys, item)
            if d['suffix']:
                d['last'] = (d['last'] + '_' +
                        d['suffix'].strip())
            listing.append(f"{d['last']},{d['first']}")
#       res = set(listing)
#   print(f"{mooring}")
#   print(f"{dock}")
    empty = set(mooring) & set(dock)
    if empty:
        report.append(
          "The following are common to both mooring and dock:")
        report.append(empty)
    else:
        report.append("No mooring & dock overlap.")
    return report



def consistency_report(report=None):
    """
    Adds info to and then returns <report>.
    Called by menu.py under Reports/check_data_consistency
    """
    if not report:
        report = []
    report.extend(ck_m_vs_g_data())
    report.extend(ck_appl_vs_status_tables())
#   report.extend(mooring_dock())
    report.extend(ck_members_vs_dues())
    return report


def ck_stati_vs_labels():
    """
    Still a work in progress
    """
    contact_data = g_data_parts(g_contacts())
    groups_by_name = contact_data['groups_by_name']
    sql_data = s_data_parts()
    stati_by_name = sql_data['stati_by_name']
    print(f"stati_by_name: {stati_by_name}")

def get_kayak_listing():
    ret = sql.fetch(kayak_query, from_file=False)
    ret = sorted(ret)
    for entry in ret:
        print(f"    {entry[4]}, {entry[3]}")

def check_g_contacts():
    print("Running check_g_contacts.py")
    contacts = g_contacts()
    n = 0
    for m in contacts:
        print(
        "{first} {last} {g_email} {groups}".format(**m))
#       "{groups}".format(**m))
        n += 1
        if n % 27 == 0:
            _ = input(f"{n%27=}")


def check_m_data():
    m_data = s_data_parts(
                stati2include=applicants_and_members,
                restriction=not_email_restriction)
    with open("m_data", 'w') as f:
        for key in m_data.keys():
            print(f"{key}", file=f)
            for item in m_data[key]:
                print(f"\t{item}", file=f)
        print(f"Data written to {f.name}")


def check_g_data_parts():
    data = g_data_parts(g_contacts())
    for key, val in data.items():
        print(f"\n{key}")
        print("=" * len(key))
        print(type(val))
        if isinstance(val, dict):
            for k, v in val.items():
                line = f"{k}: {v}"
                print(line)
        elif isinstance(val, set):
            for item in val:
                line = str(val)
                print(line)
                if len(line) > 75:
                    print()


def check_consistency_report():
    print("Generating consistency report...")
    report = "consistency_report.txt"
    with open(report, 'w') as f:
        for line in consistency_report([
                    "Consistency Report",
                    "=================="]): 
            print(line, file=f)
        print(f"Consistency report sent to {f.name}")

if __name__ == '__main__':
    check_g_data_parts()
#   ck_stati_vs_labels()
#   check_m_data()
#   check_consistency_report()

