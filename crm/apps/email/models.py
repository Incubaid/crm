from crm import db, BaseModel


class Email(db.Model, BaseModel):
    __tablename__ = "emails"

    email = db.Column(
        db.String(255),
        index=True,
        nullable=False,
    )

    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    contact_id = db.Column(
        db.String,
        db.ForeignKey("contacts.id")
    )

    organization_id = db.Column(
        db.String,
        db.ForeignKey("organizations.id")
    )

    company_id = db.Column(
        db.String,
        db.ForeignKey("companies.id")
    )

    def __str__(self):
        return self.email
