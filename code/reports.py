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


def applicant_listing(mappings):
    """
    provides a formatted with headers 'by number of meetings'
    listing of applicant data. Returns a list of lines.
    <mappings> come from applicant_mappings().
    """
    template = """
  [{P_personID:>3}], {P_first} {P_last} {P_suffix} {P_email} {P_phone}
     Sponsors: {S1_first} {S1_last} {S1_suffix}, {S2_first} {S2_last} {S2_suffix}  [{S1_personID}, {S2_personID}]
     Applied: {Ap_app_rcvd}  """
    add3 = "Meetings: {Ap_meeting1}, {Ap_meeting2}, {Ap_meeting3}"
    add2 = "Meetings: {Ap_meeting1}, {Ap_meeting2}"
    add1 = "Meeting date: {Ap_meeting1}"

    no_meetings = []; header0 = "No Meetings Yet"
    one_meeting = []; header1 = "Attended One Meeting"
    two_meetings = []; header2 = "Attended Two Meetings"
    three_meetings = []; header3 = "Attended Three Meetings"
    m3 = []; m2 = []; m1 = []; m0 = []
    apps = applicant_mappings()
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
    report = []
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
    return report


def applicant_report():
    """
    """
    mappings = applicant_mappings()
    date_line = f" as of {helpers.date}."
    report = [f"Applicants- currently {len(mappings)} in number"
              + date_line, ]
#   date_line = " " * (len(report[0])- len(date_line)) + date_line
#   report.append(date_line)
    report.append('=' * len(report[0]))
    report.append('')
    report.extend(applicant_listing(mappings))
    return report

def membership_report():
    report = []
    report.extend(applicant_report())
    report.extend(
        ['',
         "Respectfully submitted by...\n",
         "   Alex Kleider, Membership Chair,",
         "for presentation to the Executive Committee on {}"
         .format(helpers.next_first_friday(exclude=True)),
         "(or at their next meeting, which ever comes first.)",
         ])
    report.extend(
        ['',
         'PS Zoom ID: 527 109 8273; Password: 999620',
        ])
    return report

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

def ck_applicant_report():
    file_name = "applicant_report.txt"
    report = "\n".join(applicant_report())
    with open(file_name, 'w') as outf:
        outf.write(report)
    print(f"Applicant report sent to '{file_name}'")

def ck_membership_report():
    file_name = "membership_report.txt"
    report = "\n".join(membership_report())
    with open(file_name, 'w') as outf:
        outf.write(report)
    print(f"Membership report sent to '{file_name}'")

if __name__ == "__main__":
#   ck_limit_line_lengths()
    ck_membership_report()
    ck_applicant_report()
#   print("Running code/reports.py")
