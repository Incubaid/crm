from crm.db import db, BaseModel, RootModel, ManyToManyBaseModel
from datetime import datetime

class User(db.Model, BaseModel, RootModel):

    __tablename__ = "users"

    username = db.Column(
        db.String(255),
        unique=True,
        nullable=True,
        index=True
    )

    firstname = db.Column(
        db.String(255),
        index=True
    )

    lastname = db.Column(
        db.String(255),
        index=True
    )

    # should be markdown.
    description = db.Column(
        db.Text(),
        default=""
    )

    message_channels = db.Column(
        db.String(255),
        default=''
    )

    emails = db.relationship(
        'Email',
        backref='user',
        primaryjoin="User.id==Email.user_id"
    )

    telephones = db.relationship(
        'Phone',
        backref='user',
        primaryjoin="User.id==Phone.user_id"
    )

    # Tasks Linked to this user (may be someone is doing it for him) like
    # create account
    tasks = db.relationship(
        "Task",
        backref="user",
        primaryjoin="User.id==Task.user_id"
    )

    ownsTasks = db.relationship(
        "Task",
        backref="assignee",
        primaryjoin="User.id==Task.assignee_id"
    )

    comments = db.relationship(
        "Comment",
        backref="user",
        primaryjoin="User.id==Comment.user_id"

    )

    messages = db.relationship(
        "Message",
        backref="user",
        primaryjoin="User.id==Message.user_id"

    )

    links = db.relationship(
        "Link",
        backref="user",
        primaryjoin="User.id==Link.user_id"

    )

    ownsContacts = db.relationship(
        "Contact",
        backref="owner",
        primaryjoin="User.id==Contact.owner_id"
    )

    ownsAsBackupContacts = db.relationship(
        "Contact",
        backref="ownerbackup",
        primaryjoin="User.id==Contact.ownerbackup_id"
    )

    ownsCompanies = db.relationship(
        "Company",
        backref="owner",
        primaryjoin="User.id==Company.owner_id"
    )

    ownsAsBackupCompanies = db.relationship(
        "Company",
        backref="ownerbackup",
        primaryjoin="User.id==Company.ownerbackup_id"
    )

    ownsOrganizations = db.relationship(
        "Organization",
        backref="owner",
        primaryjoin="User.id==Organization.owner_id"
    )

    ownsSprints = db.relationship(
        "Sprint",
        backref="owner",
        primaryjoin="User.id==Sprint.owner_id"
    )

    # ownsAlerts = db.relationship(
    #     "Alert",
    #     backref="owner",
    #     primaryjoin="User.id==Alert.owner_id"
    # )

    promoterProjects = db.relationship(
        "Project",
        backref="promoter",
        primaryjoin="User.id==Project.promoter_id"
    )

    guardianProjects = db.relationship(
        "Project",
        backref="guardian",
        primaryjoin="User.id==Project.guardian_id"
    )

    knowledge_bases = db.relationship(
        "KnowledgeBase",
        backref="author",
        primaryjoin="User.id==KnowledgeBase.author_id"
    )

    last_login = db.Column(
        db.TIMESTAMP,
        default=datetime.utcnow,
    )

    @property
    def notification_emails(self):
        """
        :return: list of all emails to send notifications to
        :rtype: list
        """
        return self.emails or ''

    def __str__(self):
        return self.username or '%s %s'.strip() % (self.firstname or '', self.lastname or '') or self.emails[0].email

    __repr__ = __str__


class UsersOrganizations(db.Model, ManyToManyBaseModel):
    """
    Many To Many Through table
    """
    __tablename__ = 'users_organizations'

    user_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    organization_id = db.Column(
        db.String(5),
        db.ForeignKey('organizations.id')
    )
