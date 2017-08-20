from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
db = SQLAlchemy() # init later in app.py


class Telephone(db.Model):
    __tablename__ = "telephones"
    id = db.Column('telephone_id',db.Integer, primary_key=True)
    number = db.Column(db.String(10))  # how long is phoneumber
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    contact = db.relationship("Contact", back_populates="telephones") 
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    company = db.relationship("Company", back_populates="telephones") 

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column('contact_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    firstname = db.Column(db.String(10))
    lastname = db.Column(db.String(10))
    email = db.Column(db.String(10))
    telephones = db.relationship("Telephone", back_populates="contact")
    message_channels = db.Column(db.String(10))
    description = db.Column(db.String(100))  #should be markdown.
    deals = db.relationship("Deal", back_populates="contact") 
    comments = db.relationship("Comment", back_populates="contact")
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="users")  
    tasks = db.relationship("Task", back_populates="assignee") 
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.organization_id"))
    organization = db.relationship("Organization", back_populates="users")
    messages = db.relationship("Message", back_populates="contact") 

 
    # owner
    #?
    # ownerbackup
    #?

    isuser = db.Column(db.Boolean, default=False)
    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)



class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column('company_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    name = db.Column(db.String(10))
    description = db.Column(db.String(100))  #should be markdown.
    email = db.Column(db.String(10))
    telephones = db.relationship("Telephone", back_populates="company")
    deals = db.relationship("Deal", back_populates="company") 
    messages = db.relationship("Message", back_populates="company") 
    # owner
    #?
    # ownerbackup
    #?
    comments = db.relationship("Comment", back_populates="company") 
    isuser = db.Column(db.Boolean, default=False)
    tasks = db.relationship("Task", back_populates="company") 
    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Organization(db.Model):
    __tablename__ = "organizations"
    id = db.Column('organization_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    name = db.Column(db.String(10))
    description = db.Column(db.String(100))  #should be markdown.
    email = db.Column(db.String(10))
    tasks = db.relationship("Task", back_populates="organization") 
    users = db.relationship("Contact", back_populates="organization")
    comments = db.relationship("Comment", back_populates="organization") 
    messages = db.relationship("Message", back_populates="organization") 
    sprints = db.relationship("Sprint", back_populates="organization") 

    # promoter 

    #?
    # gaurdian 
    #?
    # parent (organization)
    # ?

    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)



#     owner (link to 1 contacs which is users)
#     owner_backup (link to 1 contact which is users)


class DealState(Enum):
    NEW, INTERESTED, CONFIRMED, WAITINGCLOSED, CLOSED = range(5)

class DealType(Enum):
    HOSTER, ITO, PTO, PREPTO = range(4)

class DealCurrency(Enum):
    USD, EUR, AED, GBP = range(4)


class Deal(db.Model):
    __tablename__ = "deals"
    id = db.Column('deal_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    name = db.Column(db.String(10))

    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    company = db.relationship("Company", back_populates="deals") 

    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    contact = db.relationship("Contact", back_populates="deals") 

    deal_type = db.Column(db.Enum(DealType), default=DealType.HOSTER)
    deal_state = db.Column(db.Enum(DealState), default=DealState.NEW)

    tasks = db.relationship("Task", back_populates="deal") 
    company = db.relationship("Company", back_populates="deals") 
    
    comments = db.relationship("Comment", back_populates="deal") 
    messages = db.relationship("Message", back_populates="deal") 
    remarks = db.Column(db.String(100))  #should be markdown.

    amount = db.Column(db.Integer)  # default to int.
    currency = db.Column(db.Enum(DealCurrency), default=DealCurrency.EUR)
    # owner
    #?
    # ownerbackup
    #?

    isuser = db.Column(db.Boolean, default=False)
    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    closed_at= db.Column(db.TIMESTAMP, nullable=True) # should be?




class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column('project_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    name = db.Column(db.String(10))
    description = db.Column(db.String(100))  #should be markdown.
    
    users = db.relationship("Contact", back_populates="project")
    comments = db.relationship("Comment", back_populates="project")
    tasks = db.relationship("Task", back_populates="project")
    sprints = db.relationship("Sprint", back_populates="project")
    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP) 
    messages = db.relationship("Message", back_populates="project") 
    # promoter 
    #?
    # gaurdian 
    #?
    # parent (organization)
    # ?

    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    def percentage_done():
        pass

class ContactsSprints(db.Model):
    __tablename__ = 'contacts_sprints'
    id = db.Column(db.Integer(), primary_key=True)
    contact_id = db.Column(db.Integer(), db.ForeignKey('contacts.contact_id')) #, ondelete='CASCADE'))
    sprint_id = db.Column(db.Integer(), db.ForeignKey('sprints.sprint_id')) #, ondelete='CASCADE'))

class Sprint(db.Model):
    __tablename__ = "sprints"
    id = db.Column('sprint_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    name = db.Column(db.String(10))
    description = db.Column(db.String(100))  #should be markdown.
    
    users = db.relationship("Contact", secondary="contacts_sprints", backref=db.backref("sprints"), lazy="dynamic")
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="sprints")
    
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.organization_id"))
    organization = db.relationship("Organization", back_populates="sprints")

    tasks = db.relationship("Task", back_populates="sprint")
    comments = db.relationship("Comment", back_populates="sprint") 
    start_date = db.Column(db.TIMESTAMP)
    deadline = db.Column(db.TIMESTAMP) 
    messages = db.relationship("Message", back_populates="sprint") 
    # owner 
    #?
    # gaurdian 
    #?
    # parent (organization)
    # ?

    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    def percentage_done():
        pass

    def hours_open():
        pass

    def hours_open_person_avg():
        pass

    def hours_open_person_max():
        pass

    # uid = random 4 letters/numbers e.g. sie7 (generated at start, check is unique)
    # contact_uid
    # deal_uid
    # project_uid
    # organization_uid
    # task_uid
    # sprint_uid
    # content (is markdown)
    # owner (link to 1 contact which is users)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column('comment_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    name = db.Column(db.String(10))

    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    company = db.relationship("Company", back_populates="comments") 

    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    contact = db.relationship("Contact", back_populates="comments") 
    
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.deal_id"))
    deal = db.relationship("Deal", back_populates="comments") 
    
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))
    task = db.relationship("Task", back_populates="comments") 

    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.organization_id"))
    organization = db.relationship("Organization", back_populates="comments") 
 
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="comments") 

    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.sprint_id"))
    sprint = db.relationship("Sprint", back_populates="comments") 

    remarks = db.Column(db.String(100))  #should be markdown. 
    content = db.Column(db.String(100))  #should be markdown.


    # owner
    #?
    # ownerbackup
    #?

    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TaskType(Enum):
    FEATURE, QUESTION, TASK, STORY, CONTACT = range(5)


class TaskPriority(Enum):
    MINOR, NORMAL, URGENT, CRITICAL = range(4)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column('task_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    title = db.Column(db.String(10))
    description = db.Column(db.String(100))  #should be markdown.

    type = db.Column(db.Enum(TaskType), default=TaskType.FEATURE)
    priortiy = db.Column(db.Enum(TaskPriority), default=TaskPriority.MINOR)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    company = db.relationship("Company", back_populates="tasks") 

    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    assignee = db.relationship("Contact", back_populates="tasks") 
    
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.deal_id"))
    deal = db.relationship("Deal", back_populates="tasks") 
    
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.organization_id"))
    organization = db.relationship("Organization", back_populates="tasks") 
 
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="tasks") 

    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.sprint_id"))
    sprint = db.relationship("Sprint", back_populates="tasks") 
    messages = db.relationship("Message", back_populates="task") 
    comments = db.relationship("Comment", back_populates="task") 
    remarks = db.Column(db.String(100))  #should be markdown. 
    content = db.Column(db.String(100))  #should be markdown.

class MessageChannel(Enum):
    TELEGRAM, EMAIL, SMS, INTERCOM = range(4)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column('comment_id', db.Integer, primary_key=True)
    uid = db.Column(db.String(4))
    title = db.Column(db.String(10))
    content = db.Column(db.String(100))  #should be markdown.

    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))
    company = db.relationship("Company", back_populates="messages") 

    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    contact = db.relationship("Contact", back_populates="messages") 
    
    deal_id = db.Column(db.Integer, db.ForeignKey("deals.deal_id"))
    deal = db.relationship("Deal", back_populates="messages") 
    
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))
    task = db.relationship("Task", back_populates="messages") 

    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.organization_id"))
    organization = db.relationship("Organization", back_populates="messages") 
 
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", back_populates="messages") 

    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.sprint_id"))
    sprint = db.relationship("Sprint", back_populates="messages") 

    channel = db.Column(db.String(100))  #should be markdown. 

    time_tosend = db.Column(db.TIMESTAMP)
    time_sent = db.Column(db.TIMESTAMP)

    # timestamps
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


