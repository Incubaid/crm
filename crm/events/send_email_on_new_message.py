import os
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

    # This can be executed in HTTP context after adding a message
    # or through cli/mailer when inserting a message
    # if executed in CRM HTTP context, we can get host
    # otherwise we need to check for os.get_env('DOMAIN')

    if request:
        host = request.host
        url_root = request.url_root.strip('/')
    else:
        host = os.getenv('DOMAIN')
        url_root = 'https://{}'.format(host)
        if not host:
            print('Missing DOMAIN env variable. emails are not going to be sent')
            return

    body = message.content
    body += '\n\n\n'

    for i, link in enumerate(message.links):
        body += "Attachment %s</br>" % str(i+1) + "<a clicktracking=off href={}>{}</a></br>".format(url_root  + link.admin_view_link(), link)
        body += "\n"

    message = Message.query.filter_by(id=message.id).first()

    reply_to = None

    if message.parent_id:
        reply_to = '%s_message@%s' % (message.parent_id, host)

    notification_emails = message.notification_emails[:]
    # reply message - coming from outside source since we don't support reply via messages in crm
    # so we need to exclude the author emails from notification emails
    if message.parent_id is not None:
        author_emails = message.author_original.emails.split(',')
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
