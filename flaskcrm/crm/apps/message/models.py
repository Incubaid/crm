from crm.db import db, BaseModel
from crm.admin import ExtraMixin


class Message(db.Model, BaseModel, ExtraMixin):

    __tablename__ = "messages"

    title = db.Column(
        db.String(255),
        nullable=False
    )

    content = db.Column(
        db.Text()
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

    author = db.relationship(
        "User",
        backref="createdMessages",
        uselist=False
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

    def __str__(self):
        return self.title

    @property
    def destination(self):
        emails = []
        if self.user:
            emails.extend(self.user.emails)

        if self.contact:
            emails.extend(self.contact.emails)

        if self.company:
            emails.extend(self.company.emails)

        if self.organization:
            emails.extend(self.organization.emails)

        return emails

    @property
    def destination_emails(self):
        emails = self.destination_emails
        if emails:
            return ",".join([x.email for x in self.destination_emails])
        return "Not destination yet."
