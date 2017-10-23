from crm.db import db, BaseModel


class Comment(db.Model, BaseModel):

    __tablename__ = "comments"

    # should be markdown.
    content = db.Column(
        db.Text(),
        index=True
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
    event_id = db.Column(
        db.String,
        db.ForeignKey("events.id")
    )

    # alert_id = db.Column(
    #     db.String,
    #     db.ForeignKey("alerts.id")
    # )
    #
    # alert_source_id = db.Column(
    #     db.String,
    #     db.ForeignKey("alertsources.id")
    # )

    knowledge_base_id = db.Column(
        db.String,
        db.ForeignKey("knowledgebases.id")
    )

    def __str__(self):
        return self.content
