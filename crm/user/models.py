from crm.db import db, BaseModel, RootModel


class User(db.Model, BaseModel, RootModel):

    __tablename__ = "users"

    firstname = db.Column(
        db.String(255),
        nullable=False
    )

    lastname = db.Column(
        db.String(255)
    )

    # should be markdown.
    description = db.Column(
        db.Text()
    )

    message_channels = db.Column(
        db.String(255),
        default=''
    )

    # Comma  separated emails
    emails = db.Column(
        db.Text()
    )

    # Comma separated phones
    telephones = db.Column(
        db.Text()
    )

    # Tasks Linked to this user (may be someone is doing it for him) like create account
    tasks = db.relationship(
        "Task",
        backref="user"
    )

    ownsTasks = db.relationship(
        "Task",
        backref="assignee",
        primaryjoin="User.id==Task.assignee_id"
    )

    comments = db.relationship(
        "Comment",
        backref="user"
    )

    messages = db.relationship(
        "Message",
        backref="user"
    )

    links = db.relationship(
        "Link",
        backref="user"
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

    # knowledgebases = db.relationship(
    #     "KnowledgeBase",
    #     backref="author"
    # )

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


class UsersOrganizations(db.Model):
    """
    Many To Many Through table
    """
    __tablename__ = 'users_organizations'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    organization_id = db.Column(
        db.String(5),
        db.ForeignKey('organizations.id')
    )

    IS_MANY_TO_MANY = True


class UsersSprints(db.Model):
    """
        Many To Many Through table
    """

    __tablename__ = 'users_sprints'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey('sprints.id')
    )

    IS_MANY_TO_MANY = True

class UsersProjects(db.Model):
    """
    Many To Many Through Table
    """
    __tablename__ = 'users_projects'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    project_id = db.Column(
        db.String(5),
        db.ForeignKey('projects.id')
    )

    IS_MANY_TO_MANY = True
