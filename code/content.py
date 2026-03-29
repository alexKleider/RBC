#!/usr/bin/env python3

# File: code/content.py
ap_text = """
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
    """

ap_rfc={
        "subject": "BR&BC Application",
        "from": "alexkleider@gmail.com",
        "cc": "sponsors",
        "bcc": "alex@kleider.ca",
        "body": ap_text,
        "post_scripts": (),
        "e_and_or_p": "one_only",
        },
