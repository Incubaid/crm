from re import match
import smtplib
import email.utils
import email
from email.mime.text import MIMEText
from inbox import Inbox
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail
from crm import app
from crm.db import RootModel, db
from crm.apps.user.models import User
from crm.apps.contact.models import Contact
from crm.apps.message.models import Message


PATTERN_TO_ROOTOBJ = r'(?P<objid>\w{5})_(?P<rootobjtype>\w+)@(?P<domain>.+)'
PATTERN_SUPPORT_EMAIL = r'support@(?P<domain>.+)'


def sendemail(to='', from_="support@localhost", subject="User not recognized", body="Please email support at support@localhost"):

    sg = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_API_KEY'])
    from_email = Email(from_)
    to_email = Email(to)
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("Email sent..")
    print(response.status_code)
    print(response.body)


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
        sendemail(to=sender)
    else:

        message = email.message_from_string(body)
        body = ""
        # TODO: support attachments.
        attachmentsfiles = []
        if message.is_multipart():
            for part in message.walk():
                part_content_type = part.get_content_type()
                part_body = part.get_payload()
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
