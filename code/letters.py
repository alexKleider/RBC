#!/usr/bin/env python3

# File: letters.py

"""
Code pertaining to creating letters goes here.

Problem of gmail dropping sent emails:
    If you send messages with a bulk mailing vendor or
third party affiliates there is a problem in that Gmail
recipients don't receive the emails unless unless both
the From: and ReplyTo: fields are set to the tru sender!
Also: Publish an SPF record that includes the IPs of the
vendor or affiliates acting as your SMTA and sign your
messages with a DKIM signature that is associated with
your domain.

From: alex@kleider.ca
My IP: 98.97.25.207  or easyDNS's IP4:64.68.200.48
Set the "Host" or "Name" field to @ (or leave it blank)
to apply to your root domain.
currently set to: v=spf1 include:easymail.ca ~all
should I change it to my IP:
    v=spf1 include:easymail.ca IP4:98.97.25.207 ~all
or that of easyDNS:
  v=spf1 include:easymail.ca IP4:64.68.200.48 ~all
    or
  v=spf1 include:easymail.ca IP4:64.68.200.48 Host:@ ~all
"""

try: from code import helpers
except : import helpers

applicant_fee = 25
today = helpers.date
signature = """
Sincerely,

Alex Kleider (Membership)
"""
app_mapping = {  #  applicant to test mailing
        "personID": 67,
        "first": "Joe",
        "last": "Blow",
        "suffix": "",
        "email": "myemail@provider.me",

        "s1_ID": 35,
        "s1_first": "Ralph",
        "s1_last": "Camiccia",
        "s1_suffix": "",
        "s1_email": "rc@provider.com",

        "s2_ID": 70,
        "s2_first": "Rudi",
        "s2_last": "Ferris",
        "s2_suffix": "",
        "s2_email": "rf@provider.com",

        "app_rcvd": "20260501",
        "fee_rcvd": "20260501",
        "meeting1": "20260501"
                  }

def add_salutation(mapping):
    if mapping['suffix']:
        mapping[
          "salutation"] = "Dear {first} {last}{suffix},"
    else:
        mapping[
          "salutation"] = "Dear {first} {last},"
    return mapping

def add_letter(mapping):
    """
    Still a work in progress
    """
    for key in applicants.key_status_mapping.keys():
        if mapping["notified"]:  # shouldn't get here?
            pass
        elif mapping["dues_paid"]: # notify/congrats
            pass # "member"
        elif mapping["approved"]: # notify/request $
            pass # "approved"
        elif mapping["meeting3"]: # notify exec
            pass # letter depends on # of members
        elif mapping["meeting2"]: # acknowledge
            pass # "meeting_2"
        elif mapping["meeting1"]: # acknowledge
            pass # "meeting_1" or "app_w_meeting"
        elif mapping["no_meetings"]: # acknowledge
            pass # "meeting_0"
        elif mapping["fee_rcvd"]: # acknowledge
            pass # "app_complete"
        elif mapping["app_rcvd"]: # need fee!
            pass # "app_fee_pending"
        else:
            pass
    return mapping

letter_bodies = dict(
        # app_fee_pending
        # app_complete
        # app_w_meeting
        # approved
        # member
    for_testing="""
Blah, blah, blah.
More to say.

There's a second paragraph to add.
""",
    app_fee_pending="""
The Club is now in receipt of your application but there
is still the ${app_fee} application fee to be submitted.
Once the Treasurer notifies me that it has come in,
I will communicate further.

In the mean time please keep in touch with your sponsors
who have the duty to shepherd you through the application
process.
""",

    app_complete="""
Your application for membership in the Bolinas Rod and
Boat Club has been received and appears to be in order
so as Membership Chair it is my pleasure to welcome you
to the Club!

If they haven't already done so, please ask your sponsors
to inform you of the purpose and rules of the Club (as
required by our By-Laws.)

To become eligible for membership (and not waste your
application fee) you must attend a minimum of three
meetings with in a six month period.  You may attend
as the guest of any member; your sponsors are expected
to introduce you.

Looking forward to seeing each other at future meetings
held at the Club: 83 Wharf Rd., Bolinas, CA 94924
""",
    app_w_meeting="""
This letter is to acknowledge that our application for
membership in the Bolinas Rod and Boat Club has been
received, appears to be in order, and you've already 
attended your first meeting! As Membership Chair it is
my pleasure to welcome you to the Club!

If they haven't already done so, please ask your sponsors
to inform you of the purpose and rules of the Club (as
required by our By-Laws.)

To become eligible for membership (and not waste your
application fee) you must attend at least two more
meetings with in a six month period.  You may attend
as the guest of any member; your sponsors are expected
to introduce you.

Looking forward to seeing each other at future meetings
held at the Club: 83 Wharf Rd., Bolinas, CA 94924
""",
    meeting_1="""
""",
    meeting_2="""
""",
    meeting_3="""
""",  # notify exec committee
    awaiting_vacancy="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.
Unfortunately there is not currently a vacancy. (Club
bylaws specify that membership must not exceed 200.)

But don't despair!  You are certainly welcome to enjoy
most if not all of the privileges of membership until
a vacancy occurs at which time I will send you a request
for payment of dues and once paid you will become a full
fledged member!

You're almost there; "as good as" for all intents and
purposes!""",
    vacancy_open="""
It's my pleasure to report that a vacancy has come up
and so you can now become a member.
"Welcome aboard!"
All that remains for your membership to take effect is
payment of ${dues} in prorated dues. This can be done
using Venmo or sending a check to PO Box 248 (94924.)
Upon receipt of your membership dues, I'll send you more
information about the Club and your privileges as a
member there of.
""",
    approved="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.
"Welcome aboard!"
All that remains for your membership to take effect is
payment of ${dues} in prorated dues. This can be done
using Venmo or sending a check to PO Box 248 (94924.)
Upon receipt of your membership dues, I'll send you more
information about the Club and your privileges as a
member there of.
""",
    second_request_inductee_payment="""
Your application for Club membership was approved by the
Club Executive Committee and membership fees have been
requested but as yet not received.  Until payment is
received you are not yet a member.  This could create a
problem for the Exec committee since there are applicants
ready to take the spot that you would take if, but only
if, the dues are paid.
Please send a check for ${dues} to PO Box 248 (94924.)
""",
    # following will eventually be redacted in favour of
    # first_dues_payment_welcome
    member="""
As Membership Chair, it is my pleasure to welcome you
as a new member to the Bolinas Rod and Boat Club!

As you may know, the Club has its own web site
'rodandboatclub.com' which is password protected.
The password is 'fish' and although not a very closely
guarded secret, please do not share it with non members.
By clicking on the "Membership" tab, you can find a
listing of all your fellow members along with contact
information.  Please have a look and if you see any
inaccuracies please make it known so corrections can
be made. (email rodandboatclub@gmail.com)

There is a wealth of history on our website: recordings
of past 'marine moments' along with photos of events, and
forms for renting the club ~ lots to explore there.

Members can (upon payment of a $25 deposit) get a key to
the Club from "keeper of the keys" Ralph Cammicia.  This
provides fishermen and boaters access to the docks (the
use of which is a privilege for which there is an extra
fee- see Docks and Yards Chair Don Murch about that) and
also many take advantage of having this access to spend
time on the balcony enjoying views of the lagoon and
Bolinas Ridge.  Please be sure to lock up upon leaving.

The Club is available for members to rent for private
functions (if certain conditions are met.)  More
information can be found on the web site: "Rules and
Forms" and under that "Club Rentals".

Please contact your sponsors or reach out to me if you
have any questions about anything related to the Club.
If I can't answer, I'll try to find someone who can.

As you already know, general membership meetings are held
on the first Friday of each month @ 7:30. The February
Annual General meeting is an exception to this rule.
You'll be receiving announcements from the Club Secretary.
Please come and attend meetings and other functions to
enjoy the camaraderie!""",
    retirement_from_club="""
Your wish to retire from Club membership has been noted.
I know I speak for all members in saying we're sorry to
see you go and wish you all the best in the future.
""",
    membership_termination="""
Since your membership dues have not been received by
the Sept 1st dead line set by the club by-laws, it is
my sad duty to inform you that your membership has been
terminated. Should you wish to become a member again,
it'll be necessary for you to reapply.
Let me add my own personal sentiment of regret that
you have chosen to leave the club.
If you have a club house key (issued by Ralph) please
return it to the Bolinas Rod & Boat Club, PO Box 248,
Bolinas, CA 94924.""",
    expired_application="""
With considerable regret it is my duty to inform you that
it's been more than six months since your membership
application has been received and during that time you've
failed to attend the required three Club meetings. This
causes your application to expire.
If you still wish to be a member of the Bolinas Rod and
Boat Club the application process must begin again and
I suggest you work closely with your sponsors.""",
    bad_email="""
Emails sent to you at "{email}" are being rejected.
Can you please help sort this out by contacting us
at rodandboatclub@gmail.com?
Thanks,""",
    bad_address="""
Mail sent to you has been returned.
We have your mailing address as :
{extra}
Please let us know if this should be corrected and, if so, to what.
""",
)
# ... end of letter_bodies (dict declaration.)

def generate_letter(mapping):
    """
    <mapping> provide recipient and sponsor data
    from which letter can be generated.
    Additional info needed:
    letter body, date, recipient, cc, bcc,
    and any letter content inserts.

        S1_personID, S1_first, S1_last, S1_email,
        S2_personID, S2_first, S2_last, S2_email)
    """
    letter = letter_bodies[mapping["letter_body"]]
    body = body.format(**mapping)
    date = helpers.date
    salutation = (f"Dear {mapping['first']} " +
                  f"{mapping['last']},")
    signature = "\nSincerely,\nAlex Kleider (Membership)"
    postscripts = []
    cc = mapping["ccs"]
    bcc = mapping["bccs"]
    pass

def append_letter(mapping):
    print(
    "code.letters.append_letter not yet implemented")

if __name__ == "__main__":
    print("Running letters.py")
    print(letter_bodies["for_testing"])

