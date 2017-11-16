import os
import os.path
import base64
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
from sendgrid.helpers.mail import Email, Content, Mail, Personalization, Attachment as SendGridAttachment
from crm.settings import ATTACHMENTS_DIR, STATIC_URL_PATH, SENDGRID_API_KEY, SUPPORT_EMAIL

Attachment = namedtuple('Attachment', [
                        'hashedfilename', 'hashedfilepath', 'hashedfileurl', 'originalfilename', 'binarycontent', 'type'])


def build_attachment(attachment):
    """
    Returns a valid sendgrid attachment from typical attachment object.
    e.g
    ```
    attachment = Attachment()
    attachment.content = ("TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNl"
                          "Y3RldHVyIGFkaXBpc2NpbmcgZWxpdC4gQ3JhcyBwdW12")
    attachment.type = "application/pdf"
    attachment.filename = "balance_001.pdf"
    attachment.disposition = "attachment"
    attachment.content_id = "Balance Sheet"
    return attachment

    ```

    """
    sendgridattachment = SendGridAttachment()
    sendgridattachment.content = base64.b64encode(
        attachment.binarycontent).decode()
    sendgridattachment.type = attachment.type
    sendgridattachment.filename = attachment.originalfilename
    sendgridattachment.disposition = "attachment"
    sendgridattachment.content_id = attachment.originalfilename

    return sendgridattachment


def parse_email_body(body):
    """
    Parses email body and searches for the attachements

    returns body, attachments List[Attachment] : Attachment is namedtuple with fields [hashedfilename, hashedfielpath, hashedfileurl, originalfilename, binarycontent]
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
                                              originalfilename=part_filename, binarycontent=part_binary_content, type=part_content_type))
    else:
        body = message.get_payload(decode=True).decode()

    return body, attachments


def sendemail(to=[], from_=None, subject="User not recognized", body="Please email support at support@localhost", attachments=[]):
    """
    Sends email using sendgrid API.

    @param to List[str] : receivers emails.
    @param from_ str: sender email. [defaults to support_email]
    @param subject str: email subject.
    @param body str: email message content.
    @param attachemnts List[Attachment]: list of attachments objects.


    """

    if from_ is None:
        from_ = SUPPORT_EMAIL
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email(from_)

    to_email = Email(to[0])
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)

    to = list(set(to))  # no duplicates.
    if len(to) > 1:
        for receiver in to[1:]:
            mail.personalizations[0].add_to(Email(receiver))

    for attachment in attachments:
        mail.add_attachment(build_attachment(attachment))
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except Exception as e:
        print(e)
        raise e

    print("Email sent..")
    print(response.status_code, response.body)
    return response.status_code, response.body
