from crm.db import db, BaseModel, RootModel


class Organization(db.Model, BaseModel, RootModel):

    __tablename__ = "organizations"

    name = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    # should be markdown
    description = db.Column(
        db.Text(),
        default="",
        index=True
    )

    # Comma  separated emails
    emails = db.Column(
        db.Text(),
        index=True
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
        secondaryjoin="User.id==UsersOrganizations.user_id",
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
