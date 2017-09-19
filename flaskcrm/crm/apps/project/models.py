from crm.db import db, BaseModel


class Project(db.Model, BaseModel):

    __tablename__ = "projects"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    # should be markdown.
    description = db.Column(
        db.Text()
    )

    start_date = db.Column(
        db.TIMESTAMP
    )

    deadline = db.Column(
        db.TIMESTAMP
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

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey('sprints.id')
    )

    sprints = db.relationship(
        "Sprint",
        backref="project",
        primaryjoin="Project.id==Sprint.project_id"
    )

    alert_source_id = db.Column(
        db.String,
        db.ForeignKey("alertsources.id")
    )

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
    def percentage_done(self):
        pass

    def __str__(self):
        return self.name
