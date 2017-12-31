from datetime import datetime

from sqlalchemy import event

from crm.apps.message.models import Message, MessageState
from crm.apps.user.models import User
from crm.mailer import sendemail
from crm.rq import queue


def try_send(host, notification_emails, msg_id, subject, body, reply_to=None):
    now = datetime.now()
    state = MessageState.FAILED
    if notification_emails:
        try:
            sendemail(
                to=notification_emails,
                from_='%s_message@%s' % (msg_id, host),
                subject=subject,
                body=body,
                attachments=[],
                reply_to=reply_to
            )
            state = MessageState.SENT
        except Exception as e:
            print('Error sending email : %s' % e)
    else:
        print('email not sent: message.notification_emails is empty list')

    from crm.db import db
    Message.query.filter_by(id=msg_id).update({'state':state, 'time_sent':now})
    db.session.commit()


@event.listens_for(Message, 'after_insert')
def receive_after_insert(mapper, connection, message):
    from flask import request
    host = request.host

    body = message.content
    body += '\n\n\n'

    for i, link in enumerate(message.links):
        body += "Attachment %s" % i + "<a clicktracking=off href={}>{}</a>".format(request.url_root.strip('/')  + link.admin_view_link(), link)
        body += "\n"

    message = Message.query.filter_by(id=message.id).first()

    reply_to = None

    if message.parent_id:
        reply_to = '%s_message@crm.greenitglobe.com' % message.parent_id

    notification_emails = message.notification_emails[:]
    # reply message - coming from outside source since we don't support reply via messages in crm
    # so we need to exclude the author emails from notification emails
    if message.parent_id is not None:
        author_emails = message.author.emails.split(',')
        notification_emails = list(set(notification_emails) - set(author_emails))

    if notification_emails:
        queue.enqueue(
            try_send,
            host,
            message.notification_emails,
            message.id,
            message.title,
            body,
            reply_to
        )
