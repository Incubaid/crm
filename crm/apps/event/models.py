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
