import os
import os.path
from collections import namedtuple
import smtplib
import email.utils
import email
from email.mime.text import MIMEText
from pyblake2 import blake2b
import base64
import random
import string
from collections import OrderedDict
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail, Personalization
from crm.settings import ATTACHMENTS_DIR, STATIC_URL_PATH

Attachment = namedtuple('Attachment', [
                        'hashedfilename', 'hashedfilepath', 'hashedfileurl', 'originalfilename', 'binarycontent'])


def parse_email_body(body):
    """
    returns body, attachments [hashedfilename, hashedfielpath, hashedfileurl, originalfilename, binarycontent]

    """

    message = email.message_from_string(body)
    body = ""
    attachments = []  # list of tuples (filename, filepath)
    if message.is_multipart():
        g = message.walk()
        next(g)  # SKIP THE ROOT ONE.
        for part in g:
            part_content_type = part.get_content_type()
            part_body = part.get_payload()
            part_filename = part.get_param(
                "filename", None, "content-disposition")
            # make sure to check if gmail sends 2 versions always
            if part_content_type == "text/plain":
                body += part_body
            elif part_content_type == "application/octet-stream":
                bhash = blake2b()
                part_binary_content = part.get_payload(decode=True)
                bhash.update(part_binary_content)
                part_extension = os.path.splitext(part_filename)[1]
                hashedfilename = bhash.hexdigest() + part_extension
                hashedfilepath = os.path.join(
                    ATTACHMENTS_DIR, hashedfilename)
                hashedfileurl = os.path.join(
                    STATIC_URL_PATH, "uploads", "attachments", hashedfilename)

                attachments.append(Attachment(hashedfilename=hashedfilename, hashedfilepath=hashedfilepath, hashedfileurl=hashedfileurl,
                                              originalfilename=part_filename, binarycontent=part_binary_content))
    else:
        body = message.get_payload(decode=True).decode()

    return body, attachments


def sendemail(to='', from_="support@localhost", subject="User not recognized", body="Please email support at support@localhost"):
    """
    Sends email using sendgrid API.

    @param to str: receiver email.
    @param from_ str: sender email. [defaults to support_email]
    @param subject str: email subject.
    @param body str: email message content.

    """
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email(from_)
    if isinstance(to, str):
        to = [to]

    to_email = Email(to)
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("Email sent..")
    print(response.status_code)
    print(response.body)
