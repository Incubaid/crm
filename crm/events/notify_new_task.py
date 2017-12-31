from sqlalchemy import event
from flask import request

from crm.apps.message.models import Message
from crm.apps.task.models import Task


@event.listens_for(Task, 'after_insert')
def receive_after_insert(mapper, connection, task):
    if task.assignee:
        msg = Message(
            title='You have a new assigned task',
            content='Title: {}<br>Description:{}<br/><br/>Task Link: <a clicktracking=off href={}>{}</a>'.format(task.title, task.description, request.url_root.strip('/')  + task.admin_view_link(), task),
            user=task.assignee,
            task=task,
            forced_destinations=task.assignee.emails
        )

        message_tbl = Message.__table__
        # Create a message for assignee only that he/she has new task
        connection.execute(
            message_tbl.insert().
                values(
                    id=msg.uid,
                    title=msg.title,
                    content=msg.content,
                    user_id=msg.user.id
                )
        )


@event.listens_for(Task, 'after_update')
def receive_after_update(mapper, connection, task):
    if task.assignee:
        msg = Message(
            title='Your assigned task has been updated',
            content='Title: {}<br>Description:{}<br/><br/>Task Link: <a clicktracking=off href={}>{}</a>'.format(task.title, task.description, request.url_root.strip('/')  + task.admin_view_link(), task),
            user=task.assignee,
            task=task,
            forced_destinations=task.assignee.emails
        )

        message_tbl = Message.__table__
        # Create a message for assignee only that he/she has new task
        connection.execute(
            message_tbl.insert().
                values(
                id=msg.uid,
                title=msg.title,
                content=msg.content,
                user_id=msg.user.id
            )
        )
