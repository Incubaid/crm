from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from uuid import uuid4
db = SQLAlchemy()  # init later in app.py
db.session.autocommit = True


class AdminLinksMixin:
    ADMIN_EDIT_LINK = "/{modelname}/edit/?id={modelid}&url=/{modelname}/"
    ADMIN_VIEW_LINK = "/{modelname}/details/?id={modelid}&url=/{modelname}/"

    def admin_edit_link(self):
        modelname = self.__class__.__name__.lower()
        # if modelname in "Telephone"
        return AdminLinksMixin.ADMIN_EDIT_LINK.format(modelname=modelname, modelid=self.id)

    def admin_view_link(self):
        modelname = self.__class__.__name__.lower()

        return AdminLinksMixin.ADMIN_VIEW_LINK.format(modelname=modelname, modelid=self.id)


def generate_id(): return str(uuid4())[:4]


class Telephone(db.Model, AdminLinksMixin):
    __tablename__ = "telephones"
    id = db.Column('telephone_id', db.Integer,
                   primary_key=True)
    number = db.Column(db.String(20), nullable=False)  # how long is phoneumber
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))

    def __str__(self):
        return self.number


class Email(db.Model, AdminLinksMixin):
    __tablename__ = "emails"
    id = db.Column('email_id', db.Integer,
                   primary_key=True)
    email = db.Column(db.String(255), nullable=False)  # how long is phoneumber
    contact_id = db.Column(db.String(4), db.ForeignKey("contacts.contact_id"))
    company_id = db.Column(db.String(4), db.ForeignKey("companies.company_id"))
    organization_id = db.Column(
        db.String(4), db.ForeignKey("organizations.organization_id"))

    def __str__(self):
        return self.email


class Contact(db.Model, AdminLinksMixin):
    __tablename__ = "contacts"
    id = db.Column('contact_id', db.String(
        4), default=generate_id, primary_key=True)
    # uid = db.Column(db.String(4))
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15))
    description = db.Column(db.Text())  # should be markdown.
    message_channels = db.Column(db.String(10), default="E1,S2:T1")

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)
    isuser = db.Column(db.Boolean, default=False)

    # relations
    telephones = db.relationship("Telephone", backref="contact")
    emails = db.relationship("Email", backref="contact")

    organization_id = db.Column(
        db.String(4), db.ForeignKey("organizations.organization_id"))

    deals = db.relationship("Deal", backref="contact")
    comments = db.relationship("Comment", backref="contact")
    # tasks = db.relationship("Task", backref="assignee")
    messages = db.relationship("Message", backref="contact")
    links = db.relationship("Link", backref="contact")
    assignments = db.relationship("TaskAssignment", backref="contact")
    owner_id = db.Column(db.String(4), db.ForeignKey("contacts.contact_id"))
    owner = db.relationship('Contact', primaryjoin=(
        'Contact.owner_id==Contact.id'), backref='ownedusers', remote_side=id, uselist=False)

    ownerbackup_id = db.Column(
        db.String(4), db.ForeignKey("contacts.contact_id"))
    ownerbackup = db.relationship('Contact', primaryjoin=(
        'Contact.ownerbackup_id==Contact.id'), backref='backupownedusers', remote_side=id, uselist=False)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


class Company(db.Model, AdminLinksMixin):
    __tablename__ = "companies"
    id = db.Column('company_id', db.String(
        4), default=generate_id, primary_key=True)
    # uid = db.Column(db.String(4))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    isuser = db.Column(db.Boolean, default=False)

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # relations
    telephones = db.relationship("Telephone", backref="company")
    emails = db.relationship("Email", backref="company")
    deals = db.relationship("Deal", backref="company")
    messages = db.relationship("Message", backref="company")
    tasks = db.relationship("Task", backref="company")
    comments = db.relationship("Comment", backref="company")

    contact_id = db.Column(db.String(4), db.ForeignKey("contacts.contact_id"))
    owner = db.relationship("Contact", backref="ownedcompanies", uselist=False)
    ownerbackup = db.relationship(
        "Contact", backref="backupownedcompanies", uselist=False)

    def __str__(self):
        return self.name


#  manytomany through table.
class ContactsOrganizations(db.Model, AdminLinksMixin):
    __tablename__ = 'contacts_organizations'
    id = db.Column(db.String(4), default=generate_id, primary_key=True)
    contact_id = db.Column(db.String(4), db.ForeignKey(
        'contacts.contact_id'))  # , ondelete='CASCADE'))
    organization_id = db.Column(db.String(4), db.ForeignKey(
        'organizations.organization_id'))  # , ondelete='CASCADE'))


class Organization(db.Model, AdminLinksMixin):
    __tablename__ = "organizations"
    id = db.Column('organization_id', db.String(
        4), default=generate_id, primary_key=True)
    # uid = db.Column(db.String(4))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

#     #relations
    emails = db.relationship("Email", backref="organization")
    users = db.relationship("Contact", backref="organization")
    tasks = db.relationship("Task", backref="organization")
    comments = db.relationship("Comment", backref="organization")
    # users = db.relationship("Contact", secondary="contacts_organizations",
    # backref=db.backref("organizations"), lazy="dynamic")

    links = db.relationship("Link", backref="organization")
    messages = db.relationship("Message", backref="organization")
    sprints = db.relationship("Sprint", backref="organization")
    promoter = db.relationship(
        "Contact", backref="promotedorganizations", uselist=False)
    guardian = db.relationship(
        "Contact", backref="guardianedorganizations", uselist=False)
    parent_id = db.Column(db.String(4), db.ForeignKey(
        "organizations.organization_id"))
    owner = db.relationship('Organization', primaryjoin=(
        'Organization.parent_id==Organization.id'), backref='ownedusers', remote_side=id, uselist=False)

    def __str__(self):
        return self.name


class DealState(Enum):
    NEW, INTERESTED, CONFIRMED, WAITINGCLOSED, CLOSED = range(5)


class DealType(Enum):
    HOSTER, ITO, PTO, PREPTO = range(4)


class DealCurrency(Enum):
    USD, EUR, AED, GBP = range(4)


class Deal(db.Model, AdminLinksMixin):
    __tablename__ = "deals"
    id = db.Column('deal_id', db.String(
        4), default=generate_id, primary_key=True)
    # uid = db.Column(db.String(4))
    name = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.Text())  # should be markdown.
    amount = db.Column(db.Integer)  # default to int.
    currency = db.Column(db.Enum(DealCurrency), default=DealCurrency.EUR)
    deal_type = db.Column(db.Enum(DealType), default=DealType.HOSTER)
    deal_state = db.Column(db.Enum(DealState), default=DealState.NEW)

    isuser = db.Column(db.Boolean, default=False)
    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)
    closed_at = db.Column(db.TIMESTAMP, nullable=True)  # should be?

    # relations
    company_id = db.Column(db.String(4), db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.String(4), db.ForeignKey("contacts.contact_id"))

    tasks = db.relationship("Task", backref="deal")
    comments = db.relationship("Comment", backref="deal")
    messages = db.relationship("Message", backref="deal")
    links = db.relationship("Link", backref="deal")
    owner = db.relationship("Contact", backref="owneddeals", uselist=False)
    ownerbackup = db.relationship(
        "Contact", backref="backupowneddeals", uselist=False)

    def __str__(self):
        return self.name


#  manytomany through table.
class ContactsProjects(db.Model):
    __tablename__ = 'contacts_projects'
    id = db.Column(db.String(4), default=generate_id, primary_key=True)
    contact_id = db.Column(db.String(4), db.ForeignKey(
        'contacts.contact_id'))  # , ondelete='CASCADE'))
    project_id = db.Column(db.String(4), db.ForeignKey(
        'projects.project_id'))  # , ondelete='CASCADE'))


class Project(db.Model, AdminLinksMixin):
    __tablename__ = "projects"
    id = db.Column('project_id', db.String(
        4), default=generate_id, primary_key=True)
    # uid = db.Column(db.String(4))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.

    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP)
    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # relations
    comments = db.relationship("Comment", backref="project")
    links = db.relationship("Link", backref="project")

    tasks = db.relationship("Task", backref="project")
    sprint = db.relationship("Sprint", backref="projects")

    messages = db.relationship("Message", backref="project")
    users = db.relationship("Contact", secondary="contacts_projects",
                            backref=db.backref("projects"))

    contact_id = db.Column(db.String(4), db.ForeignKey("contacts.contact_id"))
    promoter = db.relationship(
        "Contact", backref="promotedprojects", uselist=False)
    guardian = db.relationship(
        "Contact", backref="guardiansprojects", uselist=False)

    # parent organization
    parent_id = db.Column(db.String(4), db.ForeignKey(
        "organizations.organization_id"))
    parent = db.relationship(
        'Organization', backref='childprojects', uselist=False)

    def percentage_done():
        pass

    def __str__(self):
        return self.name
# manytomany through table.


class ContactsSprints(db.Model):
    __tablename__ = 'contacts_sprints'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String(4), db.ForeignKey(
        'contacts.contact_id'))  # , ondelete='CASCADE'))
    sprint_id = db.Column(db.String(4), db.ForeignKey(
        'sprints.sprint_id'))  # , ondelete='CASCADE'))

    def __str__(self):
        return self.name


class Sprint(db.Model, AdminLinksMixin):
    __tablename__ = "sprints"
    id = db.Column('sprint_id', db.String(
        4), default=generate_id, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP)
    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # relations
    users = db.relationship("Contact", secondary="contacts_sprints",
                            backref=db.backref("sprints"))
    project_id = db.Column(db.String(4), db.ForeignKey("projects.project_id"))
    organization_id = db.Column(
        db.String(4), db.ForeignKey("organizations.organization_id"))
    tasks = db.relationship("Task", backref="sprint")
    comments = db.relationship("Comment", backref="sprint")
    links = db.relationship("Link", backref="sprint")
    messages = db.relationship("Message", backref="sprint")

    contact_id = db.Column(db.String(4), db.ForeignKey("contacts.contact_id"))
    promoter = db.relationship(
        "Contact", backref="promotedsprints", uselist=False)
    guardian = db.relationship(
        "Contact", backref="guardiansprints", uselist=False)

    # parent organization
    parent = db.relationship(
        'Organization', backref='childsprints', uselist=False)

    def percentage_done():
        pass

    def hours_open():
        pass

    def hours_open_person_avg():
        pass

    def hours_open_person_max():
        pass

    def __str__(self):
        return self.name


class Comment(db.Model, AdminLinksMixin):
    __tablename__ = "comments"
    id = db.Column('comment_id', db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.Text())  # should be markdown.
    content = db.Column(db.Text())  # should be markdown.

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # relations
    company_id = db.Column(db.String(4), db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.deal_id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.organization_id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.sprint_id"))
    link_id = db.Column(db.Integer, db.ForeignKey("links.link_id"))

    def __str__(self):
        return self.name


class Link(db.Model, AdminLinksMixin):
    __tablename__ = "links"
    id = db.Column('link_id', db.Integer,
                   primary_key=True)
    # uid = db.Column(db.String(4), default=generate_id, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    labels = db.Column(db.Text())  # should be markdown.

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # relations
    contact_id = db.Column(db.String, db.ForeignKey("contacts.contact_id"))
    deal_id = db.Column(db.String, db.ForeignKey("deals.deal_id"))
    task_id = db.Column(db.String, db.ForeignKey("tasks.task_id"))
    organization_id = db.Column(
        db.String, db.ForeignKey("organizations.organization_id"))
    project_id = db.Column(db.String, db.ForeignKey("projects.project_id"))
    sprint_id = db.Column(db.String, db.ForeignKey("sprints.sprint_id"))
    comments = db.relationship("Comment", backref="link")

    def __str__(self):
        return self.url


class TaskType(Enum):
    FEATURE, QUESTION, TASK, STORY, CONTACT = range(5)


class TaskPriority(Enum):
    MINOR, NORMAL, URGENT, CRITICAL = range(4)


class TaskAssignment(db.Model, AdminLinksMixin):
    __tablename__ = 'contacts_tasks'
    id = db.Column('taskassignment_id', db.Integer,
                   primary_key=True)

    # relations
    contact_id = db.Column(db.String, db.ForeignKey("contacts.contact_id"))
    task_id = db.Column(db.String, db.ForeignKey("tasks.task_id"))
    tasktracking_id = db.Column(
        db.String, db.ForeignKey("tasktrackings.tasktracking_id"))
    time_todo = db.Column(db.Integer, default=0)

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

        return '%s (%s)' % (self.task.title, self.contact.firstname + self.contact.lastname)


class Task(db.Model, AdminLinksMixin):
    __tablename__ = "tasks"
    id = db.Column('task_id', db.Integer,
                   primary_key=True)
    uid = db.Column(db.String(4))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    remarks = db.Column(db.Text())  # should be markdown.
    content = db.Column(db.Text())  # should be markdown.
    type = db.Column(db.Enum(TaskType), default=TaskType.FEATURE)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.MINOR)

    # time_done means time be spent on that task in hours
    deadline = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    eta = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    time_estimate = db.Column(db.Integer, default=0)  # in hours again
    time_done = db.Column(db.Integer, default=0)

    # relations
    company_id = db.Column(db.String, db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.String, db.ForeignKey("contacts.contact_id"))
    deal_id = db.Column(db.String, db.ForeignKey("deals.deal_id"))
    organization_id = db.Column(
        db.String, db.ForeignKey("organizations.organization_id"))
    project_id = db.Column(db.String, db.ForeignKey("projects.project_id"))
    sprint_id = db.Column(db.String, db.ForeignKey("sprints.sprint_id"))
    comments = db.relationship("Comment", backref="task")
    messages = db.relationship("Message", backref="task")
    links = db.relationship("Link", backref="task")
    contacts = db.relationship("Contact", secondary="contacts_tasks",
                               backref=db.backref("tasks"))
    assignments = db.relationship("TaskAssignment", backref="task")

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    def __str__(self):
        return self.title


class MessageChannel(Enum):
    TELEGRAM, EMAIL, SMS, INTERCOM = range(4)


class Message(db.Model, AdminLinksMixin):
    __tablename__ = "messages"
    id = db.Column('comment_id', db.Integer,
                   primary_key=True)
    uid = db.Column(db.String(4))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text())  # should be markdown.
    channel = db.Column(db.String(255))  # should be markdown.
    time_tosend = db.Column(db.TIMESTAMP)
    time_sent = db.Column(db.TIMESTAMP)

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    # relations
    company_id = db.Column(db.String, db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.String, db.ForeignKey("contacts.contact_id"))
    deal_id = db.Column(db.String, db.ForeignKey("deals.deal_id"))
    task_id = db.Column(db.String, db.ForeignKey("tasks.task_id"))
    organization_id = db.Column(
        db.String, db.ForeignKey("organizations.organization_id"))
    project_id = db.Column(db.String, db.ForeignKey("projects.project_id"))
    sprint_id = db.Column(db.String, db.ForeignKey("sprints.sprint_id"))

    def __str__(self):
        return self.title


class TaskTracking(db.Model, AdminLinksMixin):
    __tablename__ = "tasktrackings"
    id = db.Column('tasktracking_id', db.String(
        4), default=generate_id, primary_key=True)

    assignment = db.relationship("TaskAssignment",
                                 backref=db.backref("tasktracking"), uselist=False)
    remarks = db.Column(db.Text())  # should be markdown.
    time_done = db.Column(db.Integer, default=0)

    def __str__(self):
        return "<TaskTracker %s>" % (self.id)

    # epoch = models.IntegerField(
    #     blank=True,
    #     validators=[validate_epoch]
    # )
