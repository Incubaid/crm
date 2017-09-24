from crm.db import db, BaseModel


class Company(db.Model, BaseModel):

    __tablename__ = "companies"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    # should be markdown.
    description = db.Column(
        db.Text()
    )

    vatnumber = db.Column(
        db.String(255)
    )

    telephones = db.relationship(
        "Telephone",
        backref="company"
    )

    emails = db.relationship(
        "Email",
        backref="company"
    )

    deals = db.relationship(
        "Deal",
        backref="company"
    )

    messages = db.relationship(
        "Message",
        backref="company"
    )

    tasks = db.relationship(
        "Task",
        backref="company"
    )

    comments = db.relationship(
        "Comment",
        backref="company"
    )

    contacts = db.relationship(
        "Contact",
        secondary="companies_contacts",
        backref=db.backref("companies"),
        lazy="dynamic")

    owner_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    ownerbackup_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    def __str__(self):
        return self.name
