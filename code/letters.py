#!/usr/bin/env python3

# File: letters.py

"""
Code pertaining to creating letters goes here.
"""

try: from code import helpers
except : import helpers

applicant_fee = 25
today = helpers.date
signature = """
Sincerely,

Alex Kleider (Membership)
"""

letter_bodies = dict(

    for_testing="""
{"date"}

Dear {"first"} {"last"},

Blah, blah, blah.
More to say.

There's a second paragraph to add.

""",

    app_fee_pending="""
The Club is now in receipt of your application but there is
still the application fee to be submitted.

Once the Treasurer notifies me that it has come in, I will
communicate further.

In the mean time please keep in touch with your sponsors who
have the duty to shepherd you through the application process.
""",

    app_fee_received="""
Your application fee has been received so your application is
now complete!

As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

If they haven't already done so, please ask your sponsors to
inform you of the purpose and rules of the Club (as required by
our By-Laws.)

To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in a six
month period.  You may attend as the guest of any member; your
sponsors are expected to introduce you.

Looking forward to seeing each other at future meetings held at
the Club: 83 Wharf Rd., Bolinas, CA 94924
""",

    app_with_1st_meeting="""

""",

    new_applicant_welcome="""
As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

If they haven't already done so, please ask your sponsors to
inform you of the purpose and rules of the Club (as required by
our By-Laws.)

To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings within a six
month period.  You may attend as the guest of any member; your
sponsors are expected to introduce you.

Looking forward to seeing each other at future meetings held at
the Club: 83 Wharf Rd., Bolinas, CA 94924
""",

    awaiting_vacancy="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.

Unfortunately there is not currently a vacancy (since club
bylaws specify that membership must not be over 200.)

But don't despair!  You are certainly welcome to enjoy most
if not all of the privileges of membership until a vacancy
occurs at which time I will send you a request for payment of
dues and once paid you will become a full fledged member!

You're almost there; "as good as" for all intents and purposes!""",

    vacancy_open="""
It's my pleasure to report that a vacancy has come up and so
you can now become a member.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of dues.  Please send a check for ${current_dues} to the Club
(address provided below.)

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    request_inductee_payment="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of prorated dues.  Please send a check for ${current_dues} to the Club
(address provided below.)

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    second_request_inductee_payment="""
Your application for Club membership was approved by the
Club Executive Committee and membership fees have been
requested but as yet not received.  Until payment is
received you are not yet a member.  This could create a
problem for the Exec committee since there are applicants
ready to take the spot that you would take if, but only if, the
dues are paid.

Please send a check for ${current_dues} to the Club
(address provided below.)""",


    # following will eventually be redacted in favour of
    # first_dues_payment_welcome

    welcome2full_membership="""
As Membership Chair, it is my pleasure to welcome you as a new
member to the Bolinas Rod and Boat Club!

As you may know, the Club has its own web site 'rodandboatclub.com'
which is password protected. The password is 'fish' and although
not a very closely guarded secret, please do not share it with non
members.  By clicking on the "Membership" tab, you can find a
listing of all your fellow members along with contact information.
Please have a look and if you see any inaccuracies please make it
known[1] so corrections can be made.

There is a wealth of history on our website: recordings of past
'marine moments' along with photos of events, and forms for renting
the club ~ lots to explore there.

Members can (upon payment of a $25 deposit) get a key to the Club
from "keeper of the keys" Ralph Cammicia.  This provides fishermen
and boaters access to the docks (the use of which is a privilege
for which there is an extra fee- see Docks and Yards Chair Don
Murch about that) and also many take advantage of having this
access to spend time on the balcony enjoying views of the lagoon
and Bolinas Ridge.  Please be sure to lock up upon leaving.

The Club is available for members to rent for private functions (if
certain conditions are met.)  More information can be found on the
web site: "Rules and Forms" and under that "Club Rentals".

Please contact your sponsors or reach out to me if you have any
questions about anything related to the Club. If I can't answer,
I'll try to find someone who can.

As you already know, general membership meetings are held on the
first Friday of each month @ 7:30. The February Annual General
meeting is an exception to this rule. You'll be receiving
announcements from the Club Secretary. Please come and attend
meetings and other functions to enjoy the camaraderie!""",

    first_dues_payment_welcome="""
Your dues payment of ${amt_paid} has been received so it is now
my pleasure, as Membership Chair, to welcome you as a new member
to the Bolinas Rod and Boat Club!

As you may know, the Club has its own web site 'rodandboatclub.com'
which is password protected. The password is 'fish' and although
not a very closely guarded secret, please do not share it with non
members.  By clicking on the "Membership" tab, you can find a
listing of all your fellow members along with contact information.
Please have a look and if you see any inaccuracies please let me
know so corrections can be made.

There is a wealth of history on our website: recordings of past
'marine moments' along with photos of events, and forms for renting
the club ~ lots to explore there.

Members can (upon payment of a $25 deposit) get a key to the Club
from "keeper of the keys" Ralph Cammicia.  This provides fishermen
and boaters access to the docks (the use of which is a privilege
for which there is an extra fee- see Docks and Yards Chair Don
Murch about that) and also many take advantage of having this
access to spend time on the balcony enjoying views of the lagoon
and Bolinas Ridge.  Please be sure to lock up upon leaving.

The Club is available for members to rent for private functions (if
certain conditions are met.)  More information can be found on the
web site: "Rules and Forms" and under that "Club Rentals".

Please contact your sponsors or reach out to me if you have any
questions about anything related to the Club. If I can't answer,
I'll try to find someone who can.

As you already know, general membership meetings are held on the
first Friday of each month @ 7:30. The February Annual General
meeting, held at 6pm, is an exception to this rule. You'll be
receiving announcements from the Club Secretary. Please come and
attend meetings and other functions to enjoy the camaraderie!""",

    retirement_from_club="""
Your wish to retire from Club membership has been noted.

I know I speak for all members in saying we're sorry to see you go
and wish you all the best in the future.""",

    membership_termination="""
Since your membership dues have not been received by the Sept 1st
dead line set by the club by-laws, it is my sad duty to inform
you that your membership has been terminated.  Should you wish
to become a member again, it'll be necessary for you to reapply.

Let me add my own personal sentiment of regret that you have
chosen to leave the club.

If you have a club house key (issued by Ralph) please return it
to the Bolinas Rod & Boat Club, PO Box 248, Bolinas, CA 94924.""",

    expired_application="""
With considerable regret it is my duty to inform you of the
following:
It's been more than six months since your membership application
has been received and during that time you've failed to attend
the required three Club meetings. This causes your application to
expire.
If you still wish to be a member of the Bolinas Rod and Boat Club
the application process must begin again and I suggest you work
closely with your sponsors.""",

    bad_email="""
Emails sent to you at
    "{email}"
are being rejected.

Can you please help sort this out by contacting us
at rodandboatclub@gmail.com?

Thanks,""",

    bad_address="""
Mail sent to you has been returned.

We have your mailing address as :

{extra}

Please let us know if this should be corrected and, if so, to what.
""",

    feb_meeting="""

We have a special Bolinas Rod and Boat Club meeting coming up
{}.

Board members meet at 5pm.

The general meeting is scheduled for 6:00pm.
Election of Officers is the main agenda item.

Those with reservations[1]  are invited to stay for the
annual dinner to follow.

Come for the fun!
""".format(helpers.next_first_friday()),

    happyNY_and_0th_fees_request="""
A very Happy New Year to all members of the Bolinas Rod & Boat
Club!

Another friendly reminder that the Club maintains a membership
list on the 'Membership' section of the Club web site:
(rodandboatclub.com, password is 'fish'.) Please check it out
if you want to get in touch with a fellow member.
changes that should be made.

At this time you might be doing some financial planning for the
year; don't forget to include provisions for payment of Club dues
(and possibly fees as well.)  The following is included to help
you in this regard.  It's always acceptable to pay early and get it
behind you.{extra}

If the number is negative or zero, there'll be nothing due in June.
""",

    thank="""
This acknowledges receipt of your recent ${total} payment applied
to your account as it previously stood:
{before_statement}.
Thank you.

A statement of your current standing follows:
{statement}

All the best!
""",

    # Correction!!!
    correction="""
You recently received a statement of dues for the upcoming
({}) Club year. I believe the total was in error and the
corrected amount is indicated below.  You can pay it any
time although it isn't due until June.

If you have reason to believe this is in error, please let
me know[1].

My apologies for the confusion (caused by my ineptitude!)
{{extra}}""".format(helpers.club_year(which='next')),

    first_notice="""
This is a reminder that annual Club dues will be due in June.
That is still a ways out but some might like to know in advance
in order to be able to budget appropriately.  Advance warning
also benefits those that might be planning to be away for the
summer.

A statement of your dues (+/- fees) for the upcoming ({}) Club
year appears bellow.  (If you've any reason to believe that
our accounting might be in error, please let us know[1].)
If the total is zero (or negative) you're all paid up (or more
than paid up) for the upcoming year and we thank you.
{{statement}}""".format(helpers.club_year(which='next')),

    # Send with June minutes:
    June_request="""
We are now in the final month of this ({}) Club year and
annual dues (and fees where applicable) are due at the end
of the month.

This mailing is going out to all members so everyone can know
where they stand whether already paid up or not.
(If you've any reason to believe that our accounting might be
in error, please let it be known[1].)

Details are as follows:
{{statement}}""".format(helpers.club_year(which='this')),

    July_request="""
The new ({}) Club year has begun. Please send in your dues
(and any applicable fees) to the Bolinas Rod and Boat Club
at the address provided below.

If you've any reason to believe that our accounting might
be in error, please let it be known[1]. Also keep in mind
that if you have recently sent in a payment, it may not yet
have been processed. An acknowledgement letter is generally
sent when payments are processed.

Details are as follows:
{{statement}}""".format(helpers.club_year(which='this')),

    interim_request="""
Club records indicate that you have dues (and/or
applicable fees) outstanding as follows...

{extra}

If you've any reason to believe that our accounting might be
in error, please let it be known[1]. Otherwise, please send
in your remittance to the
    Bolinas Rod and Boat Club,
    PO Box 248, Bolinas, CA 94924.
at your earliest convenience.

Remember: by-laws dictate that membership is
terminated if dues are not paid by September 1st.
""",

    # Send in early August:
    August_mailing="""
As we enter the month of August it means you've already enjoyed
a month of Club membership and/or one or more of its benefits
for free but this could end soon if you don't take action!

Club records indicate that your dues (+/or other fees) have
as yet not been paid.  Please be aware that according to
Club bylaws, membership lapses if dues are not paid by Sept 1st.
Note that the date is Sept 1st, not the 15th as is sometimes
incorrectly quoted.

(If you've any reason to believe that our accounting might be in
error, please let us know[1].)

Please pay promptly; we'd hate to loose you as a member.

Details follow.
{statement}""",

    last_chance="""
If you haven't yet paid your Club dues (&/or other fees,) time
is running out. Membership is terminated if dues are not paid
by September 1st which is fast approaching.

Fees can be paid using Venmo (details below.)

What follows is a statement of what Club records indicate must be
paid if membership is to continue.
{statement}""",

    # Send towards end of August:
    final_warning="""
Club records indicate that your dues (+/or other fees) have
as yet not been paid.  Please be aware that according to
Club bylaws, membership lapses if fees are not paid by Sept 1st.
(If you've any reason to believe that our accounting might be in
error, please let us know[1].)

Please pay promptly; we'd hate to loose you as a member.

Details follow.
{statement}""",

    waiting4application_fee=f"""
We've received your application which will be complete once the
application fee (${applicant_fee}) has been received.
You are now listed in the Club data base.

The process has begun!""",

    angie_print="""
The Bolinas Rod & Boat Club is facing a crisis!

Leadership positions are being vacated and need to be filled.

Our Secretary is retiring; we need at least a Vice President
and may need a President as well; Four of our directors are
ending their terms in February and it's unclear how many will
be willing to stay on for another two year term.

This letter is an urgent appeal for volunteers who might be
willing to stand for election to these important positions.
Important because the Club is facing challenges that it can
only meet if there is a complete and dedicated leadership.

If the Club falters and goes in a direction of which you don't
approve, members will have only themselves to blame for not
stepping up to provide guidance.

If willing to serve please nominate yourself. You can do so
by email (rodandboatclub@gmail.com) or post (94924-0148.)
The annual general meeting is coming up the first Friday of
February so time is running out.
""",

    )
# ... end of letter_bodies.

def generate_letter(mapping):
    """
    <mapping> must contain all info needed:
    letter body, date, recipient, cc, bcc,
    and any letter content inserts.
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

def append_letter(letter):
    pass

if __name__ == "__main__":
    print("Running letters.py")
    print(letter_bodies["for_testing"])
