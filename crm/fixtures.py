from crm.apps.comment.models import Comment
from crm.apps.company.models import Company
from crm.apps.contact.models import Contact, Gender, SubgroupName, Subgroup, ActivityType, Activity
from crm.apps.country.countries import CountriesEnum
from crm.apps.country.models import Country
from crm.apps.currency.models import Currency
from crm.apps.deal.models import Deal
from crm.apps.event.models import Event
from crm.apps.message.models import Message
from crm.apps.organization.models import Organization
from crm.apps.project.models import Project
from crm.apps.sprint.models import Sprint
from crm.apps.task.models import Task
from crm.apps.user.models import User
from crm.apps.passport.models import Passport

from faker import Faker
from random import choice

from crm.apps.link.models import Link
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

    def newcountry():
        name = choice([c for c in CountriesEnum])
        country = Country.query.filter_by(name=name).first()

        if country:
            return country
        country = Country(name=name)
        db.session.add(country)
        return country

    def newpassport():

        passport = Passport(passport_fullname="{} {}".format(fake.first_name(), fake.last_name()),
                            passport_number="{}{}".format(
                                fake.numerify(), fake.numerify()),
                            country=newcountry())
        db.session.add(passport)
        return passport

    def newcontact():
        firstname = fake.first_name()
        lastname = fake.last_name()

        u = Contact(firstname=firstname, lastname=lastname)
        u.subgroups = [newsubgroup(), newsubgroup()]
        u.activities = [newactivity(), newactivity()]
        u.telephones = newphones()
        u.emails = newemails()
        u.owner = newuser()
        u.ownerbackup = newuser()
        u.gender = choice([Gender.MALE, Gender.FEMALE])
        u.passports = [newpassport(), newpassport()]
        u.countries = [newcountry(), newcountry()]
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
        dealvalue = 3000

        deal = Deal(name=dealname, value=dealvalue)
        deal.currency = newcurrency()
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

    def newevent():
        e = Event(title=fake.sentence(3) + " event",
                  description=fake.paragraph())
        e.contacts = [newcontact(), newcontact()]
        e.tasks = [newtask(), newtask()]
        db.session.add(e)
        return e

    def newcurrency():
        name = choice(['USD', 'EUR', 'AED', 'GBP', 'BTC'])
        c = Currency.query.filter_by(name=name).first()
        if c:
            return c
        c = Currency(name=name)
        db.session.add(c)
        return c

    def newsubgroup():
        name = choice([s for s in SubgroupName])
        s = Subgroup.query.filter_by(groupname=name).first()
        if s:
            return s
        s = Subgroup(groupname=name)
        db.session.add(s)
        return s

    def newactivity():
        type = choice([s for s in ActivityType])
        a = Activity.query.filter_by(type=type).first()
        if a:
            return a
        a = Activity(type=type)
        db.session.add(a)
        return a


    for i in range(3):
        newuser()
        newcontact()
        newcompany()
        newproj()
        neworg()
        newdeal()
        newsprint()
        newevent()

        db.session.commit()


def import_fixtures():
    pass


def export_fixtures():
    pass
