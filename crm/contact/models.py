from crm.db import db, BaseModel


class Contact(db.Model, BaseModel):

    __tablename__ = "contacts"

    firstname = db.Column(
        db.String(15),
        nullable=False
    )

    lastname = db.Column(
        db.String(15)
    )

    description = db.Column(
        db.Text()
    )

    message_channels = db.Column(
        db.String(20),
        default=''
    )

    # relations
    telephones = db.relationship(
        "Telephone",
        backref="contact"
    )

    emails = db.relationship(
        "Email",
        backref="contact"
    )

    deals = db.relationship(
        "Deal",
        backref="contact"
    )

    comments = db.relationship(
        "Comment",
        backref="contact"
    )

    tasks = db.relationship(
        "Task",
        backref="contact"
    )

    messages = db.relationship(
        "Message",
        backref="contact"
    )

    links = db.relationship(
        "Link",
        backref="contact"
    )

    owner_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    ownerbackup_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    parent_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


class ContactsSprints(db.Model, BaseModel):
    """
        Many To Many Through table
    """

    __tablename__ = 'contacts_sprints'

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey('sprints.id')
    )

    IS_MANY_TO_MANY = True

class CompaniesContacts(db.Model, BaseModel):

    __tablename__ = 'companies_contacts'

    company_id = db.Column(
        db.String(5),
        db.ForeignKey('companies.id')
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    IS_MANY_TO_MANY = True


class ContactsProjects(db.Model, BaseModel):
    """
        Many To Many Through Table
    """

    __tablename__ = 'contacts_projects'

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    project_id = db.Column(
        db.String(5),
        db.ForeignKey('projects.id')
    )

    IS_MANY_TO_MANY = True
