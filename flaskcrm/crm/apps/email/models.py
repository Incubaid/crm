from crm.db import db, BaseModel
from crm.admin import ExtraMixin


class Email(db.Model, BaseModel, ExtraMixin):

    __tablename__ = "emails"

    email = db.Column(
        db.String(150),
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

    organization_id = db.Column(
        db.String(5),
        db.ForeignKey("organizations.id")
    )

    def __str__(self):
        return self.email
