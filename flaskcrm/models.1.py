from enum import Enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listen
import string
import random


db = SQLAlchemy()  # init later in app.py
db.session.autocommit = True


# def generate_id(mapper, connect, target):
#     target.generate_id()


class Base:

    id = db.Column(db.String(5), primary_key=True)
    

    # timestamps
    created_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)    

    def _newuid(self):
        uid = ''.join(random.sample(string.ascii_lowercase + string.digits, 5))
        return uid

    def generate_id(self):
        if not self.id:
            uid = self._newuid()
            while True:
                currentobjs = self.query.filter_by(id=uid)
                if currentobjs.count() == 0:
                    self.id = uid
                    # self.uid = uid
                    return
                uid = self._newuid()


class AdminLinksMixin:
    ADMIN_EDIT_LINK = "/{modelname}/edit/?id={modelid}"
    #&url=/{modelname}/"
    ADMIN_LIST_LINK = "/{modelname}/"
    # &url=/{modelname}/"
    ADMIN_VIEW_LINK = "/{modelname}/details/?id={modelid}"
    ADMIN_CREATE_LINK = "/{modelname}/new/?id={modelid}"  # &url=/{modelname}/"

    ADMIN_EDIT_LINK_MODAL = "/{modelname}/edit/?id={modelid}"  # &modal=True"
    # &modal=True"
    ADMIN_VIEW_LINK_MODAL = "/{modelname}/details/?id={modelid}"
    ADMIN_CREATE_LINK_MODAL = "/{modelname}/new/?url=/{modelname}"

    def admin_list_link(self):
        modelname = self.__class__.__name__.lower()
        return AdminLinksMixin.ADMIN_LIST_LINK.format(modelname=modelname)

    def admin_edit_link(self):
        modelname = self.__class__.__name__.lower()
        return AdminLinksMixin.ADMIN_EDIT_LINK.format(modelname=modelname, modelid=self.id)

    def admin_view_link(self):
        modelname = self.__class__.__name__.lower()

        return AdminLinksMixin.ADMIN_VIEW_LINK.format(modelname=modelname, modelid=self.id)

    def admin_create_link(self):
        modelname = self.__class__.__name__.lower()

        return AdminLinksMixin.ADMIN_CREATE_LINK.format(modelname=modelname, modelid=self.id)

    def admin_edit_link_modal(self):
        modelname = self.__class__.__name__.lower()
        return AdminLinksMixin.ADMIN_EDIT_LINK_MODAL.format(modelname=modelname, modelid=self.id)

    def admin_view_link_modal(self):
        modelname = self.__class__.__name__.lower()
        return AdminLinksMixin.ADMIN_VIEW_LINK_MODAL.format(modelname=modelname, modelid=self.id)

    def admin_create_link_modal(self):
        modelname = self.__class__.__name__.lower()

        return AdminLinksMixin.ADMIN_CREATE_LINK_MODAL.format(modelname=modelname, modelid=self.id)

    @property
    def uid(self):
        return self.id


class Telephone(db.Model, AdminLinksMixin,Base):
    __tablename__ = "telephones"
    number = db.Column(db.String(20), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __str__(self):
        return self.number


class Email(db.Model, AdminLinksMixin,Base):
    __tablename__ = "emails"
    email = db.Column(db.String(255), nullable=False)
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.contact_id"))
    company_id = db.Column(db.String(5), db.ForeignKey("companies.company_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    organization_id = db.Column(
        db.String(5), db.ForeignKey("organizations.organization_id"))

    def __str__(self):
        return self.email


class Contact(db.Model, AdminLinksMixin, Base):
    __tablename__ = "contacts"
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15))
    description = db.Column(db.Text())  # should be markdown.
    message_channels = db.Column(db.String(10), default="")

    # relations
    telephones = db.relationship("Telephone", backref="contact")
    emails = db.relationship("Email", backref="contact")

    deals = db.relationship("Deal", backref="contact")
    comments = db.relationship("Comment", backref="contact")
    # tasks = db.relationship("Task", backref="assignee")
    messages = db.relationship("Message", backref="contact")
    links = db.relationship("Link", backref="contact")

    # owner_id = db.Column(db.String(5), db.ForeignKey("users.user_id"))
    # owner = db.relationship('User', primaryjoin=(
    #     'Contact.owner_id==User.id'), backref='ownedusers', remote_side=id, uselist=False)

    # ownerbackup_id = db.Column(
    #     db.String(5), db.ForeignKey("users.user_id"))
    # ownerbackup = db.relationship('Contact', primaryjoin=(
    #     'Contact.ownerbackup_id==Contact.id'), backref='backupownedusers', remote_side=id, uselist=False)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

class User(db.Model, AdminLinksMixin, Base):
    __tablename__ = "users"
    id = db.Column('user_id', db.String(
        5), primary_key=True)
    uid = db.Column(db.String(5))
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15))
    description = db.Column(db.Text())  # should be markdown.
    message_channels = db.Column(db.String(10), default="")

    # relations
    telephones = db.relationship("Telephone", backref="user")
    emails = db.relationship("Email", backref="user")

    organizations = db.relationship("UsersOrganizations", backref="user_id")

    comments = db.relationship("Comment", backref="user")
    # tasks = db.relationship("Task", backref="assignee")
    messages = db.relationship("Message", backref="user")
    links = db.relationship("Link", backref="user")

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

class Company(db.Model, AdminLinksMixin, Base):
    __tablename__ = "companies"
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.


    # relations
    telephones = db.relationship("Telephone", backref="company")
    emails = db.relationship("Email", backref="company")
    deals = db.relationship("Deal", backref="company")
    messages = db.relationship("Message", backref="company")
    tasks = db.relationship("Task", backref="company")
    comments = db.relationship("Comment", backref="company")

    contact_id = db.Column(db.String(5), db.ForeignKey("users.user_id"))


    # owner_id = db.Column(db.String(5), db.ForeignKey("users.user_id"))
    # owner = db.relationship('User', primaryjoin=(
    #     'Contact.owner_id==User.id'), backref='ownedusers', remote_side=id, uselist=False)

    # ownerbackup_id = db.Column(
    #     db.String(5), db.ForeignKey("users.user_id"))
    # ownerbackup = db.relationship('Contact', primaryjoin=(
    #     'Contact.ownerbackup_id==Contact.id'), backref='backupownedusers', remote_side=id, uselist=False)


    def __str__(self):
        return self.name


#  manytomany through table.
class UsersOrganizations(db.Model, AdminLinksMixin):
    __tablename__ = 'users_organizations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(5), db.ForeignKey(
        'users.user_id'))  # , ondelete='CASCADE'))
    organization_id = db.Column(db.String(5), db.ForeignKey(
        'organizations.organization_id'))  # , ondelete='CASCADE'))

class UsersSprints(db.Model, AdminLinksMixin):
    __tablename__ = 'users_sprints'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(5), db.ForeignKey(
        'users.user_id'))  # , ondelete='CASCADE'))
    sprint_id = db.Column(db.String(5), db.ForeignKey(
        'sprints.sprint_id'))  # , ondelete='CASCADE'))


class Organization(db.Model, AdminLinksMixin, Base):
    __tablename__ = "organizations"
    id = db.Column('organization_id', db.String(
        5), primary_key=True)
    uid = db.Column(db.String(5))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.

#     #relations
    emails = db.relationship("Email", backref="organization")
    users = db.relationship("User", backref="organization")
    tasks = db.relationship("Task", backref="organization")
    comments = db.relationship("Comment", backref="organization")
    # users = db.relationship("Contact", secondary="contacts_organizations",
    # backref=db.backref("organizations"), lazy="dynamic")

    links = db.relationship("Link", backref="organization")
    messages = db.relationship("Message", backref="organization")
    # sprints = db.relationship("Sprint", backref="organization")
    # promoter = db.relationship(
    #     "Contact", backref="promotedorganizations", uselist=False)
    # guardian = db.relationship(
    #     "Contact", backref="guardianedorganizations", uselist=False)
    parent_id = db.Column(db.String(5), db.ForeignKey(
        "organizations.organization_id"))
    parent = db.relationship('Organization', primaryjoin=(
        'Organization.parent_id==Organization.id'), backref='organizationparent', remote_side=id, uselist=False)

    def __str__(self):
        return self.name


class DealState(Enum):
    NEW, INTERESTED, CONFIRMED, WAITINGCLOSED, CLOSED = range(5)


class DealType(Enum):
    HOSTER, ITO, PTO, AMBASSADOR = range(4)


class DealCurrency(Enum):
    USD, EUR, AED, GBP = range(4)


class Deal(db.Model, AdminLinksMixin, Base):
    __tablename__ = "deals"
    id = db.Column('deal_id', db.String(
        5), primary_key=True)
    uid = db.Column(db.String(5))
    name = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.Text())  # should be markdown.
    amount = db.Column(db.Integer)  # default to int.
    currency = db.Column(db.Enum(DealCurrency), default=DealCurrency.EUR)
    deal_type = db.Column(db.Enum(DealType), default=DealType.HOSTER)
    deal_state = db.Column(db.Enum(DealState), default=DealState.NEW)

    closed_at = db.Column(db.TIMESTAMP, nullable=True)  # should be?

    # relations
    company_id = db.Column(db.String(5), db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.contact_id"))

    tasks = db.relationship("Task", backref="deal")
    comments = db.relationship("Comment", backref="deal")
    messages = db.relationship("Message", backref="deal")
    links = db.relationship("Link", backref="deal")
    # owner = db.relationship("User", backref="owneddeals", uselist=False)
    # ownerbackup = db.relationship(
    #     "User", backref="backupowneddeals", uselist=False)

    def __str__(self):
        return self.name


#  manytomany through table.
class UsersProjects(db.Model):
    __tablename__ = 'users_projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(5), db.ForeignKey(
        'users.user_id'))  # , ondelete='CASCADE'))
    project_id = db.Column(db.String(5), db.ForeignKey(
        'projects.project_id'))  # , ondelete='CASCADE'))


class Project(db.Model, AdminLinksMixin, Base):
    __tablename__ = "projects"
    id = db.Column('project_id', db.String(
        5), primary_key=True)
    uid = db.Column(db.String(5))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.

    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP)

    # relations
    comments = db.relationship("Comment", backref="project")
    links = db.relationship("Link", backref="project")

    tasks = db.relationship("Task", backref="project")
    sprint = db.relationship("Sprint", backref="projects")

    messages = db.relationship("Message", backref="project")
    users = db.relationship("User", secondary="users_projects",
                            backref=db.backref("user"))

    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.contact_id"))
    promoter = db.relationship(
        "User", backref="promotedprojects", uselist=False)
    guardian = db.relationship(
        "User", backref="guardiansprojects", uselist=False)

    # parent organization
    parent_id = db.Column(db.String(5), db.ForeignKey(
        "organizations.organization_id"))
    parent = db.relationship(
        'Organization', backref='childprojects', uselist=False)

    def percentage_done():
        pass

    def __str__(self):
        return self.name
# manytomany through table.


class Sprint(db.Model, AdminLinksMixin, Base):
    __tablename__ = "sprints"
    id = db.Column('sprint_id', db.String(
        4), primary_key=True)
    uid = db.Column(db.String(5))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP)

    # relations
    users = db.relationship("Users", secondary="users_sprints",
                            backref=db.backref("users"))
    tasks = db.relationship("Task", backref="sprint")
    comments = db.relationship("Comment", backref="sprint")
    links = db.relationship("Link", backref="sprint")
    messages = db.relationship("Message", backref="sprint")

    # owner = db.relationship(
    #     "User", backref="ownersprints", uselist=False)
    
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
    content = db.Column(db.Text())  # should be markdown.

    # relations
    company_id = db.Column(db.String(5), db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
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
    url = db.Column(db.String(255), nullable=False)
    labels = db.Column(db.Text())  

    # relations
    contact_id = db.Column(db.String, db.ForeignKey("contacts.contact_id"))
    user_id = db.Column(db.String, db.ForeignKey("users.user_id"))
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


# class ContactsTasks(db.Model, AdminLinksMixin):
#     __tablename__ = 'contacts_tasks'
#     id = db.Column('taskassignment_id', db.Integer,
#                    primary_key=True)

#     # relations
#     contact_id = db.Column(db.String, db.ForeignKey("users.user_id"))
#     task_id = db.Column(db.String, db.ForeignKey("tasks.task_id"))

# class TaskAssignment(db.Model, AdminLinksMixin):
#     __tablename__ = 'taskassignments'
#     id = db.Column('taskassignment_id', db.Integer,
#                    primary_key=True)

#     # relations
#     contact_id = db.Column(db.String, db.ForeignKey("users.user_id"))
#     task_id = db.Column(db.String, db.ForeignKey("tasks.task_id"))
#     tasktracking_id = db.Column(
#         db.Integer, db.ForeignKey("tasktrackings.tasktracking_id"))




#     def __str__(self):

#         return '%s (%s)' % (self.task.title, self.contact.firstname + self.contact.lastname)

class TaskState(Enum):
    NEW, PROGRESS, QUESTION, VERIFICATION, CLOSED = range(5)

class Task(db.Model, AdminLinksMixin, Base):
    __tablename__ = "tasks"
    id = db.Column('task_id', db.String(
        4), primary_key=True, unique=True)
    uid = db.Column(db.String(5))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    type = db.Column(db.Enum(TaskType), default=TaskType.FEATURE)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.MINOR)
    task_state = db.Column(db.Enum(DealState), default=TaskState.NEW)
    
    assignment_id = db.Column(db.String, db.ForeignKey("users.user_id"))

    deadline = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    eta = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    time_estimate = db.Column(db.Integer, default=0)  # in hours again
    time_done = db.Column(db.Integer, default=0)

    # relations
    company_id = db.Column(db.String, db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.String, db.ForeignKey("users.user_id"))
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


    # assignments = db.relationship("TaskAssignment", backref="task")

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


class MessageChannel(Enum):
    TELEGRAM, EMAIL, SMS, INTERCOM = range(4)


class Message(db.Model, AdminLinksMixin):
    __tablename__ = "messages"
    id = db.Column('comment_id', db.Integer,
                   primary_key=True)
    uid = db.Column(db.String(5))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text())  # should be markdown.
    channel = db.Column(db.String(255))  # should be markdown.
    time_tosend = db.Column(db.TIMESTAMP)
    time_sent = db.Column(db.TIMESTAMP)

    # relations
    company_id = db.Column(db.String, db.ForeignKey("companies.company_id"))
    contact_id = db.Column(db.String, db.ForeignKey("contacts.contact_id"))
    user_id = db.Column(db.String, db.ForeignKey("users.user_id"))
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
    id = db.Column('tasktracking_id', db.Integer, primary_key=True)

    assignment = db.relationship("TaskAssignment",
                                 backref=db.backref("tasktracking"), uselist=False)
    remarks = db.Column(db.Text())  # should be markdown.
    time_done = db.Column(db.Integer, default=0)

    def __str__(self):
        return "<TaskTracker %s>" % (self.id)


for m in [Contact, Company, Organization, Deal, Project, Sprint, Task,User]:
    listen(m, 'before_insert', generate_id)
