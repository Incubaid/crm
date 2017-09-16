from enum import Enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listen
import string
import random


db = SQLAlchemy()  # init later in app.py
db.session.autocommit = True


def generate_id(mapper, connect, target):
    target.generate_id()

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
        print("##GENID:%s"%self)
        if not self.id:            
            while True:
                uid = self._newuid()
                currentobjs = self.query.filter_by(id=uid)
                if currentobjs.count() == 0:
                    self.id = uid
                    return


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
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.id"))
    company_id = db.Column(db.String(5), db.ForeignKey("companies.id"))
    user_id = db.Column(db.String(5), db.ForeignKey("users.id"))

    def __str__(self):
        return self.number


class Email(db.Model, AdminLinksMixin,Base):
    __tablename__ = "emails"
    email = db.Column(db.String(150), nullable=False)
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.id"))
    company_id = db.Column(db.String(5), db.ForeignKey("companies.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    organization_id = db.Column(db.String(5), db.ForeignKey("organizations.id"))

    def __str__(self):
        return self.email


class Contact(db.Model, AdminLinksMixin, Base):
    __tablename__ = "contacts"
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15))
    description = db.Column(db.Text())  # should be markdown.
    message_channels = db.Column(db.String(20), default="")

    # relations
    telephones = db.relationship("Telephone", backref="contact")
    emails = db.relationship("Email", backref="contact")
    deals = db.relationship("Deal", backref="contact")
    comments = db.relationship("Comment", backref="contact")
    tasks = db.relationship("Task", backref="contact")
    messages = db.relationship("Message", backref="contact")
    links = db.relationship("Link", backref="contact")


    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

class User(db.Model, AdminLinksMixin, Base):
    __tablename__ = "users"

    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15))
    description = db.Column(db.Text())  # should be markdown.
    message_channels = db.Column(db.String(10), default="")

    # relations
    telephones = db.relationship("Telephone", backref="user")
    emails = db.relationship("Email", backref="user")

    organizations = db.relationship("UsersOrganizations", backref="users")

    comments = db.relationship("Comment", backref="user")
    messages = db.relationship("Message", backref="user")
    links = db.relationship("Link", backref="user")

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


class CompaniesContacts(db.Model, AdminLinksMixin,Base):
    __tablename__ = 'companies_contacts'
    company_id = db.Column(db.String(5), db.ForeignKey('companies.id'))  # , ondelete='CASCADE'))
    contact_id = db.Column(db.String(5), db.ForeignKey('contacts.id'))  # , ondelete='CASCADE'))


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

    contacts = db.relationship("Contact", secondary="companies_contacts",
        backref=db.backref("companies"), lazy="dynamic")

    def __str__(self):
        return self.name


#  manytomany through table.
class UsersOrganizations(db.Model, AdminLinksMixin,Base):
    __tablename__ = 'users_organizations'
    user_id = db.Column(db.String(5), db.ForeignKey('users.id'))  # , ondelete='CASCADE'))
    organization_id = db.Column(db.String(5), db.ForeignKey('organizations.id'))  # , ondelete='CASCADE'))

class UsersSprints(db.Model, AdminLinksMixin,Base):
    __tablename__ = 'users_sprints'
    user_id = db.Column(db.String(5), db.ForeignKey('users.id'))  # , ondelete='CASCADE'))
    sprint_id = db.Column(db.String(5), db.ForeignKey('sprints.id'))  # , ondelete='CASCADE'))


class Organization(db.Model, AdminLinksMixin, Base):
    __tablename__ = "organizations"

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.

#     #relations
    emails = db.relationship("Email", backref="organization")
    tasks = db.relationship("Task", backref="organization")
    comments = db.relationship("Comment", backref="organization")
    
    users = db.relationship("User", secondary="users_organizations",
        backref=db.backref("organizationss"), lazy="dynamic")

    links = db.relationship("Link", backref="organization")
    messages = db.relationship("Message", backref="organization")

    parent_id = db.Column(db.String(5), db.ForeignKey("organizations.id"))

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
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    amount = db.Column(db.Integer)  # default to int.
    currency = db.Column(db.Enum(DealCurrency), default=DealCurrency.EUR)
    deal_type = db.Column(db.Enum(DealType), default=DealType.HOSTER)
    deal_state = db.Column(db.Enum(DealState), default=DealState.NEW)

    closed_at = db.Column(db.TIMESTAMP, nullable=True)  # should be?

    # relations
    company_id = db.Column(db.String(5), db.ForeignKey("companies.id"))
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.id"))

    tasks = db.relationship("Task", backref="deal")
    comments = db.relationship("Comment", backref="deal")
    messages = db.relationship("Message", backref="deal")
    links = db.relationship("Link", backref="deal")

    def __str__(self):
        return self.name


#  manytomany through table.
class UsersProjects(db.Model,Base):
    __tablename__ = 'users_projects'
    user_id = db.Column(db.String(5), db.ForeignKey('users.id'))  # , ondelete='CASCADE'))
    project_id = db.Column(db.String(5), db.ForeignKey('projects.id'))  # , ondelete='CASCADE'))

class ContactsProjects(db.Model,Base):
    __tablename__ = 'contacts_projects'
    contact_id = db.Column(db.String(5), db.ForeignKey('contacts.id'))  # , ondelete='CASCADE'))
    project_id = db.Column(db.String(5), db.ForeignKey('projects.id'))  # , ondelete='CASCADE'))


class Project(db.Model, AdminLinksMixin, Base):
    __tablename__ = "projects"

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.

    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP)

    # relations
    comments = db.relationship("Comment", backref="project")
    links = db.relationship("Link", backref="project")

    tasks = db.relationship("Task", backref="project")

    messages = db.relationship("Message", backref="project")

    # users = db.relationship("User", secondary="users_projects",backref=db.backref("users"))

    contacts = db.relationship("Contact", secondary="contacts_projects",backref=db.backref("contacts"))

    # #promotor/guardian
    # promoter = db.relationship("User", backref="promotedprojects", uselist=False)
    # guardian = db.relationship("User", backref="guardiansprojects", uselist=False)

    def percentage_done():
        pass

    def __str__(self):
        return self.name


class Sprint(db.Model, AdminLinksMixin, Base):
    __tablename__ = "sprints"
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP)

    # relations
    # users = db.relationship("User", secondary="users_sprints",backref=db.backref("userss"))

    tasks = db.relationship("Task", backref="sprint")
    comments = db.relationship("Comment", backref="sprint")
    links = db.relationship("Link", backref="sprint")
    messages = db.relationship("Message", backref="sprint")

    
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


class Comment(db.Model, AdminLinksMixin,Base):
    __tablename__ = "comments"

    content = db.Column(db.Text())  # should be markdown.

    # relations
    company_id = db.Column(db.String(5), db.ForeignKey("companies.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    link_id = db.Column(db.Integer, db.ForeignKey("links.id"))

    def __str__(self):
        return self.content


class Link(db.Model, AdminLinksMixin,Base):
    __tablename__ = "links"

    url = db.Column(db.String(255), nullable=False)
    labels = db.Column(db.Text())  

    # relations
    contact_id = db.Column(db.String, db.ForeignKey("contacts.id"))
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    deal_id = db.Column(db.String, db.ForeignKey("deals.id"))
    task_id = db.Column(db.String, db.ForeignKey("tasks.id"))
    organization_id = db.Column(db.String, db.ForeignKey("organizations.id"))
    project_id = db.Column(db.String, db.ForeignKey("projects.id"))
    sprint_id = db.Column(db.String, db.ForeignKey("sprints.id"))

    comments = db.relationship("Comment", backref="link")

    def __str__(self):
        return self.url


class TaskType(Enum):
    FEATURE, QUESTION, TASK, STORY, CONTACT = range(5)


class TaskPriority(Enum):
    MINOR, NORMAL, URGENT, CRITICAL = range(4)

class TaskState(Enum):
    NEW, PROGRESS, QUESTION, VERIFICATION, CLOSED = range(5)

class Task(db.Model, AdminLinksMixin, Base):
    __tablename__ = "tasks"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    type = db.Column(db.Enum(TaskType), default=TaskType.FEATURE)
    priority = db.Column(db.Enum(TaskPriority), default=TaskPriority.MINOR)
    state = db.Column(db.Enum(TaskState), default=TaskState.NEW)
    
    assignment_id = db.Column(db.String, db.ForeignKey("users.id"))

    deadline = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    eta = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    time_estimate = db.Column(db.Integer, default=0)  # in hours again
    time_done = db.Column(db.Integer, default=0)

    # relations
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    contact_id = db.Column(db.String, db.ForeignKey("contacts.id"))
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    deal_id = db.Column(db.String, db.ForeignKey("deals.id"))
    organization_id = db.Column(db.String, db.ForeignKey("organizations.id"))
    project_id = db.Column(db.String, db.ForeignKey("projects.id"))
    sprint_id = db.Column(db.String, db.ForeignKey("sprints.id"))

    comments = db.relationship("Comment", backref="task")
    messages = db.relationship("Message", backref="task")
    links = db.relationship("Link", backref="task")

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



# class MessageChannel(Enum):
#     TELEGRAM, EMAIL, SMS, INTERCOM = range(4)


class Message(db.Model, AdminLinksMixin,Base):
    __tablename__ = "messages"
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text())  # should be markdown.
    channel = db.Column(db.String(255))  # should be markdown.
    time_tosend = db.Column(db.TIMESTAMP)
    time_sent = db.Column(db.TIMESTAMP)

    # relations
    company_id = db.Column(db.String, db.ForeignKey("companies.id"))
    contact_id = db.Column(db.String, db.ForeignKey("contacts.id"))
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    deal_id = db.Column(db.String, db.ForeignKey("deals.id"))
    task_id = db.Column(db.String, db.ForeignKey("tasks.id"))
    organization_id = db.Column(
        db.String, db.ForeignKey("organizations.id"))
    project_id = db.Column(db.String, db.ForeignKey("projects.id"))
    sprint_id = db.Column(db.String, db.ForeignKey("sprints.id"))

    def __str__(self):
        return self.title


class TaskTracking(db.Model, AdminLinksMixin,Base):
    __tablename__ = "tasktrackings"

    remarks = db.Column(db.Text())  # should be markdown.
    time_done = db.Column(db.Integer, default=0)

    def __str__(self):
        return "<TaskTracker %s>" % (self.id)


for m in [Telephone,Email,Contact, User, Company,CompaniesContacts,UsersOrganizations, Comment, Link, \
         UsersSprints,Organization, Deal,UsersProjects, ContactsProjects, Project, Sprint, Task, User, \
         Message, TaskTracking]:
    listen(m, 'before_insert', generate_id)
