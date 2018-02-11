from crm import db, BaseModel


class Phone(db.Model, BaseModel):
    __tablename__ = "phones"

    telephone = db.Column(
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

    company_id = db.Column(
        db.String,
        db.ForeignKey("companies.id")
    )

    def __str__(self):
        return self.telephone

