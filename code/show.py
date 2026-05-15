#!/usr/bin/env python3

# File: $RBC/code/show.py

"""
In parallel with code/reports.py both supporting logic.py
"""

import sys
import csv
try: import helpers, sql
except ImportError: from code import helpers, sql

today = helpers.eightdigitdate
file4web = f"4web{today}.txt"
file4app_report = f"applicants{today}.txt"
file4attrition = f"former_members{today}.txt"


def get_listing_2f(query_file):
    """
    Returns the result of a query that needs today's
    <helper.eightdigitdate> formatted twice.
    """
    date = today
    query = sql.import_query(query_file)
    query = query.format(date, date)
    return sql.fetch(query, from_file=False)


def modified_join_date(personID, status, jd):
    """
    Deals with special case of recent members (who where first
    year members for a year before becoming "members in good
    standing") and inactive and honorary members.
    Provides date of joining the club (when became new member)
    for people who have sinced become member in good standing.
    """
    # First deal with those who might have spent a year as
    # probatioinary members:
    if status == 15:
        res = sql.fetch(f"""SELECT begin, statusID
            FROM Person_Status
            WHERE personID = {personID}
            AND statusID = 11;""", from_file=False)
        if res:
            jd = res[0][0]
            return jd
    # Now deal with inactive and honorary members:
    if status in (14, 16):
#       print(f"dealing with memberID {personID}")
        res = sql.fetch(f"""SELECT begin, end
            FROM Person_Status WHERE
            personID = {personID} AND statusID = 15;""",
            from_file=False)
        if res:
            if res[0][0]:  # "begin" field may be empty (unknown)
                jd = res[0][0]
            else:
                jd = ''
    return jd


def get_numbers(listing, verbose=False):
    """
    Returns a 3 tuple:
        number of first year members
        number of members in good standing
        a tuple of strings constituting a report
    Client is show4web()
    """
    m0 = m1 = hon = inactive = 0
    for item in listing:
        status = item[9]
        if status == 11:
            m0 += 1
        elif status in {15, 17}:
            m1 += 1
        elif status == 14:
            hon += 1
        elif status == 16:
            inactive += 1
        else:
            _ = input(f"{repr(item)}")
            assert False, (
                "In show.py get_numbers: " +
                " member status must be 11 or 15!")

    report = (
            f"Total membership stands at {m0 + m1}",
            f"of whom {m1} are 'members in good standing' while",
            f"{m0} (indicated by an (*) asterix) are still",
             "within their first year of membership.",
             "Members indicated by a (^) caret have announced",
             "their intent to retire from the club.",
            f"Also listed are {hon} honorary members, indicated by an",
            f"'at' (@) sign and {inactive} inactive members, indicated by",
             "a percent (%) sign.",
            )
    if verbose:
        for line in report:
            print(line)
    return (m0, m1, report)

def create_membership_csv(listing):
    """
    creates memberlisting.csv
    """
    fieldnames = ( "first, last, suffix, phone, address, " +
            "town, state, postal_code, email, " +
            "statusID" ).split(', ')
    outcsvfile = "memberlisting.csv"
    with open(outcsvfile, 'w', newline='') as outf:
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        for item in listing:
            writer.writerow(helpers.make_dict(fieldnames,item))


def show4web(listing):
    """
    Deals with members only (not applicants!)
    <listing> list of lists: [10] is begin date
    which may need modification- see modified_join_date
    """
    m0, m1, member_report  = get_numbers(listing)
    report = ["""
FOR MEMBER USE ONLY

THE DEMOGRAPHIC DATA OF THE BOLINAS ROD & BOAT CLUB MEMBERSHIP
CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED FOR
ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BR&BC EXECUTIVE
COMMITTEE.
""",
    '\n'.join(member_report),
    f"\n(Last update: {helpers.date})", ]
    first_letter = '_'
    for item in listing:
        last_initial = item[1][:1]
        if last_initial != first_letter:
            first_letter = last_initial
            report.append("")
        status = item[9]
        if status == 15:   # Current Member
            prefix = ' '
        elif status == 11:  # New Member (1st year)
            prefix = '*'
        elif status == 17:   # Retiring
            prefix = '^'
        elif status == 14:   # Honorary member
            prefix = '@'
        elif status == 16:   # Inactive member
            prefix = '%'
        else:
            _ = input(f"Status: {status}")
            assert False, 'Status must be 11, 15, 17, 14 or 16!'
        personID = item[-1]
        # adjust date prn
        join_date = item[10]
        join_date = modified_join_date(personID, status, join_date)
        entry = str(prefix) + """{0} {1} {2} [{3}] [{8}]
\t{4}, {5}, {6} {7}""".format(*item)
        if join_date:
            entry = entry+" -joined: " + join_date
        report.append(entry)
    report.extend(["","", ])
    return report

newbyquery = """      -- > newbies --> newby_dict
    /* applicant data based on Applicant table */
    SELECT P.personID, P.first, P.last, P.suffix,
        P.phone, P.address, P.town, P.state, P.postal_code,
        P.country, P.email,
        A.sponsor1ID, P1.first, P1.last,
        A.sponsor2ID, P2.first, P2.last,
        A.app_rcvd, A.fee_rcvd, 
        A.meeting1, A.meeting2, A.meeting3,
        A.approved, A.dues_paid
    FROM Applicants AS A
    JOIN People AS P
    ON P.personID = A.personID
    JOIN People AS P1
    ON P1.personID = A.sponsor1ID
    JOIN People AS P2
    ON P2.personID = A.sponsor2ID
    WHERE A.notified = ""
    ORDER BY P.last, P.first
    ; """
byappstatusquery = f"""      -- > app_by_status
    /* applicant data based on Person_Status table, ordered
    by ID, last, first, suffix; also does consistency check.  */
    SELECT P.personID, P.first, P.last, P.suffix,
        PS.statusID, S.text
    FROM People as P
    JOIN Person_Status as PS ON PS.personID = P.personID
    JOIN Stati as S on S.statusID = PS.statusID
    WHERE (PS.begin = "" or PS.begin <= {today})
        AND (PS.end = "" or PS.end > {today})
        AND PS.statusID < 11
    ORDER BY PS.statusID, P.last, P.first, P.suffix
    ;"""

def show_newbie(mapping):
    """
    Assumes data came from newbyquery.
    """
    meetings = [mapping["A_meeting1"], mapping["A_meeting2"],
                mapping["A_meeting3"]]
    meetings = [meeting for meeting in meetings if meeting]
    ret = [
    """  {P_first} {P_last} {P_suffix}  {P_phone}  {P_email}
      {P_address}, {P_town}, {P_state}, {P_postal_code}
    Sponsors: {P1_first} {P1_last}, {P2_first} {P2_last}
    Applied {A_fee_rcvd}"""
           .format(**mapping), ]
    if meetings:
        ret.append("    Meetings: " +
                   ", ".join(meetings))
    if mapping["A_approved"]:
        ret.append(f'    Approved {mapping["A_approved"]}')
    return ret

def newby_dict():
    """ 
    Provides a dict keyed by personID and values are the dicts
    returned by <newbyquery> (taken from Applicant table.)
    """
    newbies = [newby for newby in 
               sql.dicts_from_query(newbyquery,
                                         replace_periods=True)]
    mapping = dict()
    for newby in newbies:
        key = newby["P_personID"]
        value = newby
        mapping[key] = value
    return mapping

def meetings(mapping):
    """
    Provides list of meeting dates based on <mapping> as
    derived from newbyquery; empty string if no meetings.
    """
    return ", ".join([date for date in [
                mapping['A_meeting1'],
                mapping['A_meeting2'],
                mapping['A_meeting3']  ] if date])



def applicant_report():
    app_by_status = [app for app in  # from Person_Status table
                        sql.dicts_from_query(byappstatusquery,
                                           replace_periods=True)]
    newbies = newby_dict()  # from Applicant table
    res = ["", f"Applicants- currently " + 
#       f"({helpers.eightdigitdate4filename}) " +
        f"{len(app_by_status)} in number",]
    res.append("=" * len(res[-1]))
    statusID = 0
    for a in app_by_status:
        id_ = a["P_personID"]
        newby = newbies[id_]
        if a["PS_statusID"] != statusID:
            res.append("")
            res.append(a["S_text"])
            res.append('-' * len(a["S_text"]))
            statusID = a["PS_statusID"]
        res.append(f"[{a['P_personID']:>4}] " +
                f"{newby['P_first']} {newby['P_last']}  " +
                f"{newby['P_email']} {newby['P_phone']} " )
        res.append(f'    Sponsors: ' +
            f'{newby["P1_first"]} {newby["P1_last"]}, ' +
            f'{newby["P2_first"]} {newby["P2_last"]}  ' + '[' +
            f'{newby["A_sponsor1ID"]}, ' +
            f'{newby["A_sponsor2ID"]}' + ']')
        dates = "Applied: "+ newby["A_app_rcvd"]
        m_dates = meetings(newby)
        if m_dates:
            if ", " in m_dates:
                dates = dates + "   Meetings: " + m_dates
            else:
                dates = dates + "   Meeting : " + m_dates
        res.append(f"    {dates}")
    res.extend(["", f"Report generated {helpers.date}.",])
    res.append("")
    return res


def show_applicants_cmd(report=None):
    helpers.add2report(report,
        "Entering code.show.show_applicants_cmd")
    ret = applicant_report()
    ans = input(
      f"Send applicant listing to {file4app_report}? (y/n) ")
    if ans and ans[0] in 'yY':
        with open(file4app_report, 'w') as outf:
            outf.write('\n'.join(ret))
        line = f"Applicant listing sent to {file4app_report}." 
        helpers.add2report(report, line)
        print(line)
    helpers.add2report(report,
        "...leaving code/show/show_applicants_cmd")
    return ret

def show_cmd(report=None):
    helpers.add2report(report,
            "Entering code.show.show_cmd", also_print=False)
    member_part = show4web(
            get_listing_2f("Sql/list4join_ff.sql"))
            # include honorary, inactive & retiring
    applicant_part = applicant_report()
    ret = member_part + applicant_part
    ans = input(f"Send data to {file4web}? (y/n) ")
    if ans and ans[0] in 'yY':
        with open(file4web, 'w') as outf:
            outf.write("\n".join(ret))
        line2add = f"Data sent to {file4web}."
        helpers.add2report(report, line2add, also_print=True)
        ret.append(line2add)
    helpers.add2report(report,
        "...leaving code/show/show_cmd")
    return ret


def former_members():
    """
    Returns a list of formatted strings showing
    IDs, names and emails
    of those currently in the following stati:
        18: 't'   Membership teminated
        27: 'zzz' No longer a member
        28: 'zzd' Died recently
    """
    query = """ SELECT 
            P.personID, PS.begin, P.first, P.last, P.suffix, P.email
        FROM people as P
        JOIN Person_Status as PS
        ON PS.personID = P.personID
        WHERE
            PS.statusID in (18, 27, 28)
        AND (PS.end = '' OR PS.end > {})
        AND (PS.begin = '' OR PS.begin < {})
        ORDER BY P.last, P.suffix, P.first
        ; """
    query = query.format(today,
                         today)
    res = sql.fetch(query, from_file=False)
    ret = []
    for entry in res:
        if entry[4]: entry[3] += entry[4]
        ret.append("{0:>3} {1:<8}{2:>10} {3:<13} {5:}".format(*entry))
    return ret


if __name__ == "__main__":
    file_name = "applicants.txt"
    with open(file_name, 'w') as outf:
        for line in applicant_report():
            outf.write(line + '\n')
    print(f"Applicant report written to {file_name}.")
