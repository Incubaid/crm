from enum import Enum
from crm.db import db, BaseModel
from sqlalchemy_utils import generic_relationship

class MessageState(Enum):
    TOSEND = 'TOSEND'
    SENT = 'SENT'
    FAILED = 'FAILED'


MessageState.__str__ = lambda self: self.name


class Message(db.Model, BaseModel):

    __tablename__ = "messages"

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    content = db.Column(
        db.Text(),
        nullable=False,
        index=True
    )

    channel = db.Column(
        db.String(255)
    )

    time_sent = db.Column(
        db.TIMESTAMP
    )

    message_author_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )
    author = db.relationship(
        "User",
        backref="createdMessages",
        uselist=False,
        foreign_keys=[message_author_id]
    )

    company_id = db.Column(
        db.String,
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String,
        db.ForeignKey("contacts.id")
    )

    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    deal_id = db.Column(
        db.String,
        db.ForeignKey("deals.id")
    )

    task_id = db.Column(
        db.String,
        db.ForeignKey("tasks.id")
    )

    organization_id = db.Column(
        db.String,
        db.ForeignKey("organizations.id")
    )

    project_id = db.Column(
        db.String,
        db.ForeignKey("projects.id")
    )

    sprint_id = db.Column(
        db.String,
        db.ForeignKey("sprints.id")
    )

    event_id = db.Column(
        db.String,
        db.ForeignKey("events.id")
    )

    links = db.relationship(
        "Link",
        backref="message"
    )

    state = db.Column(
        db.Enum(MessageState),
        default=MessageState.TOSEND,
        index=True
    )

    parent_id = db.Column(
        db.String(5),
        db.ForeignKey('messages.id')
    )

    author_original_type = db.Column(
        db.Unicode(255)
    )

    author_original_id = db.Column(
        db.Integer,
    )

    author_original = generic_relationship(
        author_original_type,
        author_original_id
    )

    @property
    def parent(self):
        if self.parent_id:
            return self.__class__.query.filter_by(id=self.parent_id).first()

    replies = db.relationship(
        "Message",
        uselist=True,

    )

    # ',' separated string of emails
    # Is used to force sending emails to certain destination
    # If not set, `notification_emails` is used instead to calculate
    # ALl email addresses
    forced_destinations = db.Column(
        db.String,
    )

    @property
    def notification_emails(self):
        """
        :return: list of all emails to send notifications to
        :rtype: list
        """
        if self.forced_destinations:
            return [d.strip() for d in self.forced_destinations.split(',') if d]

        obj = None

        if self.user:
            obj = self.user
        elif self.contact:
            obj = self.contact
        elif self.company:
            obj = self.company
        elif self.organization:
            obj = self.organization
        elif self.deal: # contact emails or company emails
            obj = self.deal
        elif self.task: # assignee + one of these if found (contact, users, deal, company, organization, event, sprint)
            obj = self.task
        elif self.project: # promoter + guardian + contacts + one of (tasks, sprints)
            obj = self.project
        elif self.event: # All contacts emails + All tasks emails
            obj = self.event
        elif self.sprint: # contacts + owner + tasks
            obj = self.sprint

        if not obj:
            return []

        return list(set(obj.notification_emails))

    def __str__(self):
        return self.title
