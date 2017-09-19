from crm.db import db, BaseModel
from crm.admin import ExtraMixin


class Telephone(db.Model, BaseModel, ExtraMixin):

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
