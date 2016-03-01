#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Fetch E-mail content using imaplib
"""

from flanker import mime
import getpass
import logging
import imaplib

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "YOUR EMAIL ADDRESS"
PASSWORD = getpass.getpass()
"""
If your E-mail account has two-step verification,
you should input the specific application password.
"""
EMAIL_FOLDER = "EMAIL FILTER FOLDER NAME"
"""
You can create a filter, and specify the folder name in your filter tree here
"""


def process_mailbox(mail):
    """
    Dump all emails in the folder to files in output directory.
    """
    response_code, data = mail.search(None, "ALL")
    """
    If you want to fetch the unread E-mail, you can try:
    response_code, data = mail.search(None, "(UNSEEN)")
    """
    if response_code != 'OK':
        logging.warning("No messages found!")
        return

    for num in data[0].split():
        rv, data = mail.fetch(num, '(RFC822)')
        if response_code != 'OK':
            logging.warning("ERROR getting message")
            return
        msg = mime.from_string(data[0][1])
        if msg.body:
            """
            Your logic goes here.
            """
            return


def main():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    rv, data = mail.select(EMAIL_FOLDER)
    if rv == 'OK':
        logging.info("Processing mailbox: %s" % EMAIL_FOLDER)
        process_mailbox(mail)
        mail.close()
    else:
        logging.warining("ERROR: Unable to open mailbox %s " % rv)
    mail.logout()

if __name__ == "__main__":
    main()
