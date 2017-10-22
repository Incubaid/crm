from enum import Enum
from crm.db import db, BaseModel, RootModel, ManyToManyBaseModel


class SubgroupName(Enum):
    AMBASSADOR, INVESTOR, HOSTER, MEMBER, PUBLIC = range(5)


class Subgroup(db.Model, BaseModel):
    __tablename__ = "subgroups"

    groupname = db.Column(
        db.Enum(SubgroupName),
        default=SubgroupName.MEMBER,
        index=True
    )

    contacts = db.relationship(
        "Contact",
        secondary="contacts_subgroups",
        backref="subgroups"
    )

    def __str__(self):
        return self.groupname.name


class ContactSubgroup(db.Model, ManyToManyBaseModel):
    __tablename__ = "contacts_subgroups"

    subgroup_id = db.Column(
        db.String(5),
        db.ForeignKey('subgroups.id')
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )


class Contact(db.Model, BaseModel, RootModel):

    __tablename__ = "contacts"

    firstname = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    lastname = db.Column(
        db.String(255),
        default="",
        index=True
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
        backref="contact",
        primaryjoin="Contact.id==Deal.contact_id"
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
        db.Text(),
        index=True
    )

    # Comma separated phones
    telephones = db.Column(
        db.Text(),
        index=True
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


class ContactsSprints(db.Model, ManyToManyBaseModel):
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



class CompaniesContacts(db.Model, ManyToManyBaseModel):

    __tablename__ = 'companies_contacts'


    company_id = db.Column(
        db.String(5),
        db.ForeignKey('companies.id')
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )


class ContactsProjects(db.Model, ManyToManyBaseModel):
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

