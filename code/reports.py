#!/usr/bin/env python3

# File: code/reports.py

"""
Functions in parallel with the logic module.
Here's where we generate reports.
Provides the following:
    _limit_line_lengths, _header4, 
    applicant_listing, applicant_report
    member_listing,
    exec_report,
    forWeb
#
The _mapping() functions moved into data.py

Possible m_types:
    "active", "first_yr", "honorary", "inactive"
"""
import helpers
import data

linelengthlimit = 62

keys = """
SELECT
    P.personID, PS.statusID,
    P.first, P.last, P.suffix, P.email, P.address,
    P.town, P.state, P.postal_code, P.phone
"""

def _limit_line_lengths(entry, linelengthlimit=linelengthlimit):
    """
    <entry> is text typically containing '\n' characters
    Lines (between '\n' chars) are limited to <linelengthlimit>
    (word boundies respected) with the removed part, right
    justified on a following line.
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

def applicant_listing(mappings):
    """
    Returns a formatted, with 'by # of meetings' headers,
    listing of applicant data (a list of lines.)
   <mappings> come from data.applicant_mappings().
    """
    # set up the template for each applicant entry...
    template = """
  [{P_personID:>3}], {P_first} {P_last} {P_suffix} {P_email} {P_phone}
     Sponsors: {S1_first} {S1_last} {S1_suffix}, {S2_first} {S2_last} {S2_suffix}  [{S1_personID}, {S2_personID}]
     Applied: {Ap_app_rcvd}  """
    # last line of template will depend on # of meetings...
    add3 = "Meetings: {Ap_meeting1}, {Ap_meeting2}, {Ap_meeting3}"
    add2 = "Meetings: {Ap_meeting1}, {Ap_meeting2}"
    add1 = "Meeting date: {Ap_meeting1}"
    # collectors & headers for each type (by # of meetings)
    no_meetings = []; header0 = "No Meetings Yet"
    one_meeting = []; header1 = "Attended One Meeting"
    two_meetings = []; header2 = "Attended Two Meetings"
    three_meetings = []; header3 = "Attended Three Meetings"
    m3 = []; m2 = []; m1 = []; m0 = []
    # use query to get the mappings...
#   apps = data.applicant_mappings()
    apps = data.get_mappings("applicants")
    # separate mappings into "by meeting" listings...
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
    # assemble the report...
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
            report.append(_limit_line_lengths(
                template1.format(**d)))
        report.append("")
    if m2:
        report.append(header2)
        report.append('-' * len(report[-1]))
        template2 = template + add2
        for d in m2:
            report.append(_limit_line_lengths(
                template2.format(**d)))
        report.append("")
    if m3:
        report.append(header3)
        report.append('-' * len(report[-1]))
        template3 = template + add3
        for d in m3:
            report.append(_limit_line_lengths(
                template3.format(**d)))
        report.append("")
    return report


def applicant_report():
    """
    Adds header & footer to what's returned by
    applicant_listing() returning a list of strings.
    """
    mappings = data.get_mappings("applicants")
    report = _header4("applicants")
    report.append('')
    report.extend(applicant_listing(mappings))
    return report

def member_listing():
    """
    Returns a formatted listing of all members (incl.
    first year, in good standing, inactive and honorary)
    with indicators for those not "in-good_standing."
    """
    stati = {11: "*", 15: " ", 14: "@", 16: "%", 17: "^"}
    fmt_str = """{status} {P_first} {P_last} {P_suffix}  {P_phone} [{P_email}]
    {P_address}, {P_town}, {P_state} {P_postal_code} -joined: {PS_begin}
"""
    report = []
    first_letter = "_"
    for mbr in data.get_mappings("all_members"):
        mbr["status"] = stati[mbr["PS_statusID"]]
        if mbr["P_last"][0] != first_letter:
            report.append("")
            first_letter = mbr["P_last"][0]
        report.append(fmt_str.format(**mbr))
    return report

def _header4(whom):
    """
    <whom> possible values: web", "exec", "applicants"...
    """
    gs = data.numbers("in_good_standing")
    f = data.numbers("first_yr")
    tm = gs + f  # all members
    h = data.numbers("honorary")
    i = data.numbers("inactive")
    a = data.numbers("applicants")
    if whom == "web":
        header = [f"Membership Roster (as of {helpers.date})", ]
        header.append("=" * len(header[0]))
        header.extend([ "",
        f"Total membership currently stands at {tm} of which",
        f"{gs} are 'members in good standing' while {f} ",
        f"(those indicated by an (*) asterix) are still",
        "within their first year of membership.",
        "Members indicated by a (^) caret have announced",
        "their intent to retire from the club.",
        f"Also listed are {h} honorary members, indicated by an",
        f"'at' (@) sign and {i} inactive members, indicated by",
        "a percent (%) sign.", "", ])
    if whom == "exec":
        header = [f"Membership Report (prepared {helpers.date})", ]
        header.append("=" * len(header[0]))
        header.extend([ "",
        f"Total membership currently stands at {tm} of which",
        f"{gs} are 'members in good standing' while {f} ",
        f"are still within their first year of membership.",
        f"There are also {h} honorary and {i} inactive members.",
          "", ])
    if whom == "applicants":
        header = [
            f"Applicants (currently {a} in number)"
            + f" as of {helpers.date}.", ]
        header.append("=" * len(header[0]))
    return header

def exec_report():  # report to executive committee
    """
    Provides a report to Exec committee.
    Returns a list of lines/strings.
    """
    report = _header4("exec")
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
    report = ["""
FOR MEMBER USE ONLY

THE DEMOGRAPHIC DATA OF THE BOLINAS ROD & BOAT CLUB MEMBERSHIP
CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED FOR
ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BR&BC EXECUTIVE
COMMITTEE.
""", ]
    report.append("")
    report.extend(_header4("web"))
    report.extend(member_listing())
    report = report[:-2]
    report.append('*' * 60)
    report.append(report[-1])
    report.append("")
    report.extend(applicant_report())
    return report

def ck__limit_line_lengths():
    text = """Hello my friend, how is every things?
I'm planning to head south to British Columbia
late in June.
What are your plans for the summer of 2026?
"""
    print(f"{text}")
    print(limit_line_lengths(text, 35))

def ck_applicant_mappings():
    for mapping in data.applicant_mappings():
        print(mapping.values())

def ck_applicant_report():
    file_name = "applicant_report.txt"
    report = "\n".join(applicant_report())
    with open(file_name, 'w') as outf:
        outf.write(report)
    print(f"Applicant report sent to '{file_name}'")

def ck_membership_report():  # report to exec
    file_name = "membership_report.txt"
    report = "\n".join(membership_report())
    with open(file_name, 'w') as outf:
        outf.write(report)
    print(f"Membership report sent to '{file_name}'")

def ck_member_mappings():
    mappings = data.member_mappings()
    n = 0
    for mapping in mappings:
        vals = [str(val) for val in mapping.values()]
        if str(n)[-1] == "0":
            print(f"{', '.join(vals)}")
            print()
        n += 1

def send2file(listing, test_file=None):
    if not test_file:
        test_file = "2check.txt"
    report = "\n".join(listing)
    with open(test_file, "w") as outf:
        outf.write(report)
    print(f"Output sent to '{test_file}'.")

def ck_member_listing():
    listing = member_listing()
    send2file(listing)

def ck_headers():
#   send2file(_header4("web"), "4web.txt")
#   send2file(_header4("exec"), "4exec.txt")
    send2file(_header4("applicants"), "4applicants.txt")


if __name__ == "__main__":
#   send2file(applicant_report(), "4app.txt")
#   send2file(exec_report(), "4exec.txt")
    send2file(forWeb(), "4web.txt")

