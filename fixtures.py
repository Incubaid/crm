from models import db
from models import Telephone, Email, Contact, Company, Organization, Deal, Link, Project, Sprint, Task, Comment, Message
from faker import Faker

fake = Faker()


def do_fixtures():
    global db

    def newemail():
        em = Email(email=fake.email())
        db.session.add(em)
        return em

    def newlink():
        labels = "critical, minor, urgent, fixed, inprogress"
        l = Link(url=fake.url(), labels=labels)
        l.comments = [newcomment() for i in range(2)]
        db.session.add(l)

        return l

    def newuser():
        phonenumber = fake.phone_number()
        firstname = fake.first_name()
        lastname = fake.last_name()
        phoneobj = Telephone(number=phonenumber)
        email = newemail()
        u = Contact(firstname=firstname, lastname=lastname)
        u.telephones = [phoneobj]
        u.emails = [email]
        db.session.add(phoneobj)

        u.comments = [newcomment() for i in range(2)]
        u.tasks = [newtask() for i in range(2)]
        u.messages = [newmsg() for i in range(2)]
        u.links = [newlink() for i in range(3)]
        db.session.add(u)
        return u

    def newcompany():
        companyname = fake.company()
        companyemail = newemail()
        description = fake.catch_phrase()
        company = Company(name=companyname,
                          description=description)
        companyphone = Telephone(number=fake.phone_number())
        company.telephones = [companyphone]
        company.emails = [companyemail]
        company.owner = newuser()
        db.session.add(company)
        company.comments = [newcomment() for i in range(5)]
        company.messages = [newmsg() for i in range(20)]

        db.session.add(companyphone)
        return company

    def neworg():
        orgname = fake.company() + "org"
        orgemail = newemail()
        description = fake.catch_phrase()

        org = Organization(name=orgname,
                           description=description)
        org.emails = [orgemail]
        org.comments = [newcomment() for i in range(5)]
        org.tasks = [newtask() for i in range(5)]
        org.messages = [newmsg() for i in range(20)]

        org.links = [newlink() for i in range(3)]
        db.session.add(org)
        return org

    def newproj():
        projname = fake.name() + "proj"
        projdesc = fake.paragraph()
        proj = Project(name=projname, description=projdesc)
        proj.comments = [newcomment() for i in range(5)]
        proj.tasks = [newtask() for i in range(5)]
        proj.messages = [newmsg() for i in range(5)]
        proj.links = [newlink() for i in range(3)]
        proj.users = [newuser(), newuser()]
        db.session.add(proj)
        return proj

    def newsprint():
        sprintname = fake.name() + "sprint"
        sprintdesc = fake.paragraph()
        sprint = Sprint(name=sprintname, description=sprintdesc)
        sprint.users = [newuser() for i in range(2)]
        sprint.org = neworg()
        sprint.tasks = [newtask() for i in range(5)]
        sprint.comments = [newcomment() for i in range(5)]
        sprint.messages = [newmsg() for i in range(5)]
        sprint.project = newproj()
        sprint.links = [newlink() for i in range(3)]

        db.session.add(sprint)

        return sprint

    def newdeal():

        dealname = fake.name() + "deal"
        dealamount = 5000
        deal = Deal(name=dealname, amount=dealamount)
        deal.comments = [newcomment() for i in range(5)]
        deal.tasks = [newtask() for i in range(5)]
        deal.messages = [newmsg() for i in range(5)]
        deal.links = [newlink() for i in range(3)]
        deal.company = newcompany()
        db.session.add(deal)

        return deal

    def newcomment():
        com = Comment(name=fake.sentence(4),
                      content=fake.paragraph())
        db.session.add(com)
        return com

    def newtask():
        t = Task(title=fake.sentence(5), content=fake.paragraph(),
                 remarks=fake.paragraph())
        t.comments = [newcomment() for i in range(10)]
        db.session.add(t)
        return t

    def newmsg():
        m = Message(title=fake.sentence(5), content=fake.paragraph())
        db.session.add(m)
        return m

    for i in range(5):
        u = newuser()

        com = newcompany()
        proj = newproj()
        org = neworg()
        deal = newdeal()
        sprint = newsprint()

    db.session.commit()
