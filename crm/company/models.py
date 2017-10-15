from crm.db import db, BaseModel, RootModel


class CompanyTag(db.Model, BaseModel, RootModel):
    __tablename__ = "companytags"

    tag = db.Column(
        db.String(20),
        nullable=False
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey("companies.id")
    )

    def __str__(self):
        return self.tag


class Company(db.Model, BaseModel, RootModel):

    __tablename__ = "companies"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    # should be markdown.
    description = db.Column(
        db.Text(),
        default=""
    )

    vatnumber = db.Column(
        db.String(255)
    )

    website = db.Column(
        db.String(255)
    )

    # Comma  separated emails
    emails = db.Column(
        db.Text()
    )

    # Comma separated phones
    telephones = db.Column(
        db.Text()
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
        backref='companies',
    )

    owner_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    ownerbackup_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    links = db.relationship(
        "Link",
        backref="company"
    )

    tags = db.relationship(
        "CompanyTag",
        backref="company"
    )

    addresses = db.relationship(
        "Address",
        backref="company"
    )

    def __str__(self):
        return self.name
