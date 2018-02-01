import os
from re import match
from inbox import Inbox
import logging

from crm.apps.company.models import Company
from crm.apps.email.models import Email
from crm.apps.organization.models import Organization
from crm.settings import ATTACHMENTS_DIR, STATIC_URL_PATH, SENDGRID_API_KEY, SUPPORT_EMAIL
from crm.mailer import sendemail, parse_email_body
from crm.db import RootModel, db
from crm import app
from crm.apps.user.models import User
from crm.apps.contact.models import Contact
from crm.apps.message.models import Message, MessageState
from crm.apps.link.models import Link
import click

PATTERN_TO_ROOTOBJ = r'(?P<objid>\w{5})_(?P<rootobjtype>\w+)@(?P<domain>.+)'
PATTERN_SUPPORT_EMAIL = r'support@(?P<domain>.+)'


inbox = Inbox()


def get_sender(email):
    sender = Email.query.filter_by(email=email).first()

    if not sender:
        return

    if sender.user:
        return sender.user
    if sender.contact:
        return sender.contact
    if sender.company:
        return sender.company


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

    # _contacts_emails = ",".join(
    #     [c.emails for c in db.session.query(Contact).all()]
    # )

    sender_obj = get_sender(sender)

    supported_models_to_send_to = RootModel.__subclasses__() + [Message]

    if sender_obj is None and SUPPORT_EMAIL not in to:
        print("CANT RECOGNIZE SENDER ", sender)
        sendemail(to=[sender], from_=SUPPORT_EMAIL)
    else:
        for x in to:
            msupport = match(PATTERN_SUPPORT_EMAIL, x)
            mrootobj = match(PATTERN_TO_ROOTOBJ, x)
            if msupport is not None:
                d = msupport.groupdict()
                sendemail(from_=[sender], to=[SUPPORT_EMAIL], body=body)
                continue
            if mrootobj is not None:
                d = mrootobj.groupdict()
                objid = d['objid']


                rootobjtype = d['rootobjtype']
                cls = None
                q = [x for x in supported_models_to_send_to if x.__name__.lower() ==
                     rootobjtype]
                if q:
                    cls = q[0]
                else:
                    continue

                obj = cls.query.filter(cls.id == objid).first()
                if obj:


                    body, attachments = parse_email_body(body)
                    # body, attachments [hashedfilename, hashedfilpath, hashedfileurl, originalfilename, binarycontent, type]
                    msgobj = Message(title=subject, content=body, author_original=sender_obj)

                    for attachment in attachments:
                        if not os.path.exists(attachment.hashedfilepath):
                            with open(attachment.hashedfilepath, "wb") as hf:
                                hf.write(attachment.binarycontent)
                        msgobj.links.append(
                            Link(url=attachment.hashedfileurl, labels=attachment.hashedfilename + "," + attachment.originalfilename, filename=attachment.originalfilename))
                    if cls.__name__ ==  Message.__name__:
                        msgobj.deal_id = obj.deal_id
                        msgobj.company_id = obj.company_id
                        msgobj.contact_id = obj.contact_id
                        msgobj.user_id = obj.user_id
                        msgobj.task_id = obj.task_id
                        msgobj.organization_id = obj.organization_id
                        msgobj.project_id = obj.project_id
                        msgobj.sprint_id = obj.sprint_id
                        msgobj.event_id = obj.event_id
                        msgobj.author_last = sender_obj
                        msgobj.author_last_id = sender_obj.id
                        obj.replies.append(msgobj)
                    else:
                        obj.messages.append(msgobj)
                    db.session.add(obj)
                db.session.commit()


@app.cli.command()
@click.option("--host", '-h', default="0.0.0.0", help="SMTP Inbox server host.")
@click.option("--port", '-p', default=25, help="SMTP Inbox server port.", type=int)
def mailer(host, port):
    """
    Start mail in/out services.
    :param host: Host
    :param port: Port
    """
    print("Starting mail-in/out on {}:{}".format(host, port))
    inbox.serve(address=host, port=port)
