from crm.db import db, BaseModel


class Organization(db.Model, BaseModel):

    __tablename__ = "organizations"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    # should be markdown
    description = db.Column(
        db.Text()
    )

    emails = db.relationship(
        "Email",
        backref="organization"
    )

    tasks = db.relationship(
        "Task",
        backref="organization"
    )

    comments = db.relationship(
        "Comment",
        backref="organization"
    )

    users = db.relationship(
        "User",
        secondary="users_organizations",
        backref="organizations"
    )

    links = db.relationship(
        "Link",
        backref="organization"
    )

    messages = db.relationship(
        "Message",
        backref="organization"
    )

    owner_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    parent_id = db.Column(
        db.String(5),
        db.ForeignKey("organizations.id")
    )

    def __str__(self):
        return self.name