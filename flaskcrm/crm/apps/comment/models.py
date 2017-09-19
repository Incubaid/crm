from crm.db import db, BaseModel
from crm.admin import ExtraMixin


class Comment(db.Model, BaseModel, ExtraMixin):

    __tablename__ = "comments"

    # should be markdown.
    content = db.Column(
        db.Text()
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    user_id = db.Column(
        db.String(5),
        db.ForeignKey("users.id")
    )

    deal_id = db.Column(
        db.String(5),
        db.ForeignKey("deals.id")
    )

    task_id = db.Column(
        db.String(5),
        db.ForeignKey("tasks.id")
    )

    organization_id = db.Column(
        db.String(5),
        db.ForeignKey("organizations.id")
    )

    project_id = db.Column(
        db.String(5),
        db.ForeignKey("projects.id")
    )

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey("sprints.id")
    )

    link_id = db.Column(
        db.String(5),
        db.ForeignKey("links.id")
    )

    alert_id = db.Column(
        db.String,
        db.ForeignKey("alerts.id")
    )

    alert_source_id = db.Column(
        db.String,
        db.ForeignKey("alertsources.id")
    )

    def __str__(self):
        return self.content
