#!/usr/bin/env python3

# File: code/reports.py

"""
Functions in parallel with the logic module.
Here's where we generate reports.
"""
import helpers
import sql

linelengthlimit = 62

def limit_line_lengths(entry, linelengthlimit=linelengthlimit):
    """
    <entry> is text typically containing '\n' characters
    Returns the same but with long lines shortened.
    """
    ret = []
    for line in (entry.split("\n")):
        if len(line) > linelengthlimit:
            p1 = line[:linelengthlimit]
            p2 = line[linelengthlimit:]
            while p1[-1] != " ":
                p2 = p1[-1] + p2
                p1 = p1[:-1]
            ret.append(p1)
            ret.append((' ' * (linelengthlimit - len(p2)))+p2)
        else:
            ret.append(line)
    return "\n".join(ret)

def applicants():
    """
    """
    template = """
  [{P_personID:>3}], {P_first} {P_last} {P_suffix} {P_email} {P_phone}
     Sponsors: {S1_first} {S1_last} {S1_suffix}, {S2_first} {S2_last} {S2_suffix}  [{S1_personID}, {S2_personID}]
     Applied: {Ap_app_rcvd}  """
    add3 = "Meetings: {Ap_meeting1}, {Ap_meeting2}, {Ap_meeting3}"
    add2 = "Meetings: {Ap_meeting1}, {Ap_meeting2}"
    add1 = "Meeting date: {Ap_meeting1}"

    query = sql.import_query(
            "Sql/appl_dates_sponsors_f.sql")
    query = query.format(today=helpers.eightdigitdate)
    apps = sql.dicts_from_query(query, from_file=False,
                                replace_periods=True)
    apps = [mapping for mapping in apps]
    no_meetings = []; header0 = "No Meetings Yet"
    one_meeting = []; header1 = "Attended One Meeting"
    two_meetings = []; header2 = "Attended Two Meetings"
    three_meetings = []; header3 = "Attended Three Meetings"
    report = [f"Applicants- currently {len(apps)} in number", ]
    report.append('=' * len(report[0]))
    report.append('')
    m3 = []; m2 = []; m1 = []; m0 = []
    for map in apps:
        if map["Ap_meeting3"]:
            m3.append(map)
        elif map["Ap_meeting2"]:
            m2.append(map)
        elif map["Ap_meeting1"]:
            m1.append(map)
        elif map["Ap_meeting0"]:
            m0.append(map)
        else:
            _ = input("bypassed!!!")
    if m0:
        report.append(header0)
        report.append('-' * len(report[-1]))
        for d in m0:
            report.append(template.format(**d))
        report.append("")
    if m1:
        report.append(header1)
        report.append('-' * len(report[-1]))
        template1 = template + add1
        for d in m1:
            report.append(limit_line_lengths(
                template1.format(**d)))
        report.append("")
    if m2:
        report.append(header2)
        report.append('-' * len(report[-1]))
        template2 = template + add2
        for d in m2:
            report.append(limit_line_lengths(
                template2.format(**d)))
        report.append("")
    if m3:
        report.append(header3)
        report.append('-' * len(report[-1]))
        template3 = template + add3
        for d in m3:
            report.append(limit_line_lengths(
                template3.format(**d)))
        report.append("")
    return '\n'.join(report)

def forWeb():
    """
    """

def ck_limit_line_lengths():
    text = """Hello my friend, how is every things?
I'm planning to head south to British Columbia
late in June.
What are your plans for the summer of 2026?
"""
    print(f"{text}")
    print(limit_line_lengths(text, 35))

def ck_applicants():
    app_report = "applicant_report.txt"
    report = applicants()
    with open(app_report, 'w') as outf:
        outf.write(report)
    print(f"Applicant report sent to '{app_report}'")

if __name__ == "__main__":
#   ck_limit_line_lengths()
    ck_applicants()
#   print("Running code/reports.py")
