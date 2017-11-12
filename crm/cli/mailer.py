import os
from re import match
import smtplib
import email.utils
import email
from email.mime.text import MIMEText
from pyblake2 import blake2b
from inbox import Inbox
import sendgrid
from crm import app
from crm.utils import sendemail
from crm.db import RootModel, db
from crm.apps.user.models import User
from crm.apps.contact.models import Contact
from crm.apps.message.models import Message
from crm.settings import ATTACHMENTS_DIR


PATTERN_TO_ROOTOBJ = r'(?P<objid>\w{5})_(?P<rootobjtype>\w+)@(?P<domain>.+)'
PATTERN_SUPPORT_EMAIL = r'support@(?P<domain>.+)'


inbox = Inbox()


@inbox.collate
def handle_mail(to, sender, subject, body):
    """
    Fired on every new email received 

    @param to [str]: receivers list. [should be in format $uid_roottypeobj@$domain].
    @param sender str: sender email. [should be in CRM database users/contacts emails] 
    @param subject str: subject
    @param body email.Message: email message object.

    If sender is not in recognized senders (contacts/users emails) an email will be sent back to him to contact support. 
    If sender is in recognized senders: we get the correct object receiving the message and attach the email text body to its messages.
    If receiever is SUPPORT_EMAIL: an email will be sent to it using sendgrid.
    """
    SUPPORT_EMAIL = app.config['SUPPORT_EMAIL']
    _contacts_emails = ",".join(
        [c.emails for c in db.session.query(Contact).all()])
    _users_emails = ",".join(
        [u.emails for u in db.session.query(User).all()])

    RECOGNIZED_SENDERS = _contacts_emails + _users_emails
    rootclasses = RootModel.__subclasses__()

    if sender not in RECOGNIZED_SENDERS:
        print("CANT RECOGNIZE SENDER ", sender)
        sendemail(to=sender, from_=SUPPORT_EMAIL)
    else:
        message = email.message_from_string(body)
        body = ""
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
                    if not os.path.exists(hashedfilepath):
                        with open(hashedfilepath, "wb") as hf:
                            hf.write(part_binary_content)
        else:
            body = message.get_payload(decode=True).decode()
        for x in to:
            msupport = match(PATTERN_SUPPORT_EMAIL, x)
            mrootobj = match(PATTERN_TO_ROOTOBJ, x)
            if msupport is not None:
                d = msupport.groupdict()
                domain = d['domain']
                sendemail(from_=SUPPORT_EMAIL, to=sender, body=body)
            if mrootobj is not None:
                d = mrootobj.groupdict()
                objid = d['objid']
                rootobjtype = d['rootobjtype']
                cls = None
                q = [x for x in rootclasses if x.__name__.lower() ==
                     rootobjtype]
                if q:
                    cls = q[0]
                else:
                    continue

                obj = cls.query.filter(cls.id == objid).first()
                obj.notify()
                msgobj = Message(title=subject, content=body)
                obj.messages.append(msgobj)
                db.session.add(obj)

                domain = d['domain']
                db.session.commit()


@app.cli.command()
def mailer():
    """
    Start mailin/out services.
    """
    SENDGRID_API_KEY = app.config['SENDGRID_API_KEY']
    if not SENDGRID_API_KEY:
        print('SENDGRID_API_KEY is not set.')
        exit(1)

    SUPPORT_EMAIL = app.config['SUPPORT_EMAIL']
    if SUPPORT_EMAIL is None:
        print("SUPPORT_EMAIL is not set.")
        exit(1)

    print("Starting mail-in/out..")
    inbox.serve(address='0.0.0.0', port=6700)
