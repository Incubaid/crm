from crm.db import db, BaseModel


class Message(db.Model, BaseModel):

    __tablename__ = "messages"

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    content = db.Column(
        db.Text(),
        index=True
    )

    channel = db.Column(
        db.String(255)
    )

    time_tosend = db.Column(
        db.TIMESTAMP
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

    def __str__(self):
        return self.title

    @property
    def destination(self):
        emails = []
        if self.user:
            emails.extend(self.user.emails.split(','))

        if self.contact:
            emails.extend(self.contact.emails.split(','))

        if self.company:
            emails.extend(self.company.emails.split(','))

        if self.organization:
            emails.extend(self.organization.emails.split(','))

        return emails

    @property
    def destination_emails(self):

        emails = self.destination
        if emails:
            return ",".join([x.email for x in self.destination])
        return "Not destination yet."
