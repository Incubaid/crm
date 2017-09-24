from enum import Enum
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listen
import string
import random


db = SQLAlchemy()  # init later in app.py
db.session.autocommit = True


def generate_id(mapper, connect, target):
    target.generate_id()

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


class Base(AdminLinksMixin):

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
        print("##GENID:{}".format(str(self)))
        if not self.id:            
            while True:
                uid = self._newuid()
                currentobjs = self.query.filter_by(id=uid)
                if currentobjs.count() == 0:
                    self.id = uid
                    return

    def as_dict(self, resolve_refs=True):

        d = {
            'datetime_fields': []
        }

        for c in self.__table__.columns:
            k = c.name
            v = getattr(self, c.name)
            d[k] = v

            # ujson only serialize datetimes into epoch
            if isinstance(v, datetime) or isinstance(v, date):
                d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
                d['datetime_fields'].append(k)
            # translate F.Ks to dicts
            elif c.foreign_keys and resolve_refs:
                if getattr(self, k):
                    k = k.replace('_id', '')
                    v = getattr(self, k)
                    if v:
                        d[k] = v.as_dict(resolve_refs=False)
        # list backrefs
        if resolve_refs:
            from sqlalchemy import inspect
            backrefs = set(inspect(self.__class__).attrs.keys()) - set([c.name for c in self.__table__.columns])
            for backref in  backrefs:
                d[backref] = d.get(backref, [])
                v = getattr(self, backref)
                try:
                    for item in v:
                            d[backref].append(item.as_dict(resolve_refs=False))
                except TypeError:
                    # not iterable
                    pass



        return d

    @property
    def short_description(self):
        if hasattr(self, "description"):
            return "\n".join(self.description.splitlines()[:3])

    @property
    def short_content(self):
        if hasattr(self, "content"):
            return "\n".join(self.content.splitlines()[:3])


    @property
    def created_at_short(self):
        return self.created_at.strftime("%Y-%m-%d")
 
    @property
    def updated_at_short(self):
        return self.updated_at.strftime("%Y-%m-%d")
 
class Telephone(db.Model, Base):
    __tablename__ = "telephones"
    number = db.Column(db.String(20), nullable=False)
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.id"))
    company_id = db.Column(db.String(5), db.ForeignKey("companies.id"))
    user_id = db.Column(db.String(5), db.ForeignKey("users.id"))

    def __str__(self):
        return self.number


class Email(db.Model, Base):
    __tablename__ = "emails"
    email = db.Column(db.String(150), nullable=False)
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.id"))
    company_id = db.Column(db.String(5), db.ForeignKey("companies.id"))
    user_id = db.Column(db.String(5), db.ForeignKey("users.id"))
    organization_id = db.Column(db.String(5), db.ForeignKey("organizations.id"))

    def __str__(self):
        return self.email


class Contact(db.Model, Base):
    __tablename__ = "contacts"
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255))
    description = db.Column(db.Text()) 
    message_channels = db.Column(db.String(255), default="")

    # relations
    telephones = db.relationship("Telephone", backref="contact")
    emails = db.relationship("Email", backref="contact")
    deals = db.relationship("Deal", backref="contact")
    comments = db.relationship("Comment", backref="contact")
    tasks = db.relationship("Task", backref="contact")
    messages = db.relationship("Message", backref="contact")
    links = db.relationship("Link", backref="contact")

    owner_id = db.Column(db.String(5), db.ForeignKey('users.id')) 
    ownerbackup_id = db.Column(db.String(5), db.ForeignKey('users.id')) 
    parent_id = db.Column(db.String(5), db.ForeignKey('users.id'))

    def as_dict(self, *args, **kwargs):
        d = super(Contact, self).as_dict(*args, **kwargs)
        # d['emails'] = [e.email for e in self.emails]
        # d['telephones'] = [t.number for t in self.telephones]
        # d['messages'] = [m.message for m in self.messages]
        # d['tasks'] = [m.message for m in self.messages]
        return d

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)


class CompaniesContacts(db.Model):
    __tablename__ = 'companies_contacts'
    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.String(5), db.ForeignKey('companies.id')) 
    contact_id = db.Column(db.String(5), db.ForeignKey('contacts.id')) 


class Company(db.Model, Base):
    __tablename__ = "companies"
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    vatnumber = db.Column(db.String(255))
    website = db.Column(db.String(255))
    # relations
    telephones = db.relationship("Telephone", backref="company")
    emails = db.relationship("Email", backref="company")
    deals = db.relationship("Deal", backref="company")
    messages = db.relationship("Message", backref="company")
    tasks = db.relationship("Task", backref="company")
    comments = db.relationship("Comment", backref="company")
    contacts = db.relationship("Contact", secondary="companies_contacts",backref="companies")

    owner_id = db.Column(db.String(5), db.ForeignKey('users.id')) 
    ownerbackup_id = db.Column(db.String(5), db.ForeignKey('users.id'))

    def __str__(self):
        return self.name


class User(db.Model, Base):
    __tablename__ = "users"

    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255))
    description = db.Column(db.Text())  # should be markdown.
    message_channels = db.Column(db.String(255), default="")

    # relations
    telephones = db.relationship("Telephone", backref="user")
    emails = db.relationship("Email", backref="user")

    # organizations = db.relationship("UsersOrganizations", backref="users")

    comments = db.relationship("Comment", backref="user")
    messages = db.relationship("Message", backref="user")
    links = db.relationship("Link", backref="user")

    ownsContacts = db.relationship("Contact", backref="owner", primaryjoin=("User.id==Contact.owner_id"))
    ownsAsBackupContacts = db.relationship("Contact", backref="ownerbackup", primaryjoin="User.id==Contact.ownerbackup_id")

    ownsCompanies = db.relationship("Company", backref="owner", primaryjoin=("User.id==Company.owner_id"))
    ownsAsBackupCompanies = db.relationship("Company", backref="ownerbackup", primaryjoin="User.id==Company.ownerbackup_id")

    ownsOrganizations = db.relationship("Organization", backref="owner", primaryjoin=("User.id==Organization.owner_id"))
    ownsSprints = db.relationship("Sprint", backref="owner", primaryjoin=("User.id==Sprint.owner_id"))

    promoterProjects = db.relationship("Project", backref="promoter", primaryjoin="User.id==Project.promoter_id")
    guardianProjects = db.relationship("Project", backref="guardian", primaryjoin="User.id==Project.guardian_id")

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

#  manytomany through table.
class UsersOrganizations(db.Model):
    __tablename__ = 'users_organizations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(5), db.ForeignKey('users.id'))
    organization_id = db.Column(db.String(5), db.ForeignKey('organizations.id')) 

class UsersSprints(db.Model, Base):
    __tablename__ = 'users_sprints'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(5), db.ForeignKey('users.id'))
    sprint_id = db.Column(db.String(5), db.ForeignKey('sprints.id')) 

class ContactsSprints(db.Model, Base):
    __tablename__ = 'contacts_sprints'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String(5), db.ForeignKey('contacts.id'))
    sprint_id = db.Column(db.String(5), db.ForeignKey('sprints.id')) 



class Organization(db.Model, Base):
    __tablename__ = "organizations"

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.


    emails = db.relationship("Email", backref="organization")
    tasks = db.relationship("Task", backref="organization")
    comments = db.relationship("Comment", backref="organization")
    
    users = db.relationship("User", secondary="users_organizations",
        backref=db.backref("organizations"))

    links = db.relationship("Link", backref="organization")
    messages = db.relationship("Message", backref="organization")

    owner_id = db.Column(db.String(5), db.ForeignKey('users.id')) 
    parent_id = db.Column(db.String(5), db.ForeignKey("organizations.id"))


    def __str__(self):
        return self.name


class DealState(Enum):
    NEW, INTERESTED, CONFIRMED, PENDING, CLOSED = range(5)


class DealType(Enum):
    HOSTER, ITO, PTO, AMBASSADOR = range(4)


class DealCurrency(Enum):
    USD, EUR, AED, GBP = range(4)


class Deal(db.Model, Base):
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
class UsersProjects(db.Model, Base):
    __tablename__ = 'users_projects'
    user_id = db.Column(db.String(5), db.ForeignKey('users.id')) 
    project_id = db.Column(db.String(5), db.ForeignKey('projects.id'))

class ContactsProjects(db.Model, Base):
    __tablename__ = 'contacts_projects'
    contact_id = db.Column(db.String(5), db.ForeignKey('contacts.id'))
    project_id = db.Column(db.String(5), db.ForeignKey('projects.id'))


class Project(db.Model, Base):
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

    sprint_id = db.Column(db.String(5), db.ForeignKey('sprints.id')) 
    sprints = db.relationship("Sprint", backref="project", primaryjoin=("Project.id==Sprint.project_id"))
    # users = db.relationship("User", secondary="users_projects",backref=db.backref("users"))
    contacts = db.relationship("Contact", secondary="contacts_projects",backref=db.backref("projects"))

    # #promoter/guardian
    promoter_id = db.Column(db.String(5), db.ForeignKey('users.id')) 
    guardian_id = db.Column(db.String(5), db.ForeignKey('users.id')) 

    def percentage_done():
        pass

    def __str__(self):
        return self.name


class Sprint(db.Model, Base):
    __tablename__ = "sprints"
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())  # should be markdown.
    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP)

    # relations
    # users = db.relationship("User", secondary="users_sprints",backref=db.backref("userss"))
    contacts = db.relationship("Contact", secondary="contacts_sprints",backref="sprints")

    tasks = db.relationship("Task", backref="sprint")
    comments = db.relationship("Comment", backref="sprint")
    links = db.relationship("Link", backref="sprint")
    messages = db.relationship("Message", backref="sprint")

    owner_id = db.Column(db.String(5), db.ForeignKey('users.id')) 
    project_id = db.Column(db.String(5), db.ForeignKey('projects.id')) 

    
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


class Comment(db.Model, Base):
    __tablename__ = "comments"

    content = db.Column(db.Text())  # should be markdown.

    # relations
    company_id = db.Column(db.String(5), db.ForeignKey("companies.id"))
    contact_id = db.Column(db.String(5), db.ForeignKey("contacts.id"))
    user_id = db.Column(db.String(5), db.ForeignKey("users.id"))
    deal_id = db.Column(db.String(5), db.ForeignKey("deals.id"))
    task_id = db.Column(db.String(5), db.ForeignKey("tasks.id"))
    organization_id = db.Column(db.String(5), db.ForeignKey("organizations.id"))
    project_id = db.Column(db.String(5), db.ForeignKey("projects.id"))
    sprint_id = db.Column(db.String(5), db.ForeignKey("sprints.id"))
    link_id = db.Column(db.String(5), db.ForeignKey("links.id"))

    def __str__(self):
        return self.content


class Link(db.Model, Base):
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

class Task(db.Model, Base):
    __tablename__ = "tasks"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text())
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


class Message(db.Model, Base):
    __tablename__ = "messages"
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text()) 
    channel = db.Column(db.String(255)) 
    time_tosend = db.Column(db.TIMESTAMP)
    time_sent = db.Column(db.TIMESTAMP)
    author = db.relationship("User", backref="createdMessages", uselist=False)
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
 
    
class TaskTracking(db.Model, Base):
    __tablename__ = "tasktrackings"

    remarks = db.Column(db.Text())  # should be markdown.
    time_done = db.Column(db.Integer, default=0)

    def __str__(self):
        return "<TaskTracker %s>" % (self.id)


for m in [Telephone,Email,Contact, CompaniesContacts, User, Company,UsersOrganizations, Comment, Link, \
         UsersSprints,Organization, Deal,UsersProjects, ContactsProjects, Project, Sprint, Task, User, \
         Message, TaskTracking]:
    listen(m, 'before_insert', generate_id)
