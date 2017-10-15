from enum import Enum
from crm.db import db, BaseModel, RootModel


class SubgroupName(Enum):
    AMBASSADOR, INVESTOR, HOSTER, MEMBER, PUBLIC = range(5)


class Subgroup(db.Model, BaseModel, RootModel):
    __tablename__ = "subgroups"

    groupname = db.Column(
        db.Enum(SubgroupName),
        default=SubgroupName.MEMBER
    )

    contacts = db.relationship(
        "Contact",
        secondary="contacts_subgroups",
        backref="subgroups"
    )


    def __str__(self):
        return self.groupname.name

class SubgroupContact(db.Model):
    __tablename__ = "contacts_subgroups"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    subgroup_id = db.Column(
        db.String(5),
        db.ForeignKey('subgroups.id')
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    IS_MANY_TO_MANY = True


class Contact(db.Model, BaseModel, RootModel):

    __tablename__ = "contacts"

    firstname = db.Column(
        db.String(255),
        nullable=False
    )

    lastname = db.Column(
        db.String(255),
        default=""
    )
    description = db.Column(
        db.Text()
    )

    images = db.relationship("Image", backref="contact")

    bio = db.Column(
        db.Text(),
        default=""
    )

    belief_statement = db.Column(
        db.Text(),
        default=""
    )

    message_channels = db.Column(
        db.String(255),
        default=''
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

    # Comma  separated emails
    emails = db.Column(
        db.Text()
    )

    # Comma separated phones
    telephones = db.Column(
        db.Text()
    )

    tf_app = db.Column(
        db.Boolean()
    )

    tf_web = db.Column(
        db.Boolean()
    )

    referral_code = db.Column(
        db.String(255),
    )

    addresses = db.relationship(
        "Address",
        backref="contact"
    )

    @property
    def address(self):
        return "{} {} {}".format(self.street_number or '', '%s,' % self.street_name if self.street_name else '',  self.country).strip()

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
