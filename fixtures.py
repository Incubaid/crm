from models import db
from models import Telephone, Contact, Company, Organization, Deal, Link, Project, Sprint, Task, Comment, Message


def do_fixtures():
    global db
    t1 = Telephone(number="01145533120")
    db.session.add(t1)
    u1 = Contact(firstname="ahmed", lastname="thabet",
                 email="thabeta@dmdm.com")
    u1.telephones = [t1]
    db.session.add(u1)

    t2 = Telephone(number="01145533120")
    db.session.add(t2)
    u2 = Contact(firstname="dom", lastname="xander",
                 email="fast5@dmdm.com")
    u2.telephones = [t2]
    db.session.add(u2)

    t3 = Telephone(number="010221331892")
    u3 = Contact(firstname="frodo", lastname="hobbit",
                 email="fordo@hobbits.land")
    u3.telephones = [t3]

    db.session.add(t3)
    db.session.add(u3)

    c1 = Company(name="pureevil", description="pureevil inc",
                 email="monster@dmd.inc")
    c1.telephones.append(t1)

    db.session.add(c1)
    t4 = Telephone(number="010221331892")

    c2 = Company(name="monsters", description="monsters inc",
                 email="monsters@no.inc")
    c2.telephones.append(t2)

    db.session.add(c2)

    o1 = Organization(
        name="dmdmit", description="change the world", email="dmdmit@dmdm.org")
    o1.users.append(u2)

    db.session.add(o1)

    d1 = Deal(name="cairodeal", amount=10000)
    d1.company = c1
    u1.deals.append(d1)
    d2 = Deal(name="dubaideal", amount=50000)
    d2.company = c1
    u2.deals.append(d2)

    com1 = Comment(name="a very first comment",
                   content="Works for me prettty long one")
    com2 = Comment(name="second comment", content="LGTM")
    com3 = Comment(name="third comment", content="Can you please update that?")
    com4 = Comment(name="fourth comment", content="Nope won't work.")
    com5 = Comment(name="fifth comment", content="gibberish dmdmdm")
    u1.comments.append(com1)
    d1.comments.append(com2)
    u1.comments.append(com3)
    u2.comments.append(com4)
    u1.comments.append(com5)

    o1.comments.append(com1)
    db.session.add(com1, com2)

    p1 = Project(name="proj1", description="dmdmproj", comments=[com1, com2])
    t1 = Task(title="task1", content="fix dmdm",
              remarks="someremarks")
    t2 = Task(title="task1", content="fix dmdm",
              remarks="someremarks")
    u1.tasks.append(t1)
    u1.tasks.append(t2)

    db.session.add(p1, t1)
    db.session.commit()
