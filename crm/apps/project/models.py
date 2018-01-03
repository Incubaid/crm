from crm.db import db, BaseModel, RootModel
from crm.mailer import sendemail


class Project(db.Model, BaseModel, RootModel):

    __tablename__ = "projects"

    name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    # should be markdown.
    description = db.Column(
        db.Text(),
        default="",
        index=True
    )

    start_date = db.Column(
        db.TIMESTAMP,
        index=True
    )

    deadline = db.Column(
        db.TIMESTAMP,
        index=True
    )

    comments = db.relationship(
        "Comment",
        backref="project"
    )

    links = db.relationship(
        "Link",
        backref="project"
    )

    tasks = db.relationship(
        "Task",
        backref="project"
    )

    messages = db.relationship(
        "Message",
        backref="project"
    )

    sprints = db.relationship(
        "Sprint",
        backref="project",
        primaryjoin="Project.id==Sprint.project_id"
    )

    # alert_source_id = db.Column(
    #     db.String,
    #     db.ForeignKey("alertsources.id")
    # )

    contacts = db.relationship(
        "Contact",
        secondary="contacts_projects",
        backref=db.backref("projects")
    )

    promoter_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    guardian_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    @property
    def notification_emails(self):
        """
        :return: list of all emails to send notifications to
        :rtype: list
        """
        emails = []

        if self.promoter:
            if self.promoter.notification_emails:
                emails.extend(self.promoter.notification_emails)

        if self.guardian:
            if self.guardian.notification_emails:
                emails.extend(self.guardian.notification_emails)

        if self.contacts:
            for contact in self.contacts:
                if contact.notification_emails:
                    emails.extend(contact.notification_emails)

        if self.tasks:
            for task in self.tasks:
                if task.notification_emails:
                    emails.extend(task.notification_emails)

        elif self.sprint:
            if self.sprint.notification_emails:
                emails.extend(self.sprint.notification_emails)

        return list(set(emails))

    @property
    def percentage_done(self):
        pass

    def __str__(self):
        return self.name
