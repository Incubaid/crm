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


SENDGRID_API_KEY = app.config['SENDGRID_API_KEY']
if SENDGRID_API_KEY is None:
    raise KeyError('SENDGRID_API_KEY is not set.')

SUPPORT_EMAIL = app.config['SUPPORT_EMAIL']
if SUPPORT_EMAIL is None:
    raise KeyError("SUPPORT_EMAIL is not set.")

PATTERN_TO_ROOTOBJ = r'(?P<objid>\w{5})_(?P<rootobjtype>\w+)@(?P<domain>.+)'
PATTERN_SUPPORT_EMAIL = r'support@(?P<domain>.+)'


def sendemail(to='', from_="support@localhost", subject="User not recognized", body="Please email support at support@localhost"):
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email(from_)
    to_email = Email(to)
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print("Email sent..")
    print(response.status_code)
    print(response.body)


_contacts_emails = ",".join(
    [c.emails for c in db.session.query(Contact).all()])
_users_emails = ",".join(
    [u.emails for u in db.session.query(User).all()])

RECOGNIZED_SENDERS = _contacts_emails + _users_emails
rootclasses = RootModel.__subclasses__()


inbox = Inbox()


@inbox.collate
def handle_mail(to, sender, subject, body):
    # $uid_$objtype@$maildomain e.g. 4jd3_contact@main.threefoldtoken.com
    # print("Locals: ", locals())
    # if sender not in RECOGNIZED_SENDERS:
    #     sendemail(to=sender)
    for x in to:
        msupport = match(PATTERN_SUPPORT_EMAIL, x)
        mrootobj = match(PATTERN_TO_ROOTOBJ, x)
        if msupport is not None:
            d = msupport.groupdict()
            domain = d['domain']
            sendemail(from_=sender, to=SUPPORT_EMAIL, body=body)
        if mrootobj is not None:
            d = mrootobj.groupdict()
            objid = d['objid']
            rootobjtype = d['rootobjtype']
            cls = [x.__name__ for x in rootclasses if x.__name__ == rootobjtype][0]
            obj = cls.filter(id == objid)
            obj.messages.append(Message(title=subject, content=body))
            db.session.add(obj)
            # mail = email.message_from_string(body)
            # for part in mail:
            #     if part.get_content_maintype() == "multipart":
            #         continue
            # if part.get('Content-Disposition') is None:
            #     continue

            # attachement
            # filename = part.get_filename()
            # counter = 1

            # # if there is no filename, we create one with a counter to avoid duplicates
            # if not filename:
            #     filename = '../webdir/files/part-%03d%s' % (counter, 'bin')
            #     counter += 1

            # att_path = os.path.join(detach_dir, filename)

            # #Check if its already there
            # if not os.path.isfile(att_path) :
            #     # finally write the stuff
            #     fp = open(att_path, 'wb')
            #     fp.write(part.get_payload(decode=True))
            #     fp.close()

            domain = d['domain']
            db.commit()


@app.cli.command()
def mailer():
    """
    Start mailin/out services.
    """
    print("Starting mail-in/out..")
    inbox.serve(address='0.0.0.0', port=4466)
