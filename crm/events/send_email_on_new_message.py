from datetime import datetime

from sqlalchemy import event

from crm.apps.message.models import Message, MessageState
from crm.mailer import sendemail
from crm.db import db


@event.listens_for(Message, 'after_insert')
def receive_after_insert(mapper, connection, message):

    now = datetime.now()
    state = MessageState.FAILED
    message_tbl = message.__table__

    if message.notification_emails:
        try:
            sendemail(
                to=message.notification_emails,
                from_='%s_message@crm.greenitglobe.com' % message.id,
                subject=message.title,
                body=message.content,
                attachments=[]
            )
            state = MessageState.SENT
        except Exception as e:
            print('Error sending email : %s' % e)
    else:
        print('Error sendinf email : message.notification_emails is empty list')

    connection.execute(
        message_tbl.update().
            where(message_tbl.c.id == message.id).
            values(state=state, time_sent=now)
    )

