#!/usr/bin/env python3

# File: send_emails.py
"""
Provides send.  (when imported as a module)

When run as __main__, sends emails found in the
emails.json file defined by club.EMAIL_JSON.

Have not yet implemented ability to use
a second command line argument to specify
a json file from which to load emails.
"""

import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import mimetypes
import hashlib
import time
import random

json_email_file = "Data/emails.json"

def getpw(service):
    """
    Passwords are in highly restricted dot files.
    Each file contains only the password.
    """
    with open(
        os.path.expanduser('~/.pw.{}'.format(service)), 'r') as f_obj:
        return f_obj.read().strip()

mta_config = {  # easydns: only viable option
        "host": "mailout.easydns.com",
        "tls_port": "587",
        "ssl_port": "465",  # SSL deprecated predecessor to TLS
#       "port": "2025",
        "port": "587",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "kleider.ca",
        "from": "alex@kleider.ca",
        "password": getpw("easy"),
        "tls": "on",
    }

MIN_PAUSE = 1   #} Seconds between
MAX_PAUSE = 5   #} email postings.

def pause():
    """
    Provides a random interval between emails so that the
    MTA is less likely to think the process is automated.
    Implemented when gmail was used so is probably no longer
    necessary.
    """
    time.sleep(random.randint(MIN_PAUSE,
                              MAX_PAUSE))


rfc5322 = {    # Here for reference, not used by the code.
#  Originator Fields
   "from": "From: ", # mailbox-list CRLF
   "sender": "Sender: ", # mailbox CRLF
   "reply-to": "Reply-To: ", # address-list CRLF

#  Destination Address Fields
   "to": "To: ", # address-list CRLF
   "cc": "Cc: ", # address-list CRLF
   "bcc": "Bcc: ", # [address-list / CFWS] CRLF

#  Identification Fields
   "message-id": "Message-ID: ", # msg-id CRLF
#  "in-reply-to": "In-Reply-To: ", # 1*msg-id CRLF
#  "references": "References: ", # 1*msg-id CRLF
#  "msg-id": [CFWS] "<" id-left "@" id-right ">" [CFWS]
#  "id-left": dot-atom-text / obs-id-left
#  "id-right": dot-atom-text / no-fold-literal / obs-id-right
#  "no-fold-literal": "[" *dtext "]"

#  Informational Fields
   "subject": "Subject: ", # unstructured CRLF
   "comments": "Comments: ", # unstructured CRLF
   "keywords": "Keywords: ", # phrase *("," phrase) CRLF
    }

redact = '''
def get_bytes(text):
    """
    Not used. Can be redacted.
    """
    return hashlib.sha224(bytes(text, 'utf-8')).hexdigest()

def get_py_header(header):
    """
    Not used. Can be redacted.
    """
    return rfc5322[header.replace('-', '_')]

def attach1(attachment, msg):
    """
    Not used.  Not understood- should probably be redacted.
    """
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically
        # as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
'''

def pseudo_recipient(plus_name, g_email):
    """
    Returns an email address that will go to the gmail
    account specified by <g_email>.
    This is only applicable to gmail accounts: emulation of
    multiple addresses all pointing to same inbox:
    my+person1@gmail.com, my+person2@gmail.com, ...
    all go to my@gmail.com
    """
    parts = g_email.split('@')
    assert len(parts) == 2
    return plus_name + '+' + parts[0] + '@' + parts[1]


def attach(attachment, msg):
    """
    <msg>: an instance of MIMEMultipart() to which to add
    the attachment.
    <attachment> is the name of a file to become an attachment.
    This code has been successfully tested to work for the
    following types of files: text, .docx, .pdf, ..
    so is expected to work for all files.
    """
    basename = os.path.basename(attachment)
    with open(attachment, "rb") as f_obj:
        part = MIMEApplication(
            f_obj.read(), basename)
    # After the file is closed
    part['Content-Disposition'] = (
        'attachment; filename="%s"' % basename)
    msg.attach(part)


def attach_many(attachments, msg):
    """
    This code was 'plagerized' from the web.
    It is a slightly modified version of an excerpt of
    code submitted by vijay.anand found here..
    https://stackoverflow.com/questions/52292971/sending-single-email-with-3-different-attachments-python-3
    It is failing and therefore not used.  It's being left here
    in the hopes that it can be mended.
    """
    for attachment in attachments:
        content_type, encoding = mimetypes.guess_type(attachment)
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        maintype, subtype = content_type.split("/", 1)
        if maintype == "text":
            with open(attachment) as fp:
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == "image":
            with open(attachment, "rb") as fp:
                attachment = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == "audio":
            with open(attachment, "rb")as fp:
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(attachment, "rb") as fp:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment",
                            filename=os.path.basename(attachment))
        msg.attach(attachment)


def into_string(header_value):
    """
    Returns a string (possibly empty.)
    If given a list it must be of strings and a comma/space
    separated concatination is returned.
    """
#   print("<header_value> '{}' is of type {}."
#       .format(header_value, type(header_value)))
    if isinstance(header_value, str):
        return header_value
    elif isinstance(header_value, list):
        return ', '.join(header_value)
    else:
        return ''

def send(emails, mta_config=mta_config,
            report=None, include_wait=True):
    """
    Sends emails using Python modules.
    <emails> is a list of dicts (typically collected from a json
    file.) Each dict represents an email to be sent and can have
    the following keys, some optional:
    'body': a (possibly empty) string.
    'attachments': a list (possible empty) of file names.
    'From', 'Reply-To', 'To', 'Subject', ...
    and possibly other commonly used fields defined by rfc5322.
    Values are either strings or lists of strings in which case
    the values are converted into a single comma separated string.
    <include_wait> if True inserts a pause after each mailing.
    """
    n_emails = len(emails)
    host = mta_config["host"]
    port = mta_config["port"]
    sender = mta_config["from"]
    s = smtplib.SMTP(host=host, port=port)
    s.starttls()
    s.ehlo
    # Comment out one of the following two:
    s.login(mta_config['user'], mta_config['password'])
    response = input("... Continue? ")
    if not (response and response[0] in 'yY'):
        sys.exit()
    counter = 0
    try:
        for email in emails:
            counter += 1
            print(f"Attempting to send email #{counter} " +
                    f"to {email['To']}")
            email["Sender"] = sender
            msg = MIMEMultipart()
            body = email['body']
            del email['body']
#           attachments = email['attachments']
#           del email['attachments']
            print(
                f"Sending email {counter} of {n_emails} ...")
            for key in email:
                print(f"\t{key}: {email[key]}")
                msg[key] = into_string(email[key])
            msg.attach(MIMEText(body, 'plain'))
#           attach_many(attachments, msg) ## Fails, 2b trouble sh.
#           for attachment in attachments:
#               attach(attachment, msg)
            try:
                s.send_message(msg)
            except SMTPDataError:
                print(
                    "FAILURE sending email " +
                    f"#{n} to {email['To']}")
                continue
            if include_wait:
                pause()
    except:
        s.quit()
        print(
            "Pymail.send.send() failed sending to {}."
                .format(email['To']), also_print=True)
        raise
    s.quit()

def test_send():
    print("Running send_emails.py test...")
    mta = "easy"
    mapping = {
        'From': 'alexKleider@easydns.com',
        'Reply-To': 'rodandboatclub@gmail.com',
        'To': ['akleider@sonic.net',
                'alexkleider@gmail.com'],
        'Cc': ['alexkleider@protonmail.com',
                'rodandboatclub@gmail.com',],
        'Bcc': 'alex@kleider.ca',
        'Subject': 'TESTing easydns SMTP regarding gmail.com.',
#       'attachments': [
#       '/home/alex/Notes/Books/to-consider',],
        }
    body = "\n".join([f"{key}: {val}" for key, val in
                      mapping.items()])
    mapping['body'] = body
    test_emails = [mapping,]
    send(test_emails)

def get_json(file_name):
    """
    JSON reads <file_name>: must be a valid json file
    """
    with open(file_name, 'r') as f_obj:
        return json.load(f_obj)

def main():
    """
    """
    in_file = input(
        f"Blank if {json_email_file} or enter another: ")
    if not in_file:
        in_file = json_email_file
    yn = input(f"OK to get json data from {in_file} (y/n)?")
    if yn and yn[0] in "yY":
        data = get_json(in_file)
        send(data, report=[])
#   test_send()

def tester():
    _ = input("pseudo_recipient('ak', 'alexkleider@gmail.com')"
        + " yields " +
        f"{pseudo_recipient('ak', 'alexkleider@gmail.com')}")

if __name__ == "__main__":
#   main()
#   tester()
    test_send()

