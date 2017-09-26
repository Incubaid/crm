import enum
from crm.db import db, BaseModel, RootModel
from crm.countries import countries

# countries = dict(zip(countries.values(), countries.values()))
CountriesEnum = enum.Enum('Countries', countries)

CountriesEnum.__str__ = lambda self: self.value


class Contact(db.Model, BaseModel, RootModel):

    __tablename__ = "contacts"

    firstname = db.Column(
        db.String(255),
        nullable=False
    )

    lastname = db.Column(
        db.String(255)
    )
    description = db.Column(
        db.Text()
    )
    bio = db.Column(
        db.Text()
    )
    belief_statement = db.Column(
        db.Text()
    )
    message_channels = db.Column(
        db.String(255),
        default=''
    )
    street_name = db.Column(
        db.String(255)
    )
    street_number = db.Column(
        db.Integer
    )
    zip_code = db.Column(
        db.String(255)
    )
    country = db.Column(db.Enum(CountriesEnum),
                        default=CountriesEnum.BE)
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

    # Comma  separated emails
    emails = db.Column(
        db.Text()
    )

    # Comma separated phones
    telephones = db.Column(
        db.Text()
    )

    @property
    def address(self):
        return "{} {}, {}".format(self.street_number, self.street_name, self.country)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


class ContactsSprints(db.Model):
    """
        Many To Many Through table
    """

    __tablename__ = 'contacts_sprints'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey('sprints.id')
    )

    IS_MANY_TO_MANY = True


class CompaniesContacts(db.Model):

    __tablename__ = 'companies_contacts'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey('companies.id')
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    IS_MANY_TO_MANY = True


class ContactsProjects(db.Model):
    """
        Many To Many Through Table
    """

    __tablename__ = 'contacts_projects'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    project_id = db.Column(
        db.String(5),
        db.ForeignKey('projects.id')
    )

    IS_MANY_TO_MANY = True
