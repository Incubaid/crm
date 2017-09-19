from enum import Enum
from datetime import datetime

from sqlalchemy.event import listen

from database import db, BaseModel


class Telephone(db.Model, BaseModel):

    __tablename__ = "telephones"

    number = db.Column(
        db.String(20),
        nullable=False
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey("companies.id")
    )

    user_id = db.Column(
        db.String(5),
        db.ForeignKey("users.id")
    )

    def __str__(self):
        return self.number


class Email(db.Model, BaseModel):

    __tablename__ = "emails"

    email = db.Column(
        db.String(150),
        nullable=False
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey("companies.id")
    )

    user_id = db.Column(
        db.String(5),
        db.ForeignKey("users.id")
    )

    organization_id = db.Column(
        db.String(5),
        db.ForeignKey("organizations.id")
    )

    def __str__(self):
        return self.email


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


class User(db.Model, BaseModel):

    __tablename__ = "users"

    firstname = db.Column(
        db.String(15),
        nullable=False
    )

    lastname = db.Column(
        db.String(15)
    )

    # should be markdown.
    description = db.Column(
        db.Text()
    )

    message_channels = db.Column(
        db.String(10),
        default=''
    )

    telephones = db.relationship(
        "Telephone",
        backref="user"
    )

    emails = db.relationship(
        "Email",
        backref="user"
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

    ownsAlerts = db.relationship(
        "Alert",
        backref="owner",
        primaryjoin="User.id==Alert.owner_id"
    )

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

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


class UsersOrganizations(db.Model, BaseModel):
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


class UsersSprints(db.Model, BaseModel):
    """
        Many To Many Through table
    """

    __tablename__ = 'users_sprints'

    user_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey('sprints.id')
    )


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
        backref=db.backref("organizations"),
        lazy="dynamic"
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


class DealState(Enum):
    NEW, INTERESTED, CONFIRMED, WAITINGCLOSED, CLOSED = range(5)


class DealType(Enum):
    HOSTER, ITO, PTO, AMBASSADOR = range(4)


class DealCurrency(Enum):
    USD, EUR, AED, GBP = range(4)


class Deal(db.Model, BaseModel):

    __tablename__ = "deals"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    # should be markdown.
    description = db.Column(
        db.Text()
    )

    amount = db.Column(
        db.Integer
    )

    currency = db.Column(
        db.Enum(DealCurrency),
        default=DealCurrency.EUR
    )

    deal_type = db.Column(
        db.Enum(DealType),
        default=DealType.HOSTER
    )

    deal_state = db.Column(
        db.Enum(DealState),
        default=DealState.NEW
    )

    closed_at = db.Column(
        db.TIMESTAMP,
        nullable=True
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    tasks = db.relationship(
        "Task",
        backref="deal"
    )

    comments = db.relationship(
        "Comment",
        backref="deal"
    )

    messages = db.relationship(
        "Message",
        backref="deal"
    )

    links = db.relationship(
        "Link",
        backref="deal"
    )

    def __str__(self):
        return self.name


class UsersProjects(db.Model, BaseModel):
    """
    Many To Many Through Table
    """
    __tablename__ = 'users_projects'

    user_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    project_id = db.Column(
        db.String(5),
        db.ForeignKey('projects.id')
    )


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


class Project(db.Model, BaseModel):

    __tablename__ = "projects"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    # should be markdown.
    description = db.Column(
        db.Text()
    )

    start_date = db.Column(
        db.TIMESTAMP
    )

    deadline = db.Column(
        db.TIMESTAMP
    )

    comments = db.relationship(
        "Comment",
        backref="project"
    )

    links = db.relationship(
        "Link",
        backref="project"
    )

    tasks = db.relationship(
        "Task",
        backref="project"
    )

    messages = db.relationship(
        "Message",
        backref="project"
    )

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey('sprints.id')
    )

    sprints = db.relationship(
        "Sprint",
        backref="project",
        primaryjoin="Project.id==Sprint.project_id"
    )

    alert_source_id = db.Column(
        db.String,
        db.ForeignKey("alertsources.id")
    )

    contacts = db.relationship(
        "Contact",
        secondary="contacts_projects",
        backref=db.backref("projects")
    )

    promoter_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    guardian_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    @property
    def percentage_done(self):
        pass

    def __str__(self):
        return self.name


class Sprint(db.Model, BaseModel):

    __tablename__ = "sprints"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    # should be markdown.
    description = db.Column(
        db.Text()
    )

    start_date = db.Column(
        db.TIMESTAMP
    )

    deadline = db.Column(
        db.TIMESTAMP
    )

    contacts = db.relationship(
        "Contact",
        secondary="contacts_sprints",
        backref=db.backref("sprints")
    )

    tasks = db.relationship(
        "Task",
        backref="sprint"
    )

    comments = db.relationship(
        "Comment",
        backref="sprint"
    )

    links = db.relationship(
        "Link",
        backref="sprint"
    )

    messages = db.relationship(
        "Message",
        backref="sprint"
    )

    owner_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    project_id = db.Column(
        db.String(5),
        db.ForeignKey('projects.id')
    )

    @property
    def percentage_done(self):
        pass

    @property
    def hours_open(self):
        pass

    @property
    def hours_open_person_avg(self):
        pass

    @property
    def hours_open_person_max(self):
        pass

    def __str__(self):
        return self.name


class Comment(db.Model, BaseModel):

    __tablename__ = "comments"

    # should be markdown.
    content = db.Column(
        db.Text()
    )

    company_id = db.Column(
        db.String(5),
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String(5),
        db.ForeignKey("contacts.id")
    )

    user_id = db.Column(
        db.String(5),
        db.ForeignKey("users.id")
    )

    deal_id = db.Column(
        db.String(5),
        db.ForeignKey("deals.id")
    )

    task_id = db.Column(
        db.String(5),
        db.ForeignKey("tasks.id")
    )

    organization_id = db.Column(
        db.String(5),
        db.ForeignKey("organizations.id")
    )

    project_id = db.Column(
        db.String(5),
        db.ForeignKey("projects.id")
    )

    sprint_id = db.Column(
        db.String(5),
        db.ForeignKey("sprints.id")
    )

    link_id = db.Column(
        db.String(5),
        db.ForeignKey("links.id")
    )

    alert_id = db.Column(
        db.String,
        db.ForeignKey("alerts.id")
    )

    alert_source_id = db.Column(
        db.String,
        db.ForeignKey("alertsources.id")
    )

    def __str__(self):
        return self.content


class Link(db.Model, BaseModel):

    __tablename__ = "links"

    url = db.Column(
        db.String(255),
        nullable=False
    )

    labels = db.Column(
        db.Text()
    )

    contact_id = db.Column(
        db.String,
        db.ForeignKey("contacts.id")
    )

    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    deal_id = db.Column(
        db.String,
        db.ForeignKey("deals.id")
    )

    task_id = db.Column(
        db.String,
        db.ForeignKey("tasks.id")
    )

    organization_id = db.Column(
        db.String,
        db.ForeignKey("organizations.id")
    )

    project_id = db.Column(
        db.String,
        db.ForeignKey("projects.id")
    )

    sprint_id = db.Column(
        db.String,
        db.ForeignKey("sprints.id")
    )

    alert_id = db.Column(
        db.String,
        db.ForeignKey("alerts.id")
    )

    alert_source_id = db.Column(
        db.String,
        db.ForeignKey("alertsources.id")
    )

    comments = db.relationship(
        "Comment",
        backref="link"
    )

    def __str__(self):
        return self.url


class TaskType(Enum):
    FEATURE, QUESTION, TASK, STORY, CONTACT = range(5)


class TaskPriority(Enum):
    MINOR, NORMAL, URGENT, CRITICAL = range(4)


class TaskState(Enum):
    NEW, PROGRESS, QUESTION, VERIFICATION, CLOSED = range(5)


class Task(db.Model, BaseModel):

    __tablename__ = "tasks"

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text()
    )

    type = db.Column(
        db.Enum(TaskType),
        default=TaskType.FEATURE
    )

    priority = db.Column(
        db.Enum(TaskPriority),
        default=TaskPriority.MINOR
    )

    state = db.Column(
        db.Enum(TaskState),
        default=TaskState.NEW
    )

    assignment_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    deadline = db.Column(
        db.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False)

    eta = db.Column(
        db.TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )

    # in hours
    time_estimate = db.Column(
        db.Integer,
        default=0
    )

    time_done = db.Column(
        db.Integer,
        default=0
    )

    company_id = db.Column(
        db.String,
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String,
        db.ForeignKey("contacts.id")
    )

    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    deal_id = db.Column(
        db.String,
        db.ForeignKey("deals.id")
    )

    organization_id = db.Column(
        db.String,
        db.ForeignKey("organizations.id")
    )

    project_id = db.Column(
        db.String,
        db.ForeignKey("projects.id")
    )

    sprint_id = db.Column(
        db.String,
        db.ForeignKey("sprints.id")
    )

    alert_id = db.Column(
        db.String,
        db.ForeignKey("alerts.id")
    )

    comments = db.relationship(
        "Comment",
        backref="task"
    )

    messages = db.relationship(
        "Message",
        backref="task"
    )

    links = db.relationship(
        "Link",
        backref="task"
    )

    @property
    def percent_completed(self):
        done = 0.0
        for stat in self.tasks:
            done += stat.time_done
        if not done:
            return done
        if not self.time_todo:
            return 100
        return (done / self.time_todo) * 100

    def __str__(self):
        return self.title


class Message(db.Model, BaseModel):

    __tablename__ = "messages"

    title = db.Column(
        db.String(255),
        nullable=False
    )

    content = db.Column(
        db.Text()
    )

    channel = db.Column(
        db.String(255)
    )

    time_tosend = db.Column(
        db.TIMESTAMP
    )

    time_sent = db.Column(
        db.TIMESTAMP
    )

    author = db.relationship(
        "User",
        backref="createdMessages",
        uselist=False
    )

    company_id = db.Column(
        db.String,
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String,
        db.ForeignKey("contacts.id")
    )

    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    deal_id = db.Column(
        db.String,
        db.ForeignKey("deals.id")
    )

    task_id = db.Column(
        db.String,
        db.ForeignKey("tasks.id")
    )

    organization_id = db.Column(
        db.String,
        db.ForeignKey("organizations.id")
    )

    project_id = db.Column(
        db.String,
        db.ForeignKey("projects.id")
    )

    sprint_id = db.Column(
        db.String,
        db.ForeignKey("sprints.id")
    )

    def __str__(self):
        return self.title

    @property
    def destination(self):
        emails = []
        if self.user:
            emails.extend(self.user.emails)

        if self.contact:
            emails.extend(self.contact.emails)

        if self.company:
            emails.extend(self.company.emails)

        if self.organization:
            emails.extend(self.organization.emails)

        return emails

    @property
    def destination_emails(self):
        emails = self.destination_emails
        if emails:
            return ",".join([x.email for x in self.destination_emails])
        return "Not destination yet."


class TaskTracking(db.Model, BaseModel):

    __tablename__ = "tasktrackings"

    # should be markdown.
    remarks = db.Column(
        db.Text()
    )

    time_done = db.Column(
        db.Integer,
        default=0
    )

    def __str__(self):
        return "<TaskTracker %s>" % self.id


class AlertProfile(db.Model, BaseModel):

    __tablename__ = "alertprofiles"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    decription = db.Column(
        db.Text()
    )

    # toml config.
    configuration = db.Column(
        db.Text()
    )

    alert_id = db.Column(
        db.String,
        db.ForeignKey("alerts.id")
    )


class AlertSource(db.Model, BaseModel):

    __tablename__ = "alertsources"

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text()
    )

    comments = db.relationship(
        "Comment",
        backref="alertsource"
    )

    links = db.relationship(
        "Link",
        backref="alertsource"
    )

    project = db.relationship(
        "Project",
        backref="alertsources",
        uselist=False
    )

    alerts = db.relationship(
        "Alert",
        backref="source"
    )

    @property
    def source_id(self):
        pass


class AlertState(Enum):
    NEW, CONFIRMED, CLOSED = range(3)


class AlertUrgency(Enum):
    CRITICAL, URGENT, NORMAL, MINOR = range(4)


class EscalationLevel(Enum):
    YELLOW, ORANGE, RED, GREEN = range(4)


class Alert(db.Model, BaseModel):

    __tablename__ = "alerts"

    title = db.Column(
        db.String(255),
        nullable=False
    )

    # source_id = source.source_id
    alert_source_id = db.Column(
        db.String(5),
        db.ForeignKey("alertsources.id")
    )

    content = db.Column(
        db.Text()
    )

    category = db.Column(
        db.String(255)
    )

    device_uid = db.Column(
        db.String(255)
    )

    component_uid = db.Column(
        db.String(255)
    )

    state = db.Column(
        db.Enum(AlertState),
        default=AlertState.NEW
    )

    urgency = db.Column(
        db.Enum(AlertUrgency),
        default=AlertUrgency.CRITICAL
    )

    escalation_level = db.Column(
        db.Enum(EscalationLevel),
        default=EscalationLevel.YELLOW
    )

    # relations
    profile = db.relationship(
        "AlertProfile",
        backref="alert"
    )

    tasks = db.relationship(
        "Task",
        backref="alert"
    )

    comments = db.relationship(
        "Comment",
        backref="alert"
    )

    links = db.relationship(
        "Link",
        backref="alert"
    )

    owner_id = db.Column(
        db.String(5),
        db.ForeignKey('users.id')
    )

    @property
    def start_time(self):
        pass

    @property
    def close_time(self):
        pass


def assign_unique_id(mapper, connect, target):
    target.id = target.uid

for subclass in db.Model.__subclasses__():
    listen(subclass, 'before_insert', assign_unique_id)
