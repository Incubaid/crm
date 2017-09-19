from crm.db import db, BaseModel
from crm.admin import ExtraMixin


class Link(db.Model, BaseModel, ExtraMixin):

    __tablename__ = "links"

    url = db.Column(
        db.String(255),
        nullable=False
    )

    labels = db.Column(
        db.Text()
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

    alert_id = db.Column(
        db.String,
        db.ForeignKey("alerts.id")
    )

    alert_source_id = db.Column(
        db.String,
        db.ForeignKey("alertsources.id")
    )

    comments = db.relationship(
        "Comment",
        backref="link"
    )

    def __str__(self):
        return self.url
