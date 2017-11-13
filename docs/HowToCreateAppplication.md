# HowTo Create a typical application for the CRM
We will go through the process of creating an application within the CRM.

## The application
We will create events application to manage events and the contacts of the event.

### the models
According to specs event has a title, description, contacts, comments, messages, links, tasks and event_datetime.

```python
import enum
from crm.db import db, BaseModel, ManyToManyBaseModel
from datetime import datetime


class ContactEventStatus(enum.Enum):
    INVITED = 'INVITED'
    WONTSHOW = 'WONTSHOW'
    ATTENDED = 'ATTENDED'
    DENIED = 'DENIED'
    COULDNTMAKEIT = 'COULDNTMAKEIT'

ContactEventStatus.__str__ = lambda self: self.name


class Event(db.Model, BaseModel):

    __tablename__ = "events"

    __mapper_args__ = {'polymorphic_identity': 'messages'}

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text(),
        default="",
        index=True
    )
    contact_event_status = db.Column(
        db.Enum(ContactEventStatus),
        default=ContactEventStatus.INVITED,
    )
    contacts = db.relationship(
        "Contact",
        secondary="contacts_events",
        backref="events"
    )

    comments = db.relationship(
        "Comment",
        backref="event",
    )

    messages = db.relationship(
        "Message",
        backref="event",
    )

    links = db.relationship(
        "Link",
        backref="event",
    )

    tasks = db.relationship(
        "Task",
        backref="event",
    )
    event_datetime = db.Column(
        db.TIMESTAMP,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        index=True
    )

    def __str__(self):
        return self.title


class ContactEvents(db.Model, ManyToManyBaseModel):

    __tablename__ = "contacts_events"

    event_id = db.Column(
        db.String(5),
        db.ForeignKey('events.id')
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )
```

### The Views
Add the relevent views to `admin/views.py`

#### EventModelView
```python
class EventModelView(EnhancedModelView):
    column_list = ('title', 'short_description',
                   'event_datetime',  *EnhancedModelView.columns_list_extra)
    column_searchable_list = ('title', 'event_datetime')
    column_sortable_list = ('title', 'event_datetime')

    column_details_list = ('id', 'title', 'description', 'event_datetime',
                           'contacts', 'tasks', 'messages', 'comments', 'links',
                           'author_last', 'author_original', 'updated_at')

    column_filters = ('id', 'title', 'description',
                      'event_datetime', 'contacts', 'tasks')

    form_rules = ('title', 'description',
                  'event_datetime', 'contacts', 'tasks', 'links')

    form_edit_rules = ('title', 'description',
                       'event_datetime', 'contacts', 'tasks', 'messages', 'comments', 'links',)

    inline_models = [
        (TaskModel, {'form_columns': [
            'id', 'title', 'description', 'type', 'priority', 'assignee', 'eta', 'deadline']}),
        (MessageModel, {'form_columns': [
            'id', 'title', 'content', 'channel']}),
        (CommentModel, {'form_columns': ['id', 'content']}),
        (LinkModel, {'form_columns': [
            'id', 'url', ]}),
    ]

    mainfilter = "Events / Id"
```

#### InlineEventForm 
We will create an InlineEventForm to be included in the contact views.
```python

class InlineEventModelForm(InlineFormAdmin):
    form_columns = ('id', 'title', 'contact_event_status', 'event_datetime')

    def __init__(self,):
        return super(InlineEventModelForm, self).__init__(EventModel)

```

and add it to the ContactModelView inline_models
```python
    inline_models = [
        ...
        InlineEventModelForm(),
        ...
```

### GraphQL package 

For updated docs on creating graphql package please check [Define new Types, Queries, and Mutations](docs/GraphqlAdvanced.md)
#### New type
define a new type for the event in `event/graphql/types.py`

```python
from graphene import relay

from graphene_sqlalchemy import SQLAlchemyObjectType

from crm.apps.event.models import Event


class EventType(SQLAlchemyObjectType):

    class Meta:
        model = Event
        interfaces = (relay.Node,)
        name = model.__name__

```

#### Queries
define the query in `event/graphql/queries.py`

```
import graphene

from .types import EventType
from crm.graphql import BaseQuery


class EventQuery(BaseQuery):
    events = graphene.List(EventType)

    def resolve_events(self, args, context, info):
        query = EventType.get_query(context)
        return query.all()

```

#### Arguments
define the arguments in `event/graphql/events.py`
```python
import graphene
from graphene.types.inputobjecttype import InputObjectType

from crm.apps.comment.graphql.arguments import CommentArguments
from crm.apps.link.graphql.arguments import LinkArguments
from crm.apps.message.graphql.arguments import MessageArguments
from crm.apps.task.graphql.arguments import TaskArguments


class EventArguments(InputObjectType):
    uid = graphene.String()
    title = graphene.String()
    description = graphene.String()
    contact_event_status = graphene.Float()
    event_datetime = graphene.String()

    comments = graphene.List(CommentArguments)
    tasks = graphene.List(TaskArguments)
    messages = graphene.List(MessageArguments)
    links = graphene.List(LinkArguments)
    contacts = graphene.List('crm.apps.contact.graphql.arguments.ContactArguments')


class CreateEventArguments(EventArguments):
    title = graphene.String(required=True)


class UpdateEventArguments(EventArguments):
    uid = graphene.String(required=False)
```

