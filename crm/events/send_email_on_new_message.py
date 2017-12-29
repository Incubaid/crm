from datetime import datetime

from sqlalchemy import event

from crm.apps.message.models import Message, MessageState
from crm.mailer import sendemail
from crm.rq import queue


def try_send(notification_emails, msg_id, subject, body, reply_to=None):
    now = datetime.now()
    state = MessageState.FAILED
    # message_tbl = message.__table__
    if notification_emails:
        try:
            sendemail(
                to=notification_emails,
                from_='%s_message@crm.greenitglobe.com' % msg_id,
                subject=subject,
                body=body,
                attachments=[],
                reply_to=reply_to
            )
            state = MessageState.SENT
        except Exception as e:
            print('Error sending email : %s' % e)
    else:
        print('Error sendinf email : message.notification_emails is empty list')

    from crm.db import db
    Message.query.filter_by(id=msg_id).update({'state':state, 'time_sent':now})
    db.session.commit()


@event.listens_for(Message, 'after_insert')
def receive_after_insert(mapper, connection, message):

    body = message.content
    body += '\n\n\n'

    for i, link in enumerate(message.links):
        body += "Attachment %s" % i + "<a href={}>{}</a>".format(link.admin_view_link(), link)
        body += "\n"

    message = Message.query.filter_by(id=message.id).first()

    reply_to = None

    if message.parent_id:
        reply_to = '%s_message@crm.greenitglobe.com' % message.parent_id

    if message.notification_emails:
        queue.enqueue(
            try_send,
            message.notification_emails,
            message.id,
            message.title,
            body,
            reply_to
        )
