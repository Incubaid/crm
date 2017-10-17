from faker import Faker

from crm.company.models import Company
from crm.contact.models import Contact
from crm.deal.models import Deal
from crm.link.models import Link
from crm.organization.models import Organization
from crm.project.models import Project
from crm.sprint.models import Sprint
from crm.user.models import User
from crm.comment.models import Comment
from crm.task.models import Task
from crm.message.models import Message

from crm.db import db


fake = Faker()


def generate_fixtures():

    def newemails():
        return ','.join([fake.email(), fake.email()])

    def newphones():
        return ','.join([fake.phone_number(), fake.phone_number()])

    def newlink():
        labels = "critical, minor, urgent, fixed, inprogress"
        l = Link(url=fake.url(), labels=labels)
        l.comments = [newcomment() for i in range(2)]
        db.session.add(l)

        return l



    def newcontact():
        firstname = fake.first_name()
        lastname = fake.last_name()

        u = Contact(firstname=firstname, lastname=lastname)
        u.telephones = newphones()
        u.emails = newemails()
        u.owner = newuser()
        u.ownerbackup = newuser()

        u.comments = [newcomment() for i in range(2)]
        u.tasks = [newtask() for i in range(2)]
        u.messages = [newmsg() for i in range(2)]
        u.links = [newlink() for i in range(3)]
        db.session.add(u)
        return u


    def newuser():
        firstname = fake.first_name()
        lastname = fake.last_name()
        u = User(firstname=firstname, lastname=lastname)
        u.description = fake.paragraph()
        u.telephones = newphones()
        u.emails = newemails()
        u.comments = [newcomment() for i in range(2)]
        u.messages = [newmsg() for i in range(2)]
        u.links = [newlink() for i in range(3)]
        u.ownsTasks = [newtask(), newtask()]
        u.tasks = [newtask(), newtask()]
        db.session.add(u)

        return u

    def newcompany():
        companyname = fake.company()
        description = fake.catch_phrase()
        company = Company(name=companyname,
                          description=description)
        company.contacts = [newcontact() for i in range(2)]
        company.telephones = newphones()
        company.emails = newemails()
        company.website = fake.url()
        company.owner = newuser()
        company.ownerbackup = newuser()
        db.session.add(company)
        company.comments = [newcomment() for i in range(3)]
        company.messages = [newmsg() for i in range(3)]

        return company

    def neworg():
        orgname = fake.company() + "org"
        description = fake.catch_phrase()

        org = Organization(name=orgname,
                           description=description)

        org.promotor = newuser()
        org.guardian = newuser()
        org.users = [newuser(), newuser()]
        org.emails = newemails()
        org.comments = [newcomment() for i in range(3)]
        org.tasks = [newtask() for i in range(3)]
        org.messages = [newmsg() for i in range(3)]

        org.links = [newlink() for i in range(3)]
        db.session.add(org)
        return org

    def newproj():
        projname = fake.name() + "proj"
        projdesc = fake.paragraph()
        proj = Project(name=projname, description=projdesc)
        proj.comments = [newcomment() for i in range(3)]
        proj.promotor = newuser()
        proj.guardian = newuser()
        proj.tasks = [newtask() for i in range(3)]
        proj.messages = [newmsg() for i in range(3)]
        proj.links = [newlink() for i in range(3)]
        proj.contacts = [newcontact() for i in range(3)]
        proj.users = [newuser(), newuser()]
        db.session.add(proj)
        return proj

    def newsprint():
        sprintname = fake.name() + "sprint"
        sprintdesc = fake.paragraph()
        sprint = Sprint(name=sprintname, description=sprintdesc)
        sprint.users = [newuser() for i in range(2)]
        sprint.contacts = [newcontact() for i in range(2)]
        sprint.org = neworg()
        sprint.tasks = [newtask() for i in range(3)]
        sprint.comments = [newcomment() for i in range(3)]
        sprint.messages = [newmsg() for i in range(3)]
        sprint.project = newproj()
        sprint.links = [newlink() for i in range(3)]

        db.session.add(sprint)

        return sprint

    def newdeal():

        dealname = fake.name() + "deal"
        dealamount = 3000
        deal = Deal(name=dealname, amount=dealamount)
        deal.comments = [newcomment() for i in range(3)]
        deal.tasks = [newtask() for i in range(3)]
        deal.messages = [newmsg() for i in range(3)]
        deal.links = [newlink() for i in range(3)]
        deal.company = newcompany()
        db.session.add(deal)

        return deal

    def newcomment():
        com = Comment(content=fake.paragraph())
        db.session.add(com)
        return com

    def newtask():
        t = Task(title=fake.sentence(3) + "task", description=fake.paragraph())
        t.comments = [newcomment() for i in range(3)]
        db.session.add(t)
        return t

    def newmsg():
        m = Message(title=fake.sentence(3), content=fake.paragraph())
        db.session.add(m)
        return m
    for i in range(3):
        u = newuser()
        tu = newcontact()
        com = newcompany()
        proj = newproj()
        org = neworg()
        deal = newdeal()
        sprint = newsprint()

    db.session.commit()


def import_fixtures():
    pass


def export_fixtures():
    pass
